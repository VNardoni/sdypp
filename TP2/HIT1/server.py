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
    response = requests.get(f'http://{ip_contenedor}:5001/ejecutarTarea', json=tarea)
    return response.json()

def levantarContenedor(imagen):
    cliente = docker.from_env()
    contenedor = cliente.containers.run(imagen, detach=True, auto_remove=True, ports={'5001/tcp': 5001})
    # Obtener la IP del contenedor
    contenedor_info = cliente.containers.get(contenedor.id)
    contenedor_ip = contenedor_info.attrs['NetworkSettings']['IPAddress']
    return contenedor_ip


if __name__ == '__main__':
    app.run(debug=True, port=5000)
    print("Servidor escuchando en el puerto 5000...")