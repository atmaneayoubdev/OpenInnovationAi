from langchain_ollama import OllamaEmbeddings


def get_embedding_function():

    # Initialize the OllamaEmbeddings object
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # Now, the connection settings should be configured automatically via the environment variables
    return embeddings
