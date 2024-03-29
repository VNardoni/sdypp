import json
import socket
import sys
import threading

lista_clientes = {"clientes": []}
corriendo = True

def manejar_cliente(client_address,client_socket,puertoEscucha):
    print(f"Conexión establecida desde {client_address[0]}:{puertoEscucha}")

    # Serializar datos de respuesta
    respuesta = json.dumps(lista_clientes)
    client_socket.sendall(respuesta.encode())
    client_socket.close()
    
    lista_clientes["clientes"].append({
        "IP": client_address[0],
        "puerto": puertoEscucha
    })


def server(server_ip, server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(10)
    print(f"Servidor escuchando en {server_ip}:{server_port}.")
    while corriendo:
        client_socket, client_address = server_socket.accept()
        data = client_socket.recv(1024).decode()
        data2 = json.loads(data)
        puertoEscucha = data2['puerto']
        hilo_cliente = threading.Thread(target=manejar_cliente, args=(client_address, client_socket, puertoEscucha))
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