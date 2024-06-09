# app.py
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from read_file import extract_text_from_pdf
from model import get_answer
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# # Cargar variables de entorno desde el archivo .env
# load_dotenv()

# # Verificar que la clave de API se ha cargado
# if not os.getenv('OPENAI_API_KEY'):
#     raise ValueError("No se proporcionó la clave de API. Verifique que el archivo .env contiene la clave OPENAI_API_KEY.")

# Cargar el reglamento
reglamento_path = os.path.join(os.path.dirname(__file__), '_reglamento_academico_regimen_estudiantil_2019.pdf')
reglamento_text = extract_text_from_pdf(reglamento_path)

if not reglamento_text:
    raise ValueError("No se pudo extraer el texto del reglamento.")

# Dividir el reglamento en párrafos
reglamento_sections = reglamento_text.split('\n\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.json
        question = data.get('question')
        if not question:
            return jsonify({'error': 'No question provided'}), 400

        # Filtrar las secciones relevantes
        relevant_sections = [section for section in reglamento_sections if question.lower() in section.lower()]

        # Limitar el número de secciones a 3 para evitar exceder el límite de tokens
        relevant_text = '\n\n'.join(relevant_sections[:3])

        # Añadir un contexto adicional si es necesario
        additional_context = "Proporciona una respuesta detallada y completa a la pregunta basándote en el reglamento."
        combined_context = f"{additional_context}\n\n{relevant_text}"

        answer = get_answer(combined_context, question)
        if not answer:
            return jsonify({'answer': 'No se encontró una respuesta adecuada'})
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
