import requests

url = 'http://127.0.0.1:5000/filtrarImagen'
file_path = 'imagen.jpg'

with open(file_path, 'rb') as img:
    files = {'file': img}
    response = requests.post(url, files=files)

print(response.json())
