# HIT4

Refactoriza el código de los programas A y B en un único programa, que funcione simultáneamente como cliente y servidor. Esto significa que al iniciar el programa C, se le deben proporcionar por parámetros la dirección IP y el puerto para escuchar saludos, así como la dirección IP y el puerto de otro nodo C. De esta manera, al tener dos instancias de C en ejecución, cada una configurada con los parámetros del otro, ambas se saludan mutuamente a través de cada canal de comunicación.

## ARMADO Y USO DE LA IMAGEN 

> [!IMPORTANT]
> DESDE EL CLIENTE.

1. HACEMOS BUILD DE LA IMAGEN 'hit4' 

    - Pararse en ../TP1/HIT4

```
docker build . -t hit4 -f dockerfiles/hit4.dockerfile
```

2. COLOCAMOS EL TAG A LA IMAGEN 'hit4' 

```
docker tag hit4 vnardoni/hit4
```

3. LOGIN 

```
docker login
```

4. HACEMOS PUSH DE LA IMAGEN 

```
docker push vnardoni/hit4
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
sudo docker pull vnardoni/hit4
```

4. HACEMOS RUN A LA IMAGEN 

```
sudo docker run --name hit4 --rm -p 8080:8080 vnardoni/hit4 localhost 8080
```

## FUNCIONAMIENTO

Se ejecuta el archivo 'cliente_y_servidor.py', pasandole como parametro IP PUERTO

```
python cliente_y_servidor.py localhost 8080
```

Al iniciar el programa se crea un hilo para iniciar el servidor el cual escuchara conexiones del cliente. El servidor recibira los parametros utilizados al iniciar el programa, los cuales indican la IP y PORT en el que escuchara. El cliente se ejecutara en otro hilo utilizando los parametros ingresados para conectarse al servidor. Ambos realizan el intercambio de mensajes finalizando la conexion.

