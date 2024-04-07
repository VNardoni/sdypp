import requests
import json

# DATOS A ENVIAR
parametros = { 
    "parametro1": 10,
    "parametro2": 20,
    "operacion": "suma"
}

# REQUEST AL SERVIDOR
response = requests.get('http://localhost:5000/getRemoteTask', json=parametros)

# PROCESAR LA RESPUESTA DEL SERVIDOR
resultado = response.json()
print('Resultado de la tarea:', resultado)