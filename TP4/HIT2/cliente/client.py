from flask import request
import requests

url = 'http://127.0.0.1:5000/filtrarImagen'
file_path = 'imagen.jpg'

with open(file_path, 'rb') as img:
    files = {'file': img}
    data = {'n': 10}
    response = requests.post(url, files=files, data=data)
    
    response = request.json()
    

    if response.status_code == 200:
        with open('imagen_sobel.jpg', 'wb') as f:
            f.write(response.content)
        print("Imagen recibida y guardada como 'imagen_sobel.jpg'")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
