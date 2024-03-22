# HIT1 

Elabore un código de servidor TCP para B que espere el saludo de A y lo responda.
Elabore un código de cliente TCP para A que se conecte con B y lo salude.

> [!IMPORTANT]
> DESDE EL CLIENTE.

1. HACEMOS BUILD DE LA IMAGEN 'HIT' 

    - Pararse en ../TP1/HIT1

```
docker build . -t hit1 -f dockerfiles/hit1.dockerfile
```

2. COLOCAMOS EL TAG A LA IMAGEN 'hit1' 

```
docker tag hit1 vnardoni/hit1
```

3. LOGIN 

```
docker login
```

4. HACEMOS PUSH DE LA IMAGEN 

```
docker push vnardoni/hit1
```


> [!IMPORTANT]
> DESDE LA VM.

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
sudo docker pull vnardoni/hit1
```

4. HACEMOS RUN A LA IMAGEN 

```
sudo docker run --name hit1 --rm -p 8080:8080 vnardoni/hit1
```