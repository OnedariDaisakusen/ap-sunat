from flask import Flask, jsonify, request
import concurrent.futures
import queue
import threading
import pandas as pd
import sys
import signal
from scraping import iniciarProceso
from conectar_bd import insertar_proceso, obtenerUsuario
from datetime import datetime, timedelta
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta'

class HilosControllerCurrent:
    def __init__(self, numero_hilos):
        self.numero_hilos_maximos = numero_hilos
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.numero_hilos_maximos)
        self.cola_tareas = queue.Queue()
        self.hilos_en_ejecucion = 0  # Nuevo: Contador de hilos en ejecución

        # Iniciar el procesamiento de la cola en un hilo
        threading.Thread(target=self.iniciar_procesamiento_cola).start()

    def iniciar_procesamiento_cola(self):
        while True:
            tarea = self.cola_tareas.get()  # Bloquearse hasta que haya una tarea
            self.hilos_en_ejecucion += 1  # Nuevo: Incrementar el contador
            self.executor.submit(self.ejecutar_tarea, tarea)

    def ejecutar_tarea(self, tarea):
        try:
            tarea()
        finally:
            self.hilos_en_ejecucion -= 1  # Nuevo: Decrementar el contador después de la ejecución

    def obtener_hilos_en_ejecucion(self):
        # Nuevo: Devolver el valor actualizado del contador
        return self.hilos_en_ejecucion

    def ejecutar_hilo(self, documentos,idProceso, idUsuario):
        # Añadir la tarea a la cola
        def tarea():
            
            iniciarProceso(documentos, idProceso, idUsuario)
            print("Proceso Iniciado")

        self.cola_tareas.put(tarea)

        return "Petición recibida. La tarea se ha agregado a la cola."


@app.route('/api2/hilos-en-ejecucion')
def hilos_en_ejecucion():
    return jsonify({'hilos_en_ejecucion': controlador_hilos.obtener_hilos_en_ejecucion()})

@app.route('/api2/ejecutar-hilo')
def ejecutar_hilo():
    return jsonify({'mensaje': controlador_hilos.ejecutar_hilo()})

@app.route('/upload', methods=['POST'])
def upload_file():

    id_usuario = ""

    try:
        token = request.headers.get('Authorization').split('Bearer ')[1]
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        id_usuario = payload["user_id"]
    except jwt.ExpiredSignatureError:
        return jsonify({'mensaje': 'Token expirado'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'mensaje': 'Token inválido'}), 401    

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
        'estado':'PROCESANDO',
        'registros_procesados':0,
        'registros_no_procesados':0,
        'id_usuario':id_usuario
    }

    id_proceso = insertar_proceso(proceso_dict)
    controlador_hilos.ejecutar_hilo(documentos, id_proceso, id_usuario)

    return jsonify({'mensaje': "El archivo se encuentra en proceso"}), 200

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

@app.route('/pruebaToken', methods=['GET'])
def prueba_token():
    validarToken()



def validarToken():
    try:
        token = request.headers.get('Authorization').split('Bearer ')[1]
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify(logged_in_as=payload['user_id']), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'mensaje': 'Token expirado'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'mensaje': 'Token inválido'}), 401    

if __name__ == '__main__':
    controlador_hilos = HilosControllerCurrent(numero_hilos=5)

    def handler(signum, frame):
        print("Recibida señal de interrupción. Cerrando la aplicación.")
        sys.exit(0)

    # Manejar la señal de interrupción (Ctrl+C)
    signal.signal(signal.SIGINT, handler)

    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error durante la ejecución de la aplicación: {e}")
    finally:
        # Realizar cualquier limpieza necesaria antes de salir
        print("Saliendo de la aplicación.")