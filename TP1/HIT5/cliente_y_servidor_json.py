import socket
import threading
import sys
import time
import json

def server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(1)
    print(f"== [SERVIDOR ESCUCHANDO]  {ip}:{port} ==")
    print("")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[CONEXION ESTABLECIDA] CLIENTE » {client_address}")
        print("")

        data = client_socket.recv(1024).decode()
       
        
        #deserializa el msj recibido
        saludo_recibido = json.loads(data)
        print(f"[CLIENTE] - {saludo_recibido}")

        datos_respuesta = {"mensaje": "Hola, soy el servidor. Como estas?"}
        
        # Serializar datos de respuesta
        respuesta = json.dumps(datos_respuesta)
        
        client_socket.sendall(respuesta.encode())
        client_socket.close()
        break

    time.sleep(1)
    server_socket.close()
    print("[CONEXION CERRADA POR EL SERVIDOR]")

def client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    # Datos a enviar como json
    datos_a_enviar = {"mensaje": "Hola, soy el cliente. Como estas?"}
    
    
     # Serializar datos
    saludo_json = json.dumps(datos_a_enviar)
    client_socket.sendall(saludo_json.encode())

    data = client_socket.recv(1024).decode()
    print(f"[SERVIDOR] - {data}")

    client_socket.close()

def main():
    if len(sys.argv) != 3:
        print("Debe ingresar los siguientes parametros <server_ip> <server_port>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    server_thread = threading.Thread(target=server, args=(server_ip, server_port))
    server_thread.start()

    client_thread = threading.Thread(target=client, args=(server_ip, server_port))
    client_thread.start()

if __name__ == "__main__":
    main()