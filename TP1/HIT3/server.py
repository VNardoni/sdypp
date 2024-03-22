import socket
import time

# VARIABLES

host = '0.0.0.0'
port = 8080

server_socket = socket.socket()

# Asigna la dirección y puerto al socket
print(f"Iniciando servidor en {host} puerto {port}")
server_socket.bind((host,port))

# Escucha por conexiones entrantes
while True:
    server_socket.listen(1)


    # Espera por una conexión
    print("Esperando por una conexión...")
    client_socket, addr = server_socket.accept()


    print(f"Conexión establecida desde {addr}")

    respuesta = client_socket.recv(1024).decode()
    print(f"CLIENTE ENVIA: {respuesta}")

    client_socket.send("Te saludo desde el servidor".encode())

# server_socket.close()
 