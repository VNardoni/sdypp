import json
import os
import cv2
import numpy as np
from flask import Flask, jsonify, request, send_file
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Configura la carpeta donde se guardarán las imágenes
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Asegúrate de que la carpeta de subida exista
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

PORT = 5000
jsons = []


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
    #Convierto a imagen
    cv2.imwrite('imagen_sobel.jpg', result)
    
def armar_json(image_segments):
    lastID = False
    jsons = []
    segment_id = 0
    for segment in image_segments:
        segment_id += 1
        if segment_id == len(image_segments):
            lastID = True
        data = {
            "segment_id": segment_id,
            "segment": segment.tolist(),
            "last_id": lastID
        }
        jsons.append(data)
    return jsons

@app.route('/filtrarImagen', methods=['POST'])
def filtrarImagen():
    segmentos_filtrados = []
    url = "http://34.74.195.104:5000/sobel"
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    N = request.form.get('n', type=int)
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        image = cv2.imread('uploads/imagen.jpg')
        segmentos = divide_image(image, N)
        jsons = armar_json(segmentos)
        for segmento in jsons:
            response = requests.post(url=url, json=segmento)
            if response.status_code == 200:
                segmentData = response.json()
                segmentos_filtrados.append(segmentData)
                if segmentData["last_id"]:
                    segmentos_ordenados = sorted(segmentos_filtrados, key=lambda x: x['segment_id']) # Ordeno los segmentos por ID
                    segmentos = []
                    for segmento in segmentos_ordenados: # Filtro por segmento
                        s = np.array(segmento["segment"])
                        segmentos.append(s) 
                    combine_segments(segmentos, N)
        return send_file('imagen_sobel.jpg', mimetype='image/jpg')


if __name__ == "__main__":
    app.run(port=PORT)