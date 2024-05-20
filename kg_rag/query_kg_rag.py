from llama_index import download_loader, KnowledgeGraphIndex, StorageContext, RetrieverQueryEngine, ResponseSynthesizer
from llama_index.retrievers import BaseRetriever, VectorIndexRetriever, KGTableRetriever
from typing import List

def load_documents():
    WikipediaReader = download_loader("WikipediaReader")
    loader = WikipediaReader()
    documents = loader.load_data(pages=['Advanced Encryption Standard'], auto_suggest=False)
    return documents

def build_knowledge_graph(documents, storage_context, service_context):
    kg_index = KnowledgeGraphIndex.from_documents(
        documents,
        storage_context=storage_context,
        service_context=service_context,
        max_triplets_per_chunk=10,
        space_name="rag_demo",
        edge_types=["relationship"],
        rel_prop_names=["relationship"],
        tags=["entity"],
    )
    return kg_index

def query_kg(kg_index, query):
    kg_index_query_engine = kg_index.as_query_engine(
        retriever_mode="keyword",
        verbose=True,
        response_mode="tree_summarize",
    )
    response = kg_index_query_engine.query(query)
    return response

class CustomRetriever(BaseRetriever):
    def __init__(self, vector_retriever: VectorIndexRetriever, kg_retriever: KGTableRetriever, mode: str = "OR") -> None:
        self._vector_retriever = vector_retriever
        self._kg_retriever = kg_retriever
        if mode not in ("AND", "OR"):
            raise ValueError("Invalid mode.")
        self._mode = mode
        
    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]: 
        vector_nodes = self._vector_retriever.retrieve(query_bundle)
        kg_nodes = self._kg_retriever.retrieve(query_bundle)

        vector_ids = {n.node.get_doc_id() for n in vector_nodes}
        kg_ids = {n.node.get_doc_id() for n in kg_nodes}
        
        combined_dict = {n.node.get_doc_id(): n for n in vector_nodes}
        combined_dict.update({n.node.get_doc_id(): n for n in kg_nodes})
        
        if self._mode == "AND":
            retrieve_ids = vector_ids.intersection(kg_ids)
        else:
            retrieve_ids = vector_ids.union(kg_ids)

        retrieve_nodes = [combined_dict[rid] for rid in retrieve_ids]
        return retrieve_nodes

def create_custom_query_engine(service_context, vector_index, kg_index):
    vector_retriever = VectorIndexRetriever(index=vector_index)
    kg_retriever = KGTableRetriever(index=kg_index, retriever_mode='keyword', include_text=False)
    custom_retriever = CustomRetriever(vector_retriever, kg_retriever)

    response_synthesizer = ResponseSynthesizer.from_args(
        service_context=service_context,
        response_mode="tree_summarize",
    )

    custom_query_engine = RetrieverQueryEngine(
        retriever=custom_retriever,
        response_synthesizer=response_synthesizer,
    )
    return custom_query_engine
