from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/ejecutarTarea', methods=['POST'])
def ejecutar_tarea():
    tarea = request.json
    resultado = procesar_tarea(tarea)
    return resultado

def procesar_tarea(tarea):
    # Aquí va la lógica para procesar la tarea
    # Por ejemplo, realizar un cálculo o manipulación de datos
    resultado = tarea['parametro1'] + tarea['parametro2']
    return {'resultado': resultado}

if __name__ == '__main__':
    app.run(debug=True, port=5001)