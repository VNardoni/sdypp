# HIT6

Cree un programa D, el cual, actuará como un “Registro de contactos”. Para ello, en un array en ram, inicialmente vacío, este nodo D llevará un registro de los programas C que estén en ejecución.

Modifique el programa C de manera tal que reciba por parámetros únicamente la ip y el puerto del programa D. C debe iniciar la escucha en un puerto aleatorio y debe comunicarse con D para informarle su ip y su puerto aleatorio donde está escuchando. D le debe responder con las ips y puertos de los otros nodos C que estén corriendo, haga que C se conecte a cada uno de ellos y envíe el saludo.

Es decir, el objetivo de este HIT es incorporar un nuevo tipo de nodo (D) que actúe como registro de contactos para que al iniciar cada nodo C no tenga que indicar las ips de sus pares. Esto debe funcionar con múltiples instancias de C, no solo con 2.

## ARMADO Y USO DE LA IMAGEN 

> [!IMPORTANT]
> DESDE EL CLIENTE.

1. HACEMOS BUILD DE LAS IMAGENES 'hit6server' y 'hit6cliente'

    - Pararse en ../TP1/HIT6

```
docker build . -t hit6server -f dockerfiles/hit6server.dockerfile
docker build . -t hit6liente -f dockerfiles/hit6cliente.dockerfile
```

2. COLOCAMOS EL TAG A LAS IMAGENES 'hit6server' y 'hit6cliente'

```
docker tag hit6server vnardoni/hit6server
docker tag hit6cliente vnardoni/hit6cliente
```

3. LOGIN 

```
docker login
```

4. HACEMOS PUSH DE LAs IMAGENES 

```
docker push vnardoni/hit6server
docker push vnardoni/hit6cliente
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
sudo docker pull vnardoni/hit6server
sudo docker pull vnardoni/hit6cliente

```

4. HACEMOS RUN A LA IMAGEN SERVIDOR

```
sudo docker run --name hit6server --network host --rm -p 8080:8080 vnardoni/hit6server localhost 8080
```

5. HACEMOS RUN A LA IMAGEN CLIENTE [Al ejecutar otro cliente debemos cambiar el parametro **name** por otro nombre *EJEMPLO hit6cliente2*]

```
sudo docker run --name hit6cliente --network host --rm -p 8080:8080 vnardoni/hit6cliente localhost 8080
```


## FUNCIONAMIENTO

Se ejecuta el archivo 'registro_de_contactos.py', pasandole como parametro IP PUERTO

```
python registro_de_contactos.py localhost 8080
```

Se ejecutan los N clientes con el archivo 'cliente.py', pasandole como parametro IP PUERTO

```
python cliente.py localhost 8080
```

Al levantar las imagenes docker del servidor y los **n** clientes le pasamos como parametro *--network host* para que utilicen la red de la Maquina Virtual. El servidor de *Registro de Contactos* quedara en escucha. Cuando un cliente se conecte, el servidor recibira un mensaje en formato JSON obteniendo la IP y PORT del mismo, enviara la lista con las direcciones IP - PUERTO de clientes previamente conectados y guardara en ella el mensaje que recibio. Por su parte, el cliente una vez recibida la lista con las IP y PORT de los otros N clientes, se conectara con cada uno de ellos para enviar un saludo. Al finalizar con todos los saludos, quedara en modo escucha para recibir los saludos de los futuros clientes que se conecten con el Registro de Contacto.