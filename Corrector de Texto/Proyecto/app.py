from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/corregir', methods=['POST'])
def corregir_ortografia():
    data = request.json
    texto_original = data.get('texto')

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Corrige los errores ortográficos en el siguiente texto:\n\n{texto_original}"}
            ],
            max_tokens=500,
            temperature=0.3
        )

        texto_corregido = response['choices'][0]['message']['content'].strip()

        if texto_corregido == texto_original:
            return jsonify({'corregido': texto_corregido, 'perfecto': True})
        else:
            return jsonify({'corregido': texto_corregido, 'perfecto': False})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
