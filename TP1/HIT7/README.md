# HIT7

Modifique el programa C y D, de manera tal de implementar un “sistema de inscripciones”, esto es, se define una ventana de tiempo fija de 1 MIN, coordinada por D, y los nodos C deben registrarse para participar de esa ventana, cuando un nodo C se registra a las 11:28:34 en D, el registro se hace efectivo para la próxima ventana de tiempo que corresponde a las 11:29. Cuando se alcanza las 11:29:00 el nodo D cierra las inscripciones y todo nodo C que se registre será anotado para la ventana de las 11:30, los nodos C que consulten las inscripciones activas solo pueden ver las inscripciones de la ventana actual, es decir, los nodos C no saben a priori cuales son sus pares para la próxima ventana de tiempo, solo saben los que están activos actualmente. Recuerde almacenar las inscripciones en un archivo de texto con formato JSON. Esto facilitará el seguimiento ordenado de las ejecuciones y asegurará la verificación de los resultados esperados.

## ARMADO Y USO DE LA IMAGEN 

> [!IMPORTANT]
> DESDE EL CLIENTE.

1. HACEMOS BUILD DE LAS IMAGENES 'hit7server' y 'hit7cliente'

    - Pararse en ../TP1/HIT7

```
docker build . -t hit7server -f dockerfiles/hit7server.dockerfile
docker build . -t hit7liente -f dockerfiles/hit7cliente.dockerfile
```

2. COLOCAMOS EL TAG A LAS IMAGENES 'hit7server' y 'hit7cliente'

```
docker tag hit7server vnardoni/hit7server
docker tag hit7cliente vnardoni/hit7cliente
```

3. LOGIN 

```
docker login
```

4. HACEMOS PUSH DE LAS IMAGENES 

```
docker push vnardoni/hit7server
docker push vnardoni/hit7cliente
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
sudo docker pull vnardoni/hit7server
sudo docker pull vnardoni/hit7cliente

```

4. HACEMOS RUN A LA IMAGEN SERVIDOR

```
sudo docker run --name hit7server --network host --rm -p 8080:8080 vnardoni/hit7server localhost 8080
```

5. HACEMOS RUN A LA IMAGEN CLIENTE [Al ejecutar otro cliente debemos cambiar el parametro **name** por otro nombre *EJEMPLO hit7cliente2*]

```
sudo docker run --name hit7cliente --network host --rm -p 8080:8080 vnardoni/hit7cliente localhost 8080
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

Al levantar las imagenes docker del servidor y los **n** clientes le pasamos como parametro *--network host* para que utilicen la red de la Maquina Virtual. El servidor de *Registro de Contactos* quedara en escucha. Cuando un cliente se conecte sera registrado para la proxima ventana, el servidor recibira un mensaje en formato JSON obteniendo la IP y PORT del mismo, enviara la lista con las direcciones IP - PUERTO de clientes previamente conectados en su misma ventana. Por su parte, el cliente una vez recibida la lista con las IP y PORT de los otros N clientes, se conectara con cada uno de ellos para enviar un saludo a los clientes conectados en su ventana.
Al finalizar con todos los saludos, quedara en modo escucha para recibir los saludos de los futuros clientes que se conecten con el Registro de Contacto.
Al transcurrir lod 60 seg. por ventana, el registro actual de clientes es reemplazado por los clientes que se encuentran en el registro de la siguiente ventana.
