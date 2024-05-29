import json
import os
import cv2
import numpy as np
import pika
import redis


queueName = 'colaSobel'
hostRabbit  = '35.196.254.97'
hostRedis   = '34.148.28.245'
portRedis   = '6379'



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

# MAIN

# CONECTARSE A LA COLA

def queueConnect():

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostRabbit))
    channel = connection.channel()

    channel.queue_declare(queue=queueName)


    # Funcion que se ejecuta cada vez que llega algo a la cola

    def callback(ch, method, properties, body):
        print(f" [x] Fragmento recibido")
        
        
        message_body = body.decode() #  data = {ID IMAGEN | ID FRAGMENTO | FRAGMENTO}
        fragmentData = json.loads(message_body)

        # Nos quedamos solamente con el segmento
        
        image = fragmentData["fragment"]
        idImage = fragmentData["idImage"]

        # Convertimos el segmento en nparray para aplicar el filtro
        
        image = np.array(image)
        
        cv2.imwrite(f'imagen_parte{fragmentData["idFragment"]}.jpg', image) 
        image = cv2.imread(f'imagen_parte{fragmentData["idFragment"]}.jpg')

        # Aplicamos filtro
        imagenSobel = sobel_filter(image)

        cv2.imwrite(f'imagen_parte{fragmentData["idFragment"]}.jpg', imagenSobel)
        print(f" [x] Sobel aplicado al segmento {fragmentData['idFragment']}")

        # Convertimos en tolist para enviar
        fragmentData["fragment"] = imagenSobel.tolist()

        json_data = json.dumps(fragmentData)
        
        os.remove(f'imagen_parte{fragmentData["idFragment"]}.jpg')

        # CONECTARSE AL REDIS

        cliente = redisConnect()

        # OBTENEMOS TOTAL DE FRAGMENTOS EN EL QUE FUE DIVIDIA
         
        getCantidadTotalFragmentos(cliente, idImage)




        ch.basic_ack(delivery_tag = method.delivery_tag)





# OBTENER LA CANTIDAD DE FRAGMENTOS TOTALES EN QUE DE DIVIDIOO EL IDIMAGEN
# COMPARAR SI EL FRAGMENTO RECIBIDO = FRAGMENTOS TOTALES
    # IF = ENTONCES CAMBIAR EL ESTADO DEL REDIS
    # SINO SEGUIR
# ENVIAR EL FRAGMENTO AL BUCKET
