# Knowledge Graph RAG Setup

This repository provides a structured setup for configuring a Nebula graph database, building a knowledge graph, and integrating it with a Retrieval-Augmented Generation (RAG) model.

## Prerequisites

- Docker
- Python 3.9+

## Setup Instructions

1. **Clone the Repository**

    ```sh
    git clone https://github.com/yourusername/knowledge-graph-rag.git
    cd knowledge-graph-rag
    ```

2. **Install Docker**

    Ensure Docker is installed and running on your machine. You can download Docker from [here](https://www.docker.com/products/docker-desktop).

3. **Run Nebula Container**

    Execute the following Docker commands to pull and run the Nebula container:

    ```sh
    docker pull vesoft/nebula-graph:nightly
    docker run -d --name nebula-server vesoft/nebula-graph:nightly
    ```

4. **Set Environment Variables**

    Adjust environment variables as needed in `config/nebula_config.py`.

5. **Install Python Dependencies**

    Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

6. **Setup Nebula Database**

    Run the following command to set up the Nebula database:

    ```sh
    python database/setup_nebula.py
    ```

7. **Run the Main Application**

    Run the main application to build the knowledge graph and query it:

    ```sh
    python main.py
    ```

## Overview of Project Files

- **main.py**: The entry point of the application. It sets up the Nebula database, builds the knowledge graph, and performs queries.
- **config/nebula_config.py**: Contains the configuration for connecting to the Nebula database.
- **database/setup_nebula.py**: Sets up the Nebula database schema.
- **kg_rag/query_kg_rag.py**: Contains functions to load documents, build a knowledge graph, and query it. Also includes a custom retriever to combine results from vector and graph databases.
- **requirements.txt**: Lists the Python dependencies for the project.
- **Dockerfile**: Dockerfile to containerize the application.

## License

This project is licensed under the MIT License.
