from flask import Flask, request, jsonify

app = Flask(__name__)

<<<<<<< HEAD:TP2/HIT1/tarea_remota.py
=======
# ENDPOINT TAREA REMOTA
>>>>>>> 85d1d781c4433012b4418fcdc7d95469d0e6485f:TP2/HIT1/tarea_remota/tarea_remota.py
@app.route('/ejecutarTarea', methods=['POST'])
def ejecutar_tarea():
    tarea = request.get_json()
    resultado = procesar_tarea(tarea)
    resultado = jsonify(resultado)
    print(resultado)
    return (resultado)

def procesar_tarea(tarea):
    # PROCESO DE LA TAREA
<<<<<<< HEAD:TP2/HIT1/tarea_remota.py
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
=======
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
    
    data = {'resultado': resultado}     
    return jsonify(data)
>>>>>>> 85d1d781c4433012b4418fcdc7d95469d0e6485f:TP2/HIT1/tarea_remota/tarea_remota.py

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
<<<<<<< HEAD:TP2/HIT1/tarea_remota.py
    app.run(host='0.0.0.0', port=5000)
=======
    app.run(debug=True, port=5000, host="0.0.0.0")
>>>>>>> 85d1d781c4433012b4418fcdc7d95469d0e6485f:TP2/HIT1/tarea_remota/tarea_remota.py
