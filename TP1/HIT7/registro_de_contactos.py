import json
import socket
import sys
import threading
import time

# Rutas de los archivos JSON para almacenar las inscripciones
archivo_actual = "inscripciones_actual.json"
archivo_siguiente_ventana = "inscripciones_siguiente_ventana.json"
lista_clientes = {"clientes": []}
lista_clientes_siguiente_ventana = {"clientes": []}
corriendo = True

# Función para mover los registros de la siguiente ventana a la ventana actual
def mover_registros():
    global lista_clientes
    global lista_clientes_siguiente_ventana

    while corriendo:
        # Esperar 60 segundos antes de mover registros
        time.sleep(60)
      
        # Mover registros de la siguiente ventana a la ventana actual
        print(lista_clientes) 
        lista_clientes = lista_clientes_siguiente_ventana.copy()
        
        with open(archivo_actual, "w") as f:
            json.dump(lista_clientes_siguiente_ventana, f)
        lista_clientes_siguiente_ventana = {"clientes": []}
        print("Registros de la siguiente ventana movidos a la ventana actual.")
    
        # Guardar la lista de clientes de la siguiente ventana en el archivo JSON
        with open(archivo_siguiente_ventana, "w") as f:
            json.dump(lista_clientes_siguiente_ventana, f)


def manejar_cliente(client_address,client_socket,puertoEscucha):
    print(f"Conexión establecida desde {client_address[0]}:{puertoEscucha}")

    # Serializar datos de respuesta
    respuesta = json.dumps(lista_clientes)
    client_socket.sendall(respuesta.encode())
    client_socket.close()
    
    lista_clientes_siguiente_ventana["clientes"].append({
        "IP": client_address[0],
        "puerto": puertoEscucha
    })
     # Guardar la lista de clientes actual en el archivo JSON
    with open(archivo_siguiente_ventana, "w") as f:
        json.dump(lista_clientes_siguiente_ventana, f)

def server(server_ip, server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(10)
    print(f"Servidor escuchando en {server_ip}:{server_port}.")

    hilo_mover_registros = threading.Thread(target=mover_registros)
    hilo_mover_registros.start()
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
 # Crear archivos JSON si no existen
    with open(archivo_actual, "w") as f:
        json.dump(lista_clientes, f)

    with open(archivo_siguiente_ventana, "w") as f:
        json.dump(lista_clientes_siguiente_ventana, f)

    server(server_ip, server_port)

if __name__ == "__main__":
    main()