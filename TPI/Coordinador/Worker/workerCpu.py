import pika
import json
import hashlib
import random
import requests
import time

hostRabbit = 'localhost'
queueNameTx = 'QueueTransactions'
exchangeBlock = 'ExchangeBlock'

def calcularSha256(texto):
    hash_sha256 = hashlib.sha256()
    hash_sha256.update(texto.encode('utf-8'))
    return hash_sha256.hexdigest()

def sendResult(data):
    url = "http://localhost:5000/solved_task"
    try:
        response = requests.post(url, json=data)
        print("Post response:", response.text)
    except requests.exceptions.RequestException as e:
        print("Failed to send POST request:", e)

#   block = {
#                "blockId": blockId,
 #               "transactions": listaTransactions,
  #              "prefijo": '000',
   #             "baseStringChain": "A3F8",
    #            "blockchainContent": "contenido",
     #           "numMaxRandom": maxRandom 
      #      }


def on_message_received(ch, method, properties, body):
    data = json.loads(body)
    print(f"Message {data} received")
    print('')

    encontrado = False
    intentos   = 0
    startTime  = time.time()

    print("## Iniciando Minero ##")

    while not encontrado:
        intentos = intentos + 1
        randomNumber = str(random.randint(0,data['numMaxRandom']))
        hashCalculado = calcularSha256(randomNumber + data['baseStringChain'] + data['blockchainContent'])
        if hashCalculado.startswith(data['prefijo']):
            encontrado = True
            processingTime = time.time() - startTime

            dataResult = {
                'blockId': data['blockId'],
                'processingTime': processingTime,
                'hash': hashCalculado,
                'result': randomNumber   
            }

            print(f"[x] Hash con el prefijo {data['prefijo']} encontrado")
            print(f"[x] HASH: {hashCalculado}")
            print('')
            sendResult(dataResult) 
    
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"Result found and posted for block ID {data['blockId']} in {processingTime:.2f} seconds in {intentos} intentos")
    print(f"Resultado: {randomNumber}")
    print('')

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=hostRabbit)
    )
    channel = connection.channel()
    channel.exchange_declare(exchange= exchangeBlock, exchange_type='topic', durable=True)
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange= exchangeBlock, queue=queue_name, routing_key='blocks')
    channel.basic_consume(queue=queue_name, on_message_callback=on_message_received, auto_ack=False)
    print('Waiting for messages. To exit press CTRL+C')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Consumption stopped by user.")
        connection.close()
        print("Connection closed.")

if __name__ == '__main__':
    main()