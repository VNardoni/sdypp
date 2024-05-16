import json
import time
from flask import Flask, request, jsonify
import requests
import docker

app = Flask(__name__)

# ENDPOINT TAREA REMOTA DESDE SERVIDOR
@app.route('/getRemoteTask', methods=['POST'])
def get_remote_task():
    if request.method != 'POST':
        return 'Método no permitido', 405
    
    #Levantar contenedor
    tarea = request.json
    imagen = tarea["imagen"]
    cliente = docker.from_env()
    cliente.images.pull(imagen)
    print(imagen)
    contenedor = cliente.containers.run(imagen, detach=True, ports={'5000/tcp': 5000})
    # Esperar hasta que el contenedor esté en ejecución
    while contenedor.status != "running":
        print("Estado: " + contenedor.status)  
        print("No se encontro el contenedor") 
        print("Reintentado...")
        time.sleep(1) 
        contenedor.reload()
        
    # COMUNICACION CON LA TAREA REMOTA
    headers = {'Content-Type': 'application/json'}
    IP = "34.73.239.114"
    print("Conectando a tarea remota...")
    tarea = json.dumps(tarea)
    resultado_tarea = requests.post(f'http://{IP}:5000/ejecutarTarea', data=tarea, headers=headers).json()
    
    contenedor.stop()
    contenedor.remove()
    
    return jsonify(resultado_tarea)

# ENDPOINT SERVER STATUS
@app.route(rule="/status", methods=["GET"])
def status():
    data = {
        "ESTADO DEL SERVICIO": "Funcionando"
    }
    print(data)
    return data


if __name__ == '__main__':
    app.run(debug=True, port=8210, host="0.0.0.0")