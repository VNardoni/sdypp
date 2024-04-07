from flask import Flask, request, jsonify
import requests
import docker

app = Flask(__name__)


@app.route('/getRemoteTask', methods=['GET', 'POST'])
def get_remote_task():
    if request.method == 'POST':
        tarea = request.json
        print(tarea)
        resultado_tarea = ejecutar_tarea_remota(tarea)
        return jsonify(resultado_tarea)
    else:
        return 'Método no permitido', 405

def ejecutar_tarea_remota(tarea):
    # COMUNICACION CON LA TAREA REMOTA
    response = requests.post('http://localhost:5001/ejecutarTarea', json=tarea)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
