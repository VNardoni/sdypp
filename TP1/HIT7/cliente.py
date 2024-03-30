import socket
import sys
import threading
import json
import random

# GENERAMOS PUERTO ESCUCHA

def generar_puerto():
      return random.randint(1025,10000)
      

# SERVIDOR EN ESCUCHA

def server(puertoEscucha):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0",puertoEscucha))
    server_socket.listen(10)
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f" == CONEXION ESTABLECIDA DESDE: {client_address} ==")
        print("")

        data = client_socket.recv(1024).decode()
        print(f"[MENSAJE RECIBIDO] {data}")
        print("")

        client_socket.close()

# CLIENTE

def recibir_registro_contactos(server_ip, server_port,puertoEscucha):
    
    print(" == SOY UN NUEVO CLIENTE ==")
    print(f"[IP] {server_ip}")
    print(f"[PORT] {puertoEscucha}")
    print("")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    
    # Enviar la dirección IP y puerto propios al servidor de registro de contactos (D) 
    direccion_cliente = {"IP": server_ip, "puerto": puertoEscucha}  # Puerto aleatorio
    client_socket.sendall(json.dumps(direccion_cliente).encode())
    
    # Recibir la lista de clientes registrados (nodos C) del servidor de registro de contactos (D)
    lista_clientes = client_socket.recv(1024).decode()
    client_socket.close()
    
    return json.loads(lista_clientes)["clientes"]

def saludar_a_contactos(registro_contactos, puertoEscucha):
    try:
        for cliente in registro_contactos:
            ip= cliente["IP"]
            puerto=cliente["puerto"]
            saludo = {
                "mensaje": "Hola, como estas?",
                "ip": ip,
                "puerto": puertoEscucha}
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip, puerto))
            client_socket.sendall(json.dumps(saludo).encode())
            print(f"[ENVIANDO SALUDO] IP DESTINO: {ip} PUERTO DESTINO {puerto} ")
            client_socket.close()
  
    except Exception as e:
        print(f"Error al saludar a {ip}: {e}")
        print("Este nodo con "+ ip + " se encuentra fuera de servicio")

    finally:
        print("[TODOS LOS SALUDOS ENVIADOS]")
        print("============================")
        print("")

        
def main():
    if len(sys.argv) != 3:
        print("Debe ingresar los siguientes parametros <server_ip> <server_port>")
        sys.exit(1)

    # Generamos puerto de esucha
    puertoEscucha = generar_puerto()

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    server_thread = threading.Thread(target=server, args=(puertoEscucha,))
    server_thread.start()

    # Conectarse al servidor de registro de contactos (D) y obtener la lista de contactos (nodos C)
    registro_contactos = recibir_registro_contactos(server_ip, server_port,puertoEscucha)
    print("LISTA DE CLIENTES:")
    print(registro_contactos)
    
    # Saludar a cada nodo C registrado
    saludar_a_contactos(registro_contactos, puertoEscucha)

if __name__ == "__main__":
    main()
