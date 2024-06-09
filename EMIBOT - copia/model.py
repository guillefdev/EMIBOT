import openai
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configura tu clave de API de OpenAI
openai.api_key = "sk-proj-w0EWSVDyfxNuSmVVJltlT3BlbkFJc7Tl7jWsxHwkrSaA2roa"

def get_answer(context, question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Puedes usar "gpt-3.5-turbo" o "gpt-4"
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions about the university regulations."},
                {"role": "user", "content": f"Context: {context}"},
                {"role": "user", "content": f"Question: {question}"}
            ],
            max_tokens=500,
            temperature=0.7,
            top_p=0.9  # Ajustar la probabilidad para un mejor control de diversidad
        )
        answer = response['choices'][0]['message']['content'].strip()
        return answer
    except Exception as e:
        return f"Error al obtener la respuesta: {str(e)}"
