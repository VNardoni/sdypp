# HIT3 

Modifique el código de B para que si el proceso A cierra la conexión (por ejemplo matando el proceso) siga funcionando.

## ARMADO Y USO DE LA IMAGEN 

> [!IMPORTANT]
> DESDE EL CLIENTE.

1. HACEMOS BUILD DE LA IMAGEN 'hit3' 

    - Pararse en ../TP1/HIT3

```
docker build . -t hit3 -f dockerfiles/hit3.dockerfile
```

2. COLOCAMOS EL TAG A LA IMAGEN 'hit3' 

```
docker tag hit2 vnardoni/hit3
```

3. LOGIN 

```
docker login
```

4. HACEMOS PUSH DE LA IMAGEN 

```
docker push vnardoni/hit3
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
sudo docker pull vnardoni/hit3
```

4. HACEMOS RUN A LA IMAGEN 

```
sudo docker run --name hit3 --rm -p 8080:8080 vnardoni/hit3
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

El cliente envia un mensaje al servidor y recibe la respuesta del mismo. Ambos mensajes se muentran en pantalla y se cierra la conexion del lado del cliente finalizando el socket. El servidor queda escuchando a posibles nuevas conexiones. Cuando volvemos a iniciar el cliente, se realizan los intercambios de mensajes y el cliente cierra su conexion.