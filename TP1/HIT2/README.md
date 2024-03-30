# HIT2 

Revise el código de A para implementar una funcionalidad que permita la reconexión y el envío del saludo nuevamente en caso de que el proceso B cierre la conexión, como por ejemplo, al ser terminado abruptamente.

## ARMADO Y USO DE LA IMAGEN 

> [!IMPORTANT]
> DESDE EL CLIENTE.

1. HACEMOS BUILD DE LA IMAGEN 'hit2' 

    - Pararse en ../TP1/HIT2

```
docker build . -t hit2 -f dockerfiles/hit2.dockerfile
```

2. COLOCAMOS EL TAG A LA IMAGEN 'hit2' 

```
docker tag hit2 vnardoni/hit2
```

3. LOGIN 

```
docker login
```

4. HACEMOS PUSH DE LA IMAGEN 

```
docker push vnardoni/hit2
```


> [!IMPORTANT]
> DESDE LA VM.

 sudo apt update
 
1. INSTALAMOS DOCKER 

```
sudo apt install docker.io
```

2. HACEMOS LOGIN 

```
sudo docker login
```

3. HACEMOS EL PULL DE LA IMAGEN 

```
sudo docker pull vnardoni/hit2
```

4. HACEMOS RUN A LA IMAGEN 

```
sudo docker run --name hit2 --rm -p 8080:8080 vnardoni/hit2
```

## FUNCIONAMIENTO

Se ejecuta el servidor 'server.py', el cual queda en modo escucha esperando conexiones en el puerto 8080.

```
python server.py
```

Desde el lado del cliente se ejecuta 'client.py'. Conectandose al servidor a la direccion IP 34.73.239.114 y puerto 8080.

```
python client.py
```

El cliente envia un mensaje al servidor y recibe la respuesta del mismo. Ambos mensajes se muentran en pantalla y se cierra la conexion del lado del servidor finalizando el socket. El Cliente siguen intetando conectarse cada 5 segundos al servidor. Si este no contesta se muestra un mensaje indicando que no hay ninguna conexion abierta. Cuando vuelva a iniciar el servidor, el cliente se conecta nuevamente.