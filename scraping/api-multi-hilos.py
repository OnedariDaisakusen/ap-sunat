from flask import Flask, jsonify, request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import jwt
import pandas as pd

from conectar_bd import insertar_proceso, obtenerUsuario, obtenerEstadoProceso, listaResultadosPorProceso, actualizar_proceso_estado
from scraping import iniciarProceso

app = Flask(__name__)
executor = ThreadPoolExecutor(1)  # Puedes ajustar el número de hilos según tus necesidades
app.config['SECRET_KEY'] = 'tu_clave_secreta'

def tarea_larga():
    # Simula una tarea que lleva mucho tiempo
    import time
    time.sleep(5)
    print("Tarea Completada")
    return "Tarea completada!"

def ejecutarTarea(documentos, id_proceso, id_usuario):
    print("Se inicio la tarea ===> ")

    proceso_dict = {
        "id_proceso": id_proceso,
        'estado':'PROCESANDO',
    }

    actualizar_proceso_estado(proceso_dict)
    
    iniciarProceso(documentos, id_proceso, id_usuario)
    return "Tarea completada!"

@app.route('/')
def index():
    return "¡Hola! Esta es una API multihilo."

@app.route('/tarea')
def ejecutar_tarea():
    # Ejecuta la tarea_larga en un hilo separado
    future = executor.submit(tarea_larga)
    return "Tarea en progreso. ID: {}".format(id(future))

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    usuario = obtenerUsuario(data)

    # if usuario and check_password_hash(usuario[2], data['password']):
    if usuario and usuario[6] == data['password']:
        token = generate_token(usuario[0])
        return jsonify({'mensaje': 'Inicio de sesión exitoso', 'id_usuario': usuario[0], 'token': token})
    else:
        return jsonify({'mensaje': 'Credenciales incorrectas'}), 401
 
def generate_token(user_id):
    expiration_time = datetime.utcnow() + timedelta(days=1)  # Token expira en 1 día
    payload = {'user_id': user_id, 'exp': expiration_time}
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token   

@app.route('/upload', methods=['POST'])
def upload_file():

    id_usuario = ""
    try:
        auth_header = request.headers.get('Authorization')

        # Verificar si se proporciona la cabecera de autorización y tiene el formato correcto
        if auth_header is None or 'Bearer ' not in auth_header:
            raise jwt.InvalidTokenError('Token no proporcionado en la cabecera')

        # Extraer el token
        token = auth_header.split('Bearer ')[1]

        # Decodificar el token
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        id_usuario = payload["user_id"]

    except jwt.ExpiredSignatureError:
        return jsonify({'mensaje': 'Token expirado'}), 401
    except jwt.InvalidTokenError as e:
        return jsonify({'mensaje': str(e)}), 401  

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

    except Exception as e:
        # Devuelve un mensaje de error si hay algún problema al leer el archivo
        return jsonify({'error': f'Error al leer el archivo Excel: {str(e)}'}), 500

    proceso_dict = {
        'fecha_finalizacion':None,
        'estado':'EN ESPERA',
        'registros_procesados':0,
        'registros_no_procesados':0,
        'id_usuario':id_usuario
    }

    id_proceso = insertar_proceso(proceso_dict)

    parametro1 = request.args.get('documentos', default=documentos)
    parametro2 = request.args.get('id_proceso', default=id_proceso)
    parametro3 = request.args.get('id_usuario', default=id_usuario)

    future = executor.submit(ejecutarTarea, parametro1, parametro2, parametro3)

    print("Tarea en progreso. ID: {}".format(id(future)))
    return jsonify({'mensaje': "El archivo se encuentra en proceso. Puede consultar el estado con el codigo del proceso",'codigo-proceso':id_proceso}), 200

@app.route('/obtenerEstadoProceso/<int:idProceso>', methods=['GET'])
def obtenerProceso(idProceso):

    try:
        auth_header = request.headers.get('Authorization')

        # Verificar si se proporciona la cabecera de autorización y tiene el formato correcto
        if auth_header is None or 'Bearer ' not in auth_header:
            raise jwt.InvalidTokenError('Token no proporcionado en la cabecera')

        # Extraer el token
        token = auth_header.split('Bearer ')[1]

        # Decodificar el token
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])

    except jwt.ExpiredSignatureError:
        return jsonify({'mensaje': 'Token expirado'}), 401
    except jwt.InvalidTokenError as e:
        return jsonify({'mensaje': str(e)}), 401
        
    return jsonify(obtenerEstadoProceso(idProceso))
   
@app.route('/obtenerResultadoProceso/<int:idProceso>', methods=['GET'])
def obtenerResultadoProceso(idProceso):
    try:
        auth_header = request.headers.get('Authorization')

        # Verificar si se proporciona la cabecera de autorización y tiene el formato correcto
        if auth_header is None or 'Bearer ' not in auth_header:
            raise jwt.InvalidTokenError('Token no proporcionado en la cabecera')

        # Extraer el token
        token = auth_header.split('Bearer ')[1]

        # Decodificar el token
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])

    except jwt.ExpiredSignatureError:
        return jsonify({'mensaje': 'Token expirado'}), 401
    except jwt.InvalidTokenError as e:
        return jsonify({'mensaje': str(e)}), 401
        
    return jsonify(listaResultadosPorProceso(idProceso))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
