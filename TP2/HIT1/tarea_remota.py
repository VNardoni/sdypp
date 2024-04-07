from flask import Flask, request, jsonify

app = Flask(__name__)

# ENDPOINT TAREA REMOTA
@app.route('/ejecutarTarea', methods=['GET'])
def ejecutar_tarea():
    tarea = request.json
    resultado = procesar_tarea(tarea)
    return resultado

def procesar_tarea(tarea):
    # PROCESO DE LA TAREA
    match tarea["operacion"].lower():
        case "suma":
            resultado = suma(tarea['parametro1'], tarea['parametro2'])
        case "resta":
            resultado = resta(tarea['parametro1'], tarea['parametro2']) 
        case "multiplicacion":
            resultado = multiplicacion(tarea['parametro1'], tarea['parametro2'])
        case "division":
            resultado = division(tarea['parametro1'], tarea['parametro2'])
        case _:
            resultado = "Operacion no valida"
                   
    return {'resultado': resultado}

def suma(a, b):
    return a + b

def resta(a, b):
    return a - b

def multiplicacion(a, b):
    return a * b

def division(a , b):
    if b != 0:
        return a / b
    return "Error! Division por 0"


if __name__ == '__main__':
    app.run(debug=True, port=5001)
    print("Tarea remota escuchando en el puerto 5001...")