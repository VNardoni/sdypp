import json
import signal
import socket
import sys
import threading


def handle_signal(signum, frame):
    print("Deteniendo servidor...")
    sys.exit(0)

lista_clientes = {"clientes": []}
corriendo = True
signal.signal(signal.SIGINT, handle_signal)

def manejar_cliente(client_address, client_socket):
    print(f"Conexión establecida desde {client_address[0]}:{client_address[1]}")

    lista_clientes["clientes"].append({
        "IP": client_address[0],
        "puerto": client_address[1]
    })
    
    # Serializar datos de respuesta
    respuesta = json.dumps(lista_clientes)
    
    client_socket.sendall(respuesta.encode())
    client_socket.close()


def server(server_ip, server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(10)
    print(f"Servidor escuchando en {server_ip}:{server_port}. Presione Ctrl + C para salir.")
    while corriendo:
        client_socket, client_address = server_socket.accept()
        hilo_cliente = threading.Thread(target=manejar_cliente, args=(client_address, client_socket))
        hilo_cliente.start()

def main():
    if len(sys.argv) != 3:
        print("Debe ingresar los siguientes parametros <server_ip> <server_port>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    server(server_ip, server_port)

if __name__ == "__main__":
    main()