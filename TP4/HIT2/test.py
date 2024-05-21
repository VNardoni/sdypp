import json
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='34.23.44.122'))
channel = connection.channel()
channel.queue_declare(queue="prueba", durable=True)

channel.basic_publish(exchange='',
    routing_key="prueba",
    body="HOLA",
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent
    ))

print("[*] Enviado")
connection.close()