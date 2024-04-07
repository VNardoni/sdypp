import requests
import json

# Datos de la tarea a enviar
parametros = { 
    "parametro1": 10,
    "parametro2": 20 
}



# Realizar solicitud al servidor
response = requests.post('http://localhost:5000/getRemoteTask', json=parametros)

# Procesar la respuesta del servidor
print("LLEGUE ACA")
print(response)
resultado = response.json()
print('Resultado de la tarea:', resultado)