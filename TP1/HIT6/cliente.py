import socket
import sys
import threading

def enviar_saludo(ip,puerto):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, puerto))
    hostname = socket.gethostname()
    # Obtener la dirección IP asociada con el nombre de host
    ip_propia = socket.gethostbyname(hostname)
    client_socket.sendall("Hola soy el cliente:" +" "+ ip_propia  )



def client(ip_d ,puerto_d):
  
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip_d, puerto_d))
    
    lista_clientes = client_socket.recv(1024).decode()
    print(lista_clientes)

    client_socket.close()

    ##for cliente in lista_clientes:
    ##    threading.Thread(target=enviar_saludo, args=(cliente.IP, cliente.puerto)).start() 


def main():
    if len(sys.argv) != 3:
        print("Debe ingresar los siguientes parametros <server_ip> <server_port>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    client(server_ip, server_port)

if __name__ == "__main__":
    main()