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

server_socket.listen(1)


# Espera por una conexión
print("- ESPERANDO UNA CONEXION -")
client_socket, addr = server_socket.accept()


print(f"[CONEXION ESTABLECIDA] IP CLIENTE: {addr}")

respuesta = client_socket.recv(1024).decode()
print(respuesta)

client_socket.send("[SERVIDOR] Te saludo desde el servidor".encode())

server_socket.close()
 