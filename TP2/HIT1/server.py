from flask import Flask, request, jsonify
import requests
import docker
import time

app = Flask(__name__)

@app.route('/getRemoteTask', methods=['GET', 'POST'])
def get_remote_task():
    if request.method == 'POST':
        tarea = request.get_json()
        print(tarea)

        #  Creo el cliente
        client = docker.from_env()

         # Le indico el nombre del docker de tarea_remota
        nombreImagen = "vnardoni/tarea_remota"

        # Hago pull de la image
        client.images.pull(nombreImagen)
        print("[IMAGEN DESCARGADA]")

        # Levanto el contenedor 
        id_container = client.containers.run(nombreImagen, detach=True, ports={'5000/tcp': 5000})
        container = client.containers.get(id_container.id)
        print("[CONTENEDOR CORRIENDO]")

        time.sleep(5)

        response = requests.post('http://localhost:5000/ejecutarTarea', json=tarea)
        print("[TAREA RECIBIDA CON EXITO]")

        container.stop()
        container.remove()
        print("[CONTENEDOR ELIMINADO]")
        return response.json()
    else:
        return 'Método no permitido', 405





def getIpContenedor (nombreContenedor, client, red):
    infoRed = client.networks.get(red).attrs
    return infoRed['Containers'][nombreContenedor]['IPv4Address']

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

