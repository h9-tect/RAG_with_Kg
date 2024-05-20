import os
from config import nebula_config
from database.setup_nebula import setup_nebula
from kg_rag.query_kg_rag import load_documents, build_knowledge_graph, query_kg, create_custom_query_engine

def main():
    setup_nebula()
    
    documents = load_documents()
    
    from llama_index import StorageContext
    storage_context = StorageContext.from_defaults(graph_store=None)  # Replace None with actual graph store
    
    service_context = None  # Define your service context here
    
    kg_index = build_knowledge_graph(documents, storage_context, service_context)
    
    response_graph_rag = query_kg(kg_index, "What is the secure level of AES encryption")
    print(response_graph_rag)

    custom_query_engine = create_custom_query_engine(service_context, None, kg_index)  # Replace None with actual vector index
    
    response = custom_query_engine.query("What is your encryption method, how secure it is?")
    print(response)

if __name__ == "__main__":
    main()
