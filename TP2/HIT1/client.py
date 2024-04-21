import sys
import requests
import json

<<<<<<< HEAD
# Datos de la tarea a enviar
=======

if (len(sys.argv) != 2):
    print("Se requiere como unico argumento el nombre de la imagen")
    sys.exit(1)

NOMBRE_IMAGEN = sys.argv[1]
IP = "34.73.239.114" #La IP de la VM es estatica, si cambia implementar un fix en el futuro
PORT = 8080

# DATOS A ENVIAR
>>>>>>> 85d1d781c4433012b4418fcdc7d95469d0e6485f
parametros = { 
    "parametro1": 50,
    "parametro2": 25,
    "operacion": "multiplicacion"
}

<<<<<<< HEAD
headers = {'Content-Type': 'application/json'}
jsonParametros = json.dumps(parametros)
=======
parametros = json.dumps(parametros)
headers = {'Content-Type': 'application/json'}
# REQUEST AL SERVIDOR
response = requests.post(f'http://{IP}:{PORT}/getRemoteTask', data=parametros, headers=headers)
>>>>>>> 85d1d781c4433012b4418fcdc7d95469d0e6485f

# Realizar solicitud al servidor
response = requests.post('http://localhost:8080/getRemoteTask', data=jsonParametros, headers=headers)

# Procesar la respuesta del servidor
print("LLEGUE ACA")
print(response)
resultado = response.json()
print('Resultado de la tarea:', resultado)