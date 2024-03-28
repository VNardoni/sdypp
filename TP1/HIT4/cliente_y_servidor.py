import socket
import threading
import sys
import time

def server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(1)
    print(f"Servidor escuchando en {ip}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexión establecida desde {client_address}")

        data = client_socket.recv(1024).decode()
        print(f"Mensaje recibido: {data}")

        response = "Hola, soy el servidor. ¿Cómo estás?"
        client_socket.sendall(response.encode())
        client_socket.close()
        break

    time.sleep(1)
    server_socket.close()
    print("Conexión cerrada por el servidor")

def client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    saludoCliente= "Hola, soy el cliente. ¿Cómo estás?"
    client_socket.sendall(saludoCliente.encode())
    

    data = client_socket.recv(1024).decode()
    print(f"Respuesta del servidor: {data}")

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