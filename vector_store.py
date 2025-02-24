# from embeddings import embedding_func
# import chromadb
# from langchain_chroma import Chroma

# def get_collection():
#     client = chromadb.PersistentClient(path='./data/ChromaDB_2')
#     collection = client.get_collection(name='Minisoft_data3', embedding_function=embedding_func)
#     print(f"Collection found.")
#     return client, collection


# def get_vectorstore():
#     client, collection = get_collection()
#     vector_store = Chroma(
#         client=client,
#         collection_name="Minisoft_data3",
#         embedding_function=embedding_func,
#     )
#     return vector_store


# def get_retriever():
#     vector_store = get_vectorstore()
#     retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 1, "fetch_k": 1})
#     return retriever




# from embeddings import embedding_func
# import chromadb
# from langchain_chroma import Chroma
# import os

# # Constants for configuration
# CHROMA_DB_PATH = "./data/ChromaDB_2"
# COLLECTION_NAME = "Minisoft_data3"

# def get_collection():
#     """
#     Retrieves or creates a ChromaDB collection.

#     Returns:
#         tuple: A tuple containing the ChromaDB client and collection.
#     """
#     try:
#         # Ensure the directory for ChromaDB exists
#         os.makedirs(CHROMA_DB_PATH, exist_ok=True)

#         # Initialize the ChromaDB client
#         client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

#         # Get or create the collection
#         collection = client.get_or_create_collection(
#             name=COLLECTION_NAME,
#             embedding_function=embedding_func
#         )
#         print(f"Collection '{COLLECTION_NAME}' retrieved or created successfully.")
#         return client, collection
#     except Exception as e:
#         print(f"Error in get_collection: {e}")
#         raise

# def get_vectorstore():
#     """
#     Retrieves the vector store from the ChromaDB collection.

#     Returns:
#         Chroma: The vector store object.
#     """
#     try:
#         client, collection = get_collection()
#         vector_store = Chroma(
#             client=client,
#             collection_name=COLLECTION_NAME,
#             embedding_function=embedding_func,
#         )
#         return vector_store
#     except Exception as e:
#         print(f"Error in get_vectorstore: {e}")
#         raise

# def get_retriever(search_type="mmr", k=1, fetch_k=1):
#     """
#     Retrieves a retriever from the vector store.

#     Args:
#         search_type (str): The type of search to perform (e.g., "mmr").
#         k (int): The number of documents to retrieve.
#         fetch_k (int): The number of documents to fetch before filtering.

#     Returns:
#         Retriever: The retriever object.
#     """
#     try:
#         vector_store = get_vectorstore()
#         retriever = vector_store.as_retriever(
#             search_type=search_type,
#             search_kwargs={"k": k, "fetch_k": fetch_k}
#         )
#         return retriever
#     except Exception as e:
#         print(f"Error in get_retriever: {e}")
#         raise

# if __name__ == "__main__":
#     # Example usage for testing
#     try:
#         retriever = get_retriever()
#         print("Retriever created successfully.")
#     except Exception as e:
#         print(f"Error during retriever creation: {e}")



from embeddings import embedding_func
import chromadb
from langchain_chroma import Chroma
import os
from google.cloud import storage

# Constants for configuration
CHROMA_DB_PATH = "data/ChromaDB_2"
COLLECTION_NAME = "Minisoft_data3"
GCS_BUCKET_NAME = os.getenv("CHROMADB_BUCKET", "chromadb-data-bucket")  # GCS bucket name
GCS_CHROMADB_FOLDER = "ChromaDB_2"  # Folder in GCS where ChromaDB data is stored

def download_chromadb_from_gcs():
    """
    Downloads ChromaDB data from GCS to the local filesystem.
    """
    try:
        # Ensure the local directory exists
        os.makedirs(CHROMA_DB_PATH, exist_ok=True)

        # Initialize GCS client
        client = storage.Client()
        bucket = client.bucket(GCS_BUCKET_NAME)

        # List all files in the GCS folder
        blobs = bucket.list_blobs(prefix=GCS_CHROMADB_FOLDER)

        # Download each file to the local filesystem
        for blob in blobs:
            # Create the local file path
            relative_path = os.path.relpath(blob.name, GCS_CHROMADB_FOLDER)
            local_path = os.path.join(CHROMA_DB_PATH, relative_path)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            # Download the file
            blob.download_to_filename(local_path)
            print(f"Downloaded {blob.name} to {local_path}")

        print("ChromaDB data downloaded from GCS successfully.")
    except Exception as e:
        print(f"Error downloading ChromaDB data from GCS: {e}")
        raise

def get_collection():
    """
    Retrieves or creates a ChromaDB collection.

    Returns:
        tuple: A tuple containing the ChromaDB client and collection.
    """
    try:
        # Ensure the directory for ChromaDB exists
        os.makedirs(CHROMA_DB_PATH, exist_ok=True)

        # Initialize the ChromaDB client
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

        # Get or create the collection
        collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_func
        )
        print(f"Collection '{COLLECTION_NAME}' retrieved or created successfully.")
        return client, collection
    except Exception as e:
        print(f"Error in get_collection: {e}")
        raise

def get_vectorstore():
    """
    Retrieves the vector store from the ChromaDB collection.

    Returns:
        Chroma: The vector store object.
    """
    try:
        client, collection = get_collection()
        vector_store = Chroma(
            client=client,
            collection_name=COLLECTION_NAME,
            embedding_function=embedding_func,
        )
        return vector_store
    except Exception as e:
        print(f"Error in get_vectorstore: {e}")
        raise

def get_retriever(search_type="mmr", k=1, fetch_k=1):
    """
    Retrieves a retriever from the vector store.

    Args:
        search_type (str): The type of search to perform (e.g., "mmr").
        k (int): The number of documents to retrieve.
        fetch_k (int): The number of documents to fetch before filtering.

    Returns:
        Retriever: The retriever object.
    """
    try:
        vector_store = get_vectorstore()
        retriever = vector_store.as_retriever(
            search_type=search_type,
            search_kwargs={"k": k, "fetch_k": fetch_k}
        )
        return retriever
    except Exception as e:
        print(f"Error in get_retriever: {e}")
        raise

# Download ChromaDB data from GCS at startup
download_chromadb_from_gcs()

if __name__ == "__main__":
    # Example usage for testing
    try:
        retriever = get_retriever()
        print("Retriever created successfully.")
    except Exception as e:
        print(f"Error during retriever creation: {e}")