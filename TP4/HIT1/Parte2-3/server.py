import json
import cv2
import numpy as np
import pika
from flask import Flask, request

queueName = "cola_sobel"
image = cv2.imread('imagen.jpg')
n = 10
PORT = 5000
segmentos_filtrados = []

app = Flask(__name__)


def divide_image(image, n):
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
    
    return result


def encolar(image_segments, queue):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queueName, durable=True)
    
    segment_id = 0
    lastID = False

    for segment in image_segments:
        segment_id += 1

        if segment_id == len(image_segments):
            lastID = True

        data = {
            "segment_id": segment_id,
            "segment": segment.tolist(),
            "last_id": lastID
        }

        json_data = json.dumps(data)
        channel.basic_publish(exchange='',
            routing_key=queueName,
            body=json_data,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            ))
        print(f"[x] Segmento {segment_id} enviado")
    print("-----------------------")
    print("[*] Lista enviada a la cola")
    connection.close()
    

@app.route('/juntarSobels', methods=['POST'])
def juntarSobels():
    global segmentos_filtrados
    data = request.json
    data["segment"] = np.array(data["segment"])
    segmentos_filtrados += [data]
            
    if (len(segmentos_filtrados) == n):
        segmentos_filtrados = sorted(segmentos_filtrados, key=lambda x: x['segment_id']) # Ordeno los segmentos por ID
        segmentos = []
        for segmento in segmentos_filtrados: # Filtro por segmento
            segmentos.append(segmento["segment"])    # segment , segment , segment
            
        sobel_combined = combine_segments(segmentos, n)
        cv2.imwrite('imagen_sobel.jpg', sobel_combined)
    return "OK", 200

image_segments = divide_image(image, n)
encolar(image_segments, queueName)

if __name__ == "__main__":
    app.run(port=PORT)
