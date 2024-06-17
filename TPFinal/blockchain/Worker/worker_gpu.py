import pika
import requests
from ..Minero import minero_gpu
import json
import time

#Enviar el resultado al coordinador para verificar que el resultado es correcto
def enviar_resultado(data):
    url = "http://localhost:5000/tarea_worker"
    try:
        response = requests.post(url, json=data)
        print("Resolucion enviada al Coordinador!")
    except Exception as e:
        print("Fallo al enviar el post:", e)

# #Minero: Encargado de realizar el desafio
def minero(ch, method, properties, body):
    data = json.loads(body)
    print(f"Bloque {data} recibido")

    tiempo_inicial = time.time()
    print("Minero comenzado!")
    resultado = minero_gpu.ejecutar_minero(1, data["max_random"], data["prefix"], data["base_string_chain"])
    
    resultado = json.loads(resultado)
    data["hash"] = resultado['hash_md5_result']
    data["numero"] = resultado["numero"]

    enviar_resultado(data)
    #Confirmo con un ACK que lo resolvi
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"Resultado encontrado y enviado con el ID Bloque {data['id']}")

#Conexion con rabbit al topico y comienza a ser consumidor
def main():
    exchangeBlock = 'ExchangeBlock'
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()
    channel.exchange_declare(exchange=exchangeBlock, exchange_type='topic', durable=True)
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=exchangeBlock, queue=queue_name, routing_key='blocks')
    channel.basic_consume(queue=queue_name, on_message_callback=minero, auto_ack=False)
    print('Esperando mensajes. Para salir pulse CTRL+C')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        connection.close()
        print("Conexion cerrada")

if __name__ == '__main__':
    main()