from flask import Flask, request, jsonify
import requests
import docker

app = Flask(__name__)

# ENDPOINT TAREA REMOTA DESDE SERVIDOR
@app.route('/getRemoteTask', methods=['GET', 'POST'])
def get_remote_task():
    if request.method == 'GET':
        tarea = request.json
        print(tarea)
        resultado_tarea = ejecutar_tarea_remota(tarea)
        return jsonify(resultado_tarea)
    else:
        return 'Método no permitido', 405

def ejecutar_tarea_remota(tarea):
    # COMUNICACION CON LA TAREA REMOTA
    response = requests.get('http://localhost:5001/ejecutarTarea', json=tarea)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    print("Servidor escuchando en el puerto 5000...")