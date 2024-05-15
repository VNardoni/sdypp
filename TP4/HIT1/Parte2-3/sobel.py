import json
import cv2
import numpy as np
import pika, sys, os, time

import requests

queueName = 'cola_sobel'
headers = {'Content-Type': 'application/json'}
IP = "localhost"

# Conexion a la cola 

def queueConnect():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=queueName, durable=True)

    def callback(ch, method, properties, body):
        print(f" [x] Segmento recibido")
        message_body = body.decode() #  data = {"segment_id": segment_id, "segment": segment}
        segmentData = json.loads(message_body)
        image = segmentData["segment"]
        image = np.array(image)
        # Se convierte el array a imagen y luego nuevamente a array, sin esta conversion el filtro no funciona
        cv2.imwrite(f'imagen_parte{segmentData["segment_id"]}.jpg', image) 
        image = cv2.imread(f'imagen_parte{segmentData["segment_id"]}.jpg')
        imagenSobel = sobel_filter(image)
        cv2.imwrite(f'imagen_parte{segmentData["segment_id"]}.jpg', imagenSobel)
        print(f" [x] Sobel aplicado al segmento {segmentData["segment_id"]}")
        segmentData["segment"] = imagenSobel.tolist()
        json_data = json.dumps(segmentData)
        response = requests.post(f'http://{IP}:5000/juntarSobels', data=json_data, headers=headers)
        os.remove(f'imagen_parte{segmentData["segment_id"]}.jpg')
        ch.basic_ack(delivery_tag = method.delivery_tag)
    
    channel.basic_consume(queue=queueName, on_message_callback=callback)   

    print(' [*] Esperando por segmentos')
    channel.start_consuming() 


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


if __name__ == '__main__':
    try:
        queueConnect()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
            
# image = cv2.imread('imagen.jpg')
# sobel_image = sobel_filter(image)
# cv2.imwrite('imagen_sobel.jpg', sobel_image)