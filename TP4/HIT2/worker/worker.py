import json
import os
import cv2
import numpy as np
import pika
import redis
from google.cloud import storage


queueName = 'colaSobel'
hostRabbit  = 'localhost'
hostRedis   = 'localhost'
portRedis   = '6379'
bucketName = "bucket_imagenes_sdypp"


# def filtroSobel():
#     print(f" [x] Segmento recibido")
#     segmentData = request.json
#     # Nos quedamos solamente con el segmento
#     image = segmentData["segment"]
#     # Convertimos el segmento en nparray para aplicar el filtro
#     image = np.array(image)
#     cv2.imwrite(f'imagen_parte{segmentData["segment_id"]}.jpg', image) 
#     image = cv2.imread(f'imagen_parte{segmentData["segment_id"]}.jpg')
#     # Aplicamos filtro
#     imagenSobel = sobel_filter(image)
#     cv2.imwrite(f'imagen_parte{segmentData["segment_id"]}.jpg', imagenSobel)
#     print(f" [x] Sobel aplicado al segmento {segmentData['segment_id']}")
#     # Convertimos en tolist para enviar
#     segmentData["segment"] = imagenSobel.tolist()
#     os.remove(f'imagen_parte{segmentData["segment_id"]}.jpg')
        


# Aplica el filtro al segmento

def sobel_filter(image):
    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Aplicar el filtro Sobel en el eje x
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    # Aplicar el filtro Sobel en el eje y
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    # Combinar las magnitudes de gradiente en ambas direcciones
    sobel = cv2.magnitude(sobel_x, sobel_y)
    # Escalar los valores para visualizar mejor
    sobel = np.uint8(255 * sobel / np.max(sobel))

    return sobel

# CONEXION A REDIS

def redisConnect():
    client = redis.Redis(host = hostRedis, port = portRedis, db = 0)
    return client

def getCantidadTotalFragmentos(cliente, idImage):
    resultado = cliente.hgetall(idImage)

    for key, value in resultado.items():
        if key.decode("utf-8") == 'FragmentosTotales':
            return value.decode("utf-8")

def subir_imagen(bucket_name, imagen_local, nombre_remoto):
    # Crear el cliente de Google Cloud Storage
    storage_client = storage.Client()
    # Obtener el bucket
    bucket = storage_client.bucket(bucket_name)
    # Crear un blob (objeto en el bucket) con el nombre deseado
    blob = bucket.blob(nombre_remoto)
    # Subir la imagen al blob
    blob.upload_from_filename(imagen_local)
    print(f"Imagen {imagen_local} subida a {bucket_name}/{nombre_remoto}")

def bucketConnect(bucketName):



# Funcion que se ejecuta cada vez que llega algo a la cola

def callback(ch, method, properties, body):
    print(f" [x] Fragmento recibido")
    
    message_body = body.decode() #  data = {ID IMAGEN | ID FRAGMENTO | FRAGMENTO}
    fragmentData = json.loads(message_body)

    idFragment = fragmentData["idFragment"]
    image = fragmentData["fragment"]
    idImage = fragmentData["idImage"]

    # Convertimos el segmento en nparray para aplicar el filtro
    
    image = np.array(image)
    nombreFragmento = (f'{idImage}_{idFragment}.jpg')
    
    cv2.imwrite(nombreFragmento, image) 
    image = cv2.imread(nombreFragmento)
    
    # Aplicamos filtro
    print("Aplicando filtro al segmento " + str(idFragment))
    imagenSobel = sobel_filter(image)

    cv2.imwrite(nombreFragmento, imagenSobel)
    print(f" [x] Sobel aplicado al segmento {fragmentData['idFragment']}")

    # CONECTARSE AL REDIS

    cliente = redisConnect()

    # OBTENEMOS TOTAL DE FRAGMENTOS EN EL QUE FUE DIVIDIA

    totalFragmentos = getCantidadTotalFragmentos(cliente, idImage)

    # COMPARAR SI EL FRAGMENTO RECIBIDO = FRAGMENTOS TOTALES
    if idFragment == totalFragmentos:
        cliente.hset(idImage, 'Estado', 'Completada') # (HASH, CAMPO, VALOR)

    # ENVIAR EL FRAGMENTO AL BUCKET
    subir_imagen(bucketName, nombreFragmento, nombreFragmento)
    
    
    os.remove(nombreFragmento)
    ch.basic_ack(delivery_tag = method.delivery_tag)
    

# MAIN
# CONECTARSE A LA COLA
connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostRabbit))
channel = connection.channel()

channel.queue_declare(queue=queueName)

print(' [*] Esperando por segmentos')
channel.basic_consume(queue=queueName, on_message_callback=callback)
channel.start_consuming() 




