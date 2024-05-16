import socket
import threading
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
# VARIABLES

host = '0.0.0.0'
port = 8120
port_status = 8121

status = True

#Creamos la ruta
class StatusHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/status':
            #Devuelvo un codigo 200 y un mensaje diciendo que el server funciona
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            status_json = json.dumps({
                "key":"h2",
                "status": "Servidor en funcionamiento"})
            self.wfile.write(status_json.encode())
        else:
            #Si es otro path dice que en endpoint no existe(404)
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("Endpoint no encontrado".encode())
        

def statusRun(server_class=HTTPServer, handler_class=StatusHandler):
    #Crea el socket, y deja corriendo /status
    server_address = (host, port_status)
    httpd = server_class(server_address, handler_class)
    print("Status corriendo!")
    while status:
        httpd.serve_forever() #Maneja solicitudes


def run_main_server():
    server_socket = socket.socket()

    # Asigna la dirección y puerto al socket
    print(f"== Iniciando servidor en {host} puerto {port} ==")
    print("")
    server_socket.bind((host,port))

    # Escucha por conexiones entrantes

    server_socket.listen(1)


    # Espera por una conexión
    print("- ESPERANDO UNA CONEXION -")
    client_socket, addr = server_socket.accept()


    print(f"[CONEXION ESTABLECIDA] {addr}")

    respuesta = client_socket.recv(1024).decode()
    print(f"[CLIENTE] - {respuesta}")

    client_socket.send("Te saludo desde el servidor".encode())

    server_socket.close()


if __name__ == "__main__":
    # Inicia el servidor de estado en un hilo separado
    status_thread = threading.Thread(target=statusRun)
    status_thread.start()

    # Ejecuta el servidor principal
    run_main_server()