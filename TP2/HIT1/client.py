import requests
import json

# DATOS A ENVIAR
parametros = { 
    "parametro1": 10,
    "parametro2": 20 
}



# ROST AL SERVIDOR
response = requests.post('http://localhost:5000/getRemoteTask', json=parametros)

# PROCESAR LA RESPUESTA DEL SERVIDOR
print("LLEGUE ACA")
print(response)
resultado = response.json()
print('Resultado de la tarea:', resultado)