import os
import cv2
from flask import Flask, jsonify, request
import numpy as np

PORT = 5000
app = Flask(__name__)

@app.route('/sobel', methods=['POST'])
def filtroSobel():
    try:
        print(f" [x] Segmento recibido")
        segmentData = request.json
        # Nos quedamos solamente con el segmento
        image = segmentData["segment"]
        # Convertimos el segmento en nparray para aplicar el filtro
        image = np.array(image)
        cv2.imwrite(f'imagen_parte{segmentData["segment_id"]}.jpg', image) 
        image = cv2.imread(f'imagen_parte{segmentData["segment_id"]}.jpg')
        # Aplicamos filtro
        imagenSobel = sobel_filter(image)
        cv2.imwrite(f'imagen_parte{segmentData["segment_id"]}.jpg', imagenSobel)
        print(f" [x] Sobel aplicado al segmento {segmentData['segment_id']}")
        # Convertimos en tolist para enviar
        segmentData["segment"] = imagenSobel.tolist()
        os.remove(f'imagen_parte{segmentData["segment_id"]}.jpg')
        
        return jsonify(segmentData), 200
    
    except Exception as e:
        print(f" [!] Error al procesar el segmento: {e}")
        return jsonify({"error": str(e)}), 500



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


if __name__ == "__main__":
    app.run(port=PORT)