from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/ejecutarTarea', methods=['POST'])
def ejecutar_tarea():
    tarea = request.get_json()
    resultado = procesar_tarea(tarea)
    resultado = jsonify(resultado)
    print(resultado)
    return (resultado)

def procesar_tarea(tarea):
    # PROCESO DE LA TAREA
    print(tarea)
    operacion = tarea["operacion"].lower()

    if operacion == "suma":
        resultado = suma(tarea['parametro1'], tarea['parametro2'])
    elif operacion == "resta":
        resultado = resta(tarea['parametro1'], tarea['parametro2'])
    elif operacion == "multiplicacion":
        resultado = multiplicacion(tarea['parametro1'], tarea['parametro2'])
    elif operacion == "division":
        resultado = division(tarea['parametro1'], tarea['parametro2'])
    else:
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
    app.run(host='0.0.0.0', port=5000)