import sys
import requests
import json


if (len(sys.argv) != 5):
    print("Se requieren los siguientes argumentos: <nombre_imagen> <parametro1> <operacion> <parametro2>")
    sys.exit(1)

NOMBRE_IMAGEN = sys.argv[1]
IP = "34.73.239.114" #La IP de la VM es estatica, si cambia implementar un fix en el futuro
PORT = 8210

# DATOS A ENVIAR
parametros = { 
    "parametro1": int(sys.argv[2]),
    "parametro2": int(sys.argv[4]),
    "operacion": sys.argv[3],
    "imagen": NOMBRE_IMAGEN
}

parametros = json.dumps(parametros)
headers = {'Content-Type': 'application/json'}
# REQUEST AL SERVIDOR
response = requests.post(f'http://{IP}:{PORT}/getRemoteTask', data=parametros, headers=headers)

# PROCESAR LA RESPUESTA DEL SERVIDOR
if response.status_code == 200:
    resultado = response.json()
    print('Resultado de la tarea: ', resultado)
else:
    print("Error: ", response.status_code)