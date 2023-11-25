from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Verifica si se envió un archivo en la solicitud
    if 'file' not in request.files:
        return jsonify({'error': 'No se proporcionó ningún archivo'}), 400

    file = request.files['file']

    # Verifica si el archivo tiene un nombre y es un archivo Excel
    if file.filename == '' or not file.filename.endswith('.xlsx'):
        return jsonify({'error': 'Se espera un archivo Excel (.xlsx)'}), 400

    try:
        # Lee el archivo Excel utilizando pandas
        df = pd.read_excel(file)

        # Verifica si la columna "documento" está presente en el DataFrame
        if 'documento' not in df.columns:
            return jsonify({'error': 'La columna "documento" no está presente en el archivo Excel'}), 400

        # Guarda la columna "documento" en una variable
        documentos = df['documento'].tolist()

        # Devuelve la lista de documentos
        return jsonify({'documentos': documentos}), 200

    except Exception as e:
        # Devuelve un mensaje de error si hay algún problema al leer el archivo
        return jsonify({'error': f'Error al leer el archivo Excel: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
