from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/ejecutarTarea', methods=['POST'])
def ejecutar_tarea():
    tarea = request.json
    resultado = procesar_tarea(tarea)
    return resultado

def procesar_tarea(tarea):
    # PROCESO DE LA TAREA
    resultado = tarea['parametro1'] + tarea['parametro2']
    return {'resultado': resultado}

if __name__ == '__main__':
    app.run(debug=True, port=5001)