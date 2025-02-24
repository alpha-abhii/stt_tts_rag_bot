# import requests
# import io
# from pypdf import PdfReader
# import re
# from uuid import uuid4
# from vector_store import get_collection, get_vectorstore

# ## function to read the pdf documents
# def extract_text_from_url(pdf_url):
#     response = requests.get(pdf_url)
#     response.raise_for_status() 
#     pdf_stream = io.BytesIO(response.content)
    
#     reader = PdfReader(pdf_stream)
#     text = ""
#     ## looping over the pages to extract text
#     for page_number in range(len(reader.pages)):
#         page = reader.pages[page_number]
#         text += page.extract_text()
#     return text

# ## function to classify whether text is link or simple text and then storing in DB
# def store_in_DB(data, user_id):
#     ## classify if data is URL or not
#     pattern = r"^https:"
#     if re.match(pattern, data):
#         text = extract_text_from_url(data)
#     else:
#         text = data

#     doc1 = [text]
#     metadata = [{"source" : user_id}]
#     id = [str(uuid4())]

#     client, collection = get_collection()
#     collection.add(documents=doc1, metadatas=metadata, ids=id)
#     print(f"Document added in DB")

# ## deleting documents of a particular user
# def delete_data_from_DB(user_id):
#     vstr = get_vectorstore()
#     print(f"Going to delete documents from user id : {user_id}")
#     res = vstr.get(where={"source": user_id})
#     ids = res['ids']
#     print(ids)
#     vstr.delete(ids=ids)
#     print(f"Document are deleted for user_id : {user_id}")



import requests
import io
from pypdf import PdfReader
import re
from uuid import uuid4
from vector_store import get_collection, get_vectorstore
from typing import List, Dict, Union
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def extract_text_from_url(pdf_url: str) -> str:
    """
    Extracts text from a PDF file located at the given URL.

    Args:
        pdf_url (str): The URL of the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    try:
        # Fetch the PDF content from the URL
        response = requests.get(pdf_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Read the PDF content
        pdf_stream = io.BytesIO(response.content)
        reader = PdfReader(pdf_stream)

        # Extract text from each page
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        return text
    except Exception as e:
        print(f"Error extracting text from URL {pdf_url}: {e}")
        raise


def classify_and_extract_text(data: str) -> str:
    """
    Classifies whether the input data is a URL or plain text and extracts text accordingly.

    Args:
        data (str): The input data (URL or plain text).

    Returns:
        str: The extracted or original text.
    """
    # Check if the data is a URL
    pattern = r"^https:"
    if re.match(pattern, data):
        return extract_text_from_url(data)
    else:
        return data


def store_in_DB(data: str, user_id: str):
    """
    Stores the given data in the vector database.

    Args:
        data (str): The input data (URL or plain text).
        user_id (str): The ID of the user associated with the data.
    """
    try:
        # Classify and extract text
        text = classify_and_extract_text(data)

        # Prepare documents, metadata, and IDs for storage
        doc1 = [text]
        metadata = [{"source": user_id}]
        id = [str(uuid4())]

        # Add the document to the collection
        client, collection = get_collection()
        collection.add(documents=doc1, metadatas=metadata, ids=id)
        print(f"Document added to DB for user_id: {user_id}")
    except Exception as e:
        print(f"Error storing data in DB: {e}")
        raise


def delete_data_from_DB(user_id: str):
    """
    Deletes all documents associated with the given user ID from the vector database.

    Args:
        user_id (str): The ID of the user whose documents should be deleted.
    """
    try:
        # Retrieve the vector store
        vstr = get_vectorstore()

        # Fetch document IDs associated with the user ID
        print(f"Deleting documents for user_id: {user_id}")
        res = vstr.get(where={"source": user_id})
        ids = res["ids"]

        # Delete the documents
        if ids:
            vstr.delete(ids=ids)
            print(f"Documents deleted for user_id: {user_id}")
        else:
            print(f"No documents found for user_id: {user_id}")
    except Exception as e:
        print(f"Error deleting data from DB: {e}")
        raise


if __name__ == "__main__":
    # Example usage for testing
    try:
        # Test storing a document
        data = "https://example.com/sample.pdf"  # Replace with a valid PDF URL or plain text
        user_id = "test_user_123"
        store_in_DB(data, user_id)

        # Test deleting documents
        delete_data_from_DB(user_id)
    except Exception as e:
        print(f"Error during example usage: {e}")