# model.py

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
import os
import openai

# Configura tu clave de API de OpenAI
openai.api_key = "sk-proj-w0EWSVDyfxNuSmVVJltlT3BlbkFJc7Tl7jWsxHwkrSaA2roa"

# Configura tu clave de API de OpenAI
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("No se proporcionó la clave de API. Verifique que el archivo .env contiene la clave OPENAI_API_KEY.")

def get_answer(question, api_key):
    vectordb = Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings(model="text-embedding-ada-002", api_key=api_key))
    similar_docs = vectordb.similarity_search(question, k=5)
    context = "\n".join([doc.page_content for doc in similar_docs])

    prompt_template = """
    Eres un asistente inteligente especializado en el reglamento académico. Responde las preguntas de los usuarios basándote estrictamente en el contexto proporcionado.

    Pregunta: {question}
    Contexto: {context}
    """

    llm = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=500, api_key=api_key)
    qa_chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(prompt_template))
    response = qa_chain.invoke({"question": question, "context": context})
    
    return response["text"]
