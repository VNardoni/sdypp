import time
from flask import Flask, request, jsonify
import requests
import docker

app = Flask(__name__)

# ENDPOINT TAREA REMOTA DESDE SERVIDOR
@app.route('/getRemoteTask', methods=['GET'])
def get_remote_task():
    if request.method == 'GET':
        tarea = request.json
        ip_contenedor = levantarContenedor(tarea["imagen"])
        resultado_tarea = ejecutar_tarea_remota(tarea, ip_contenedor)
        return jsonify(resultado_tarea)
    else:
        return 'Método no permitido', 405

def ejecutar_tarea_remota(tarea, ip_contenedor):
    # COMUNICACION CON LA TAREA REMOTA
    print("IP CONTENEDOR: " + ip_contenedor)
    if (ip_contenedor != ""):
        print("Conectando a tarea remota...")
        response = requests.get(f'http://{ip_contenedor}:5001/ejecutarTarea', json=tarea)
        return response.json()
    else:
        return {"mensaje": "Error al crear contenedor"}


def levantarContenedor(imagen):
    cliente = docker.from_env()
    imagen_docker = cliente.images.get(imagen)
    contenedor = cliente.containers.run(imagen_docker, auto_remove=True, detach=True, ports={'5001/tcp': 5001}, network_mode='bridge')
 
    # Esperar hasta que el contenedor esté en ejecución
    while True:
        try:
            contenedor.reload()
            print("Estado: " + contenedor.status)  
            if contenedor.status == "running":
                contenedor_info = cliente.containers.get(contenedor.id)
                contenedor_ip = contenedor_info.attrs['NetworkSettings']['IPAddress']
                break
        except docker.errors.NotFound:
            print("No se encontro el contenedor") 
        print("Reintentado...")
        time.sleep(2) 

    return contenedor_ip


if __name__ == '__main__':
    app.run(debug=True, port=5000)