import socket

client_socket = socket.socket()

client_socket.connect(('34.73.239.114',8080))

client_socket.send("Hola desde el cliente".encode())

respuesta = client_socket.recv(1024).decode()

print(respuesta)

client_socket.close()