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
credentialPath = "credentials.json"

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

def redisConnect():
    client = redis.Redis(host = hostRedis, port = portRedis, db = 0)
    return client

def bucketConnect(bucketName, credentialPath):
    bucketClient = storage.Client.from_service_account_json(credentialPath)
    bucket = bucketClient.bucket(bucketName)
    return bucket

def subirImagen(bucket,fragmentData,nombreFragmento):

    idFragment = fragmentData["idFragment"]
    idImage = fragmentData["idImage"]

    name =  (f'{idImage}_{idFragment}')

    # Crear un blob (objeto en el bucket) con el nombre deseado
    blob = bucket.blob(name)
    
    # Subir la imagen al blob
    blob.upload_from_filename(nombreFragmento)

    print(f"[x] {nombreFragmento} fue subido al bucket {bucketName} con el nombre {name}")

def getCantidadTotalFragmentos(cliente, idImage):
    resultado = cliente.hgetall(idImage)

    for key, value in resultado.items():
        if key.decode("utf-8") == 'FragmentosTotales':
            return value.decode("utf-8")
        

# Funcion que se ejecuta cada vez que llega algo a la cola

def callback(ch, method, properties, body):
    print(f"[x] Fragmento recibido")
    
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
    print("[x] [APLICANDO SOBEL] Segmento " + str(idFragment))
    imagenSobel = sobel_filter(image)

    cv2.imwrite(nombreFragmento, imagenSobel)
    print(f"[x] [SOBEL APLICADO] Segmento {fragmentData['idFragment']}")
    print("")

    # CONECTARSE AL REDIS

    cliente = redisConnect()
    print(f"[x] Conectado al servidor redist {cliente}")
    print("")
    # OBTENEMOS TOTAL DE FRAGMENTOS EN EL QUE FUE DIVIDIA

    totalFragmentos = getCantidadTotalFragmentos(cliente, idImage)

    # COMPARAR SI EL FRAGMENTO RECIBIDO = FRAGMENTOS TOTALES
    if int(idFragment) == int(totalFragmentos):
        print(f"[x] [ULTIMO FRAGMENTO] » CAMBIAR ESTADO")
        cliente.hset(idImage, 'Estado', 'LISTA') # (HASH, CAMPO, VALOR)
        print("[x] NUEVO ESTADO » LISTA")



    # ENVIAR EL FRAGMENTO AL BUCKET
    bucket = bucketConnect(bucketName,credentialPath)
    subirImagen(bucket,fragmentData,nombreFragmento)
   
    
    
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