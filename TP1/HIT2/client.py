import socket
import time 

IP = '34.73.239.114'
PORT = 8080


while True:
    try:
        client_socket = socket.socket()
        client_socket.connect((IP,PORT))

        client_socket.send("Hola desde el cliente".encode())

        respuesta = client_socket.recv(1024).decode()
        
        print(f"[SERVIDOR] - {respuesta}")
    except: 
        print("NO HAY NINGUNA CONEXION ABIERTA")
        time.sleep(5)

# client_socket.close()