# app.py
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from read_file import extract_text_from_pdf, create_vector_db
from model import get_answer
import os


app = Flask(__name__)
CORS(app)


# Verificar que la clave de API se ha cargado
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("No se proporcionó la clave de API. Verifique que el archivo .env contiene la clave OPENAI_API_KEY.")

# Cargar el reglamento y crear la base de datos vectorial
reglamento_path = os.path.join(os.path.dirname(__file__), '_reglamento_academico_regimen_estudiantil_2019.pdf')
documents = extract_text_from_pdf(reglamento_path)
vector_db = create_vector_db(documents, api_key)

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

        answer = get_answer(question, api_key)
        if not answer:
            return jsonify({'answer': 'No se encontró una respuesta adecuada'})
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
