# import numpy as np
# import os
# from langchain.schema import HumanMessage
# ##import google.generativeai as genai
# from langchain_google_genai import ChatGoogleGenerativeAI
# from vector_store import get_retriever
# from dotenv import load_dotenv

# load_dotenv()

# google_api_key = os.getenv("GOOGLE_API_KEY")

# if google_api_key:
#     os.environ["GOOGLE_API_KEY"] = google_api_key
# else:
#     raise ValueError("GOOGLE_API_KEY environment variable is not set!")


# class RAG_bot:
#     def __init__(self):
#         ##self.model = genai.GenerativeModel("gemini-pro")
#         self.model = ChatGoogleGenerativeAI(model="gemini-pro")
#         self.list1 = []
#         self.retriever = get_retriever()
    
#     def make_rag_prompt(self, query, relevant_passage):
#         escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
#         prompt = ("""You are a helpful and informative bot that answers questions using text from the reference passage included below. \
#         Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
#         However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
#         strike a friendly and converstional tone. \
#         If the passage is irrelevant to the answer, you may ignore it and return that query asked is Irrelevant.
#         QUESTION: '{query}'
#         PASSAGE: '{relevant_passage}'

#         ANSWER:
#         """).format(query=query, relevant_passage=escaped)

#         return prompt

#     # Function to create a QA chain with a given document and query
#     def qa_chain(self, query, user_id):

#         docs = self.retriever.invoke(query, filter={"source": user_id})
        
#         ##print(document)
#         custom_prompt = self.make_rag_prompt(query, docs[0].page_content)
#         # Step 6: Use the retrieved context and the query to generate the answer using the language model
#         model1 = self.model
#         messages = [HumanMessage(content=custom_prompt)]
#         answer = model1(messages)
#         ##answer = answer.candidates[0].content.parts[0].text
#         answer_text = answer.content
#         return {
#             "answer" : answer_text
#         }


import os
from langchain.schema import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from vector_store import get_retriever
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Validate Google API Key
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set!")
os.environ["GOOGLE_API_KEY"] = google_api_key


class RAG_bot:
    def __init__(self):
        """
        Initializes the RAG bot with a language model and a retriever.
        """
        self.model = ChatGoogleGenerativeAI(model="gemini-pro")
        self.retriever = get_retriever()

    def make_rag_prompt(self, query, relevant_passage):
        """
        Constructs a RAG prompt using the query and relevant passage.

        Args:
            query (str): The user's query.
            relevant_passage (str): The relevant passage retrieved from the vector store.

        Returns:
            str: The formatted RAG prompt.
        """
        # Escape special characters in the passage
        escaped_passage = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")

        # Construct the prompt
        prompt = f"""
        You are a helpful and informative bot that answers questions using text from the reference passage included below. \
        Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
        However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
        strike a friendly and conversational tone. \
        If the passage is irrelevant to the answer, you may ignore it and return that the query asked is irrelevant.

        QUESTION: '{query}'
        PASSAGE: '{escaped_passage}'

        ANSWER:
        """
        return prompt

    def qa_chain(self, query, user_id):
        """
        Executes the QA chain to generate an answer for the given query.

        Args:
            query (str): The user's query.
            user_id (str): The ID of the user for filtering documents.

        Returns:
            dict: A dictionary containing the generated answer.
        """
        try:
            # Retrieve relevant documents for the query and user_id
            docs = self.retriever.invoke(query, filter={"source": user_id})
            if not docs:
                return {"answer": "No relevant documents found."}

            # Create a RAG prompt using the query and the most relevant document
            custom_prompt = self.make_rag_prompt(query, docs[0].page_content)

            # Generate the answer using the language model
            messages = [HumanMessage(content=custom_prompt)]
            answer = self.model(messages)

            return {
                "answer": answer.content
            }
        except Exception as e:
            print(f"Error in qa_chain: {e}")
            return {
                "answer": "An error occurred while processing your query. Please try again later."
            }


if __name__ == "__main__":
    # Example usage for testing
    try:
        rag_bot = RAG_bot()
        query = "What is the capital of France?"
        user_id = "example_user_id"
        response = rag_bot.qa_chain(query, user_id)
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error during RAG bot execution: {e}")