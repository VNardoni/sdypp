import socket
import time 

IP = 'localhost'
PORT = 8080


while True:
    try:
        client_socket = socket.socket()
        client_socket.connect((IP,PORT))

        client_socket.send("[CLIENTE] Hola desde el cliente".encode())

        respuesta = client_socket.recv(1024).decode()
        
        print(respuesta)
    except: 
        print("NO HAY NINGUNA CONEXION ABIERTA")
        time.sleep(5)

# client_socket.close()