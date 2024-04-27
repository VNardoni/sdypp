from flask import Flask, request, jsonify

app = Flask(__name__)

# ENDPOINT TAREA REMOTA
@app.route('/ejecutarTarea', methods=['POST'])
def ejecutar_tarea():
    tarea = request.json
    resultado = procesar_tarea(tarea)
    return resultado

def procesar_tarea(tarea):
    # PROCESO DE LA TAREA
    match tarea["operacion"].lower():
        case ">":
            resultado = tarea['parametro1'] > tarea['parametro2']
        case "<":
            resultado = tarea['parametro1'] < tarea['parametro2'] 
        case "=":
            resultado = tarea['parametro1'] == tarea['parametro2']
        case "!=":
            resultado = tarea['parametro1'] != tarea['parametro2']
        case _:
            resultado = "Operacion no valida"
    
    if resultado:
        resultado = "Es Verdadero :)"
    else:
        resultado = "Es Falso :("
    
    data = {'resultado': resultado}     
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")