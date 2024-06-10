from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
import time
import openai

def extract_text_from_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1800, chunk_overlap=50)
    chunked_documents = text_splitter.split_documents(docs)
    return chunked_documents

def create_vector_db(documents, api_key, persist_directory="./chroma_db", max_retries=5):
    for attempt in range(max_retries):
        try:
            vectordb = Chroma.from_documents(
                documents, OpenAIEmbeddings(model="text-embedding-ada-002", api_key=api_key),
                persist_directory=persist_directory
            )
            return vectordb
        except openai.error.RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) * 10  # Espera exponencial
                print(f"RateLimitError: {e}. Reintentando en {wait_time} segundos...")
                time.sleep(wait_time)
            else:
                raise
        except Exception as e:
            raise

    return None
