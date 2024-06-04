import cv2
import numpy as np
from flask import Flask, jsonify, request, send_file
import pika
import redis
import uuid
import json
from google.cloud import storage

queueName   = 'colaSobel'
hostRabbit  = 'rabbit-mq'
hostRedis   = 'redis'
portRedis   = '6379'
cantidadFragmentos = 10
url = "http://34.74.70.187:5000/"
PORT_HOST = 5000
bucketName = "bucket_imagenes_sdypp"


app = Flask(__name__)
# Configura la carpeta donde se guardarán las imágenes
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # Asegúrate de que la carpeta de subida exista
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)



def splitImage(image, n):
    height, width = image.shape[:2]
    segment_width = width // n
    segments = []
    for j in range(n):
        start_x = j * segment_width
        end_x = start_x + segment_width
        segment = image[:, start_x:end_x]  # Tomamos todas las filas de la imagen
        segments.append(segment)
    return segments

def combine_segments(segments, n):
    # Obtener la forma de un segmento para determinar la altura y el ancho de la imagen resultante
    segment_shape = segments[0].shape
    segment_height, segment_width = segment_shape[:2]
    # Calcular el shape de la imagen resultante
    result_height = segment_height
    result_width = segment_width * n
    # Crear la imagen resultante inicializando una matriz de ceros con el shape calculado
    result = np.zeros((result_height, result_width), dtype=np.uint8)
    # Combinar los segmentos en la imagen resultante
    for i in range(n):
        start_x = i * segment_width
        end_x = start_x + segment_width
        result[:, start_x:end_x] = segments[i] 
    #Convierto a imagen
    cv2.imwrite('imagen_sobel.jpg', result)

def encolar(idImagen, listaFragmentos):
    fragmentID = 0

    # Conexion a a RabbitMQ

    connection = pika.BlockingConnection(pika.ConnectionParameters(hostRabbit))
    channel = connection.channel()
    

    # Creamos la cola si no esta creada

    channel.queue_declare(queue=queueName)

    # Armo un JSON por cada Fragmento y lo encolo
    
    for fragmento in listaFragmentos:
        fragmentID += 1
        data = {
            "idImage": idImagen,
            "idFragment": fragmentID,
            "fragment": fragmento.tolist(),
        }
        json_data = json.dumps(data)

        channel.basic_publish(exchange='',
                        routing_key=queueName,
                        body=json_data)

        print(f"[x] IMAGEN: {idImagen} | Segmento {fragmentID} enviado")
        
    print("-----------------------")
    print(f"[*] Todos los fragmentos de la imagen {idImagen} se enviaron")
    
    
        

def generarID():
    return str(uuid.uuid4())

def redisConnect():
    client = redis.Redis(host = hostRedis, port = portRedis, db = 0)
    return client

def descargar_imagen(bucket_name, nombre_remoto, destino_local):
    # Crear el cliente de Google Cloud Storage
    storage_client = storage.Client()
    # Obtener el bucket
    bucket = storage_client.bucket(bucket_name)
    # Obtener el blob (archivo) especificado por nombre_remoto
    blob = bucket.blob(nombre_remoto)
    # Descargar el blob a un archivo local
    blob.download_to_filename(destino_local)
    print(f"Imagen {nombre_remoto} descargada a {destino_local}")


@app.route('/sobel', methods=['POST'])
def recibirImagen():

    cantidadFragmentos = request.form.get('n', type=int)

    # COMPRUEBA IMAGEN
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    # Obtén el archivo adjunto de la imagen
    file = request.files['file']

    # Lee los datos binarios de la imagen
    image_data = file.read()

    # Convierte los datos binarios en una matriz numpy
    nparr = np.frombuffer(image_data, np.uint8)

    # Decodifica la imagen de la matriz numpy
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Verifica si la imagen se ha cargado correctamente
    if image is None:
        return "Bad request: error al procesar la imagen", 400

    # ASIGNARLE ID A LA IMAGEN
    idImagen = generarID()

    # SPLITEAR LA IMAGEN
    listaFragmentos = splitImage(image, cantidadFragmentos)
    encolar(idImagen, listaFragmentos)

    # CONEXION A REDIS
    cliente = redisConnect()
    
    # ENVIAR AL REDIS ID IMAGEN | N (CANTIDAD DE FRAGMENTOS QUE DIVIDE) | ESTADO
    cliente.hset(idImagen, mapping={
        'FragmentosTotales': cantidadFragmentos,
        'Estado': 'PENDIENTE'
    })

    return jsonify({'OK': "Imagen recibida", 'ID': idImagen}), 200

# Endpoint que recibe ID de la imagen y recupera todos los fragmentos del bucket y las junta si ya esta lista
@app.route("/getImagenFiltrada", methods=["POST"])
def getImagenFiltrada():
    data = request.json
    idImagen = data["idImagen"]
    cliente = redisConnect()
    #Recuperamos el idImagen de redis
    resultado = cliente.hget(idImagen)
    if resultado:
        resultado = resultado.decode("utf-8")
        if resultado.get("Estado") == "PENDIENTE":
            return "La imagen no esta lista", 202
        else:
            nroFragmentos = resultado.get("FragmentosTotales")
            fragmentos = []
            #Cada fragmento se representa por "{idImagen}_{idFragmento}.jpg"
            for i in range(1 , nroFragmentos + 1):
                nombre_blob = (f'{idImagen}_{i}')
                #Descargo del bucket
                descargar_imagen(bucketName, nombre_blob, nombre_blob)
                #Convierto imagen a array
                fragmento = cv2.imread(nombre_blob)
                #Guardo en lista con todos los fragmentos para combinar
                fragmentos.append(fragmento)
            combine_segments(fragmentos, nroFragmentos)
            return send_file('imagen_sobel.jpg', mimetype='image/jpg')
    else:
        return "No se encontro la imagen", 404
            

# @app.route('/filtrarImagen', methods=['POST'])
# def filtrarImagen():
#     segmentos_filtrados = []
#     url = "http://34.74.195.104:5000/sobel"
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part"}), 400
#     file = request.files['file']
#     N = request.form.get('n', type=int)
#     if file:
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)
#         image = cv2.imread('uploads/imagen.jpg')
#         segmentos = divide_image(image, N)
#         jsons = armar_json(segmentos)
#         for segmento in jsons:
#             response = requests.post(url=url, json=segmento)
#             if response.status_code == 200:
#                 segmentData = response.json()
#                 segmentos_filtrados.append(segmentData)
#                 if segmentData["last_id"]:
#                     segmentos_ordenados = sorted(segmentos_filtrados, key=lambda x: x['segment_id']) # Ordeno los segmentos por ID
#                     segmentos = []
#                     for segmento in segmentos_ordenados: # Filtro por segmento
#                         s = np.array(segmento["segment"])
#                         segmentos.append(s) 
#                     combine_segments(segmentos, N)
#         return send_file('imagen_sobel.jpg', mimetype='image/jpg')
    

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=PORT_HOST)