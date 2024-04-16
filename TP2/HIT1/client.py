import requests
import json

# Datos de la tarea a enviar
parametros = { 
    "parametro1": 50,
    "parametro2": 25,
    "operacion": "multiplicacion"
}

headers = {'Content-Type': 'application/json'}
jsonParametros = json.dumps(parametros)

# Realizar solicitud al servidor
response = requests.post('http://localhost:8080/getRemoteTask', data=jsonParametros, headers=headers)

# Procesar la respuesta del servidor
print("LLEGUE ACA")
print(response)
resultado = response.json()
print('Resultado de la tarea:', resultado)