import requests
import json

NOMBRE_IMAGEN = "lucasrueda01/tarea_remota"

# DATOS A ENVIAR
parametros = { 
    "parametro1": 10,
    "parametro2": 20,
    "operacion": "suma",
    "imagen": NOMBRE_IMAGEN
}

# REQUEST AL SERVIDOR
response = requests.get('http://localhost:5000/getRemoteTask', json=parametros)

# PROCESAR LA RESPUESTA DEL SERVIDOR
if response.status_code == 200:
    resultado = response.json()
    print('Resultado de la tarea: ', resultado)
else:
    print("Error: ", response.status_code)