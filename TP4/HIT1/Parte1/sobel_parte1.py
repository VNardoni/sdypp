import cv2
import numpy as np
import sys

def aplicar_operador_sobel(imagen_path):
    try:
        # Cargar la imagen
        imagen = cv2.imread(imagen_path, cv2.IMREAD_GRAYSCALE)

        # Se aplica Sobel
        sobelx = cv2.Sobel(imagen, cv2.CV_64F, 1, 0, ksize=5)
        sobely = cv2.Sobel(imagen, cv2.CV_64F, 0, 1, ksize=5)

        # se combina las respuestas de Sobel en una sola imagen
        sobel_combinada = cv2.addWeighted(cv2.convertScaleAbs(sobelx), 0.5, cv2.convertScaleAbs(sobely), 0.5, 0)

        # Mostrar la imagen original y la filtrada
        cv2.imshow('Imagen Original', imagen)
        cv2.imshow('Imagen Filtrada', sobel_combinada)
        cv2.waitKey(0)

        # Guardar la imagen filtrada
        cv2.imwrite('imagen_filtrada.jpg', sobel_combinada)

        print("La imagen filtrada se guardo como 'imagen_filtrada.jpg'")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <ruta_de_la_imagen>")
    else:
        imagen_path = sys.argv[1]
        aplicar_operador_sobel(imagen_path)
