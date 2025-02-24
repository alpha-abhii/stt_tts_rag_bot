# ## defining embedding function of Google AI
# import os
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from typing import List

# api_key = os.getenv("GOOGLE_API_KEY")


# class GoogleGenerativeAiEmbeddingFunction:
#     """Embedding function for Google Generative AI models."""

#     def __init__(self, api_key: str, model_name: str = "models/embedding-001"):
#         import google.generativeai as genai
#         genai.configure(api_key=api_key)
#         self._genai = genai
#         self._model_name = model_name

#     def __call__(self, input: List[str]) -> List[List[float]]:
#         """Generate embeddings for a list of documents."""
#         return [
#             self._genai.embed_content(
#                 model=self._model_name,
#                 content=text,
#                 task_type="RETRIEVAL_DOCUMENT"
#             )["embedding"]
#             for text in input
#         ]

#     def embed_query(self, input: str) -> List[float]:
#         """Generate an embedding for a single query."""
#         return self._genai.embed_content(
#             model=self._model_name,
#             content=input,
#             task_type="RETRIEVAL_QUERY"
#         )["embedding"]


# embedding_func = GoogleGenerativeAiEmbeddingFunction(api_key=api_key)




import os
from typing import List
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Validate Google API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set!")


class GoogleGenerativeAiEmbeddingFunction:
    """
    Embedding function for Google Generative AI models.

    Args:
        api_key (str): The Google API key.
        model_name (str): The name of the embedding model. Defaults to "models/embedding-001".
    """

    def __init__(self, api_key: str, model_name: str = "models/embedding-001"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self._genai = genai
            self._model_name = model_name
        except Exception as e:
            print(f"Error initializing GoogleGenerativeAiEmbeddingFunction: {e}")
            raise

    def __call__(self, input: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of documents.

        Args:
            input (List[str]): A list of documents to embed.

        Returns:
            List[List[float]]: A list of embeddings for the input documents.
        """
        try:
            return [
                self._genai.embed_content(
                    model=self._model_name,
                    content=text,
                    task_type="RETRIEVAL_DOCUMENT"
                )["embedding"]
                for text in input
            ]
        except Exception as e:
            print(f"Error generating embeddings for documents: {e}")
            raise

    def embed_query(self, input: str) -> List[float]:
        """
        Generate an embedding for a single query.

        Args:
            input (str): The query to embed.

        Returns:
            List[float]: The embedding for the query.
        """
        try:
            return self._genai.embed_content(
                model=self._model_name,
                content=input,
                task_type="RETRIEVAL_QUERY"
            )["embedding"]
        except Exception as e:
            print(f"Error generating embedding for query: {e}")
            raise


# Initialize the embedding function
embedding_func = GoogleGenerativeAiEmbeddingFunction(api_key=api_key)


if __name__ == "__main__":
    # Example usage for testing
    try:
        documents = ["This is a sample document.", "Another example document."]
        embeddings = embedding_func(documents)
        print(f"Document Embeddings: {embeddings}")

        query = "This is a sample query."
        query_embedding = embedding_func.embed_query(query)
        print(f"Query Embedding: {query_embedding}")
    except Exception as e:
        print(f"Error during embedding generation: {e}")