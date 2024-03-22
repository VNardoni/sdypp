# HIT1 

Elabore un código de servidor TCP para B que espere el saludo de A y lo responda.
Elabore un código de cliente TCP para A que se conecte con B y lo salude.


### DESDE EL CLIENTE

1. HACEMOS BUILD DE LA IMAGEN 'HIT' 


[!WARNING]

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

4. HACEMOS PUSH DE LA IMAGEN •

```
docker push vnardoni/hit1
```

==========================================================

# DESDE LA VM DE GCLOUD

• INSTALAMOS DOCKER • 

sudo apt install docker.io

• LOGIN •

sudo docker login

• HACEMOS EL PULL DE LA IMAGEN •

sudo docker pull vnardoni/hit1

• HACMOE RUN A LA IMAGEN •

sudo docker run --name hit1 --rm -p 8080:8080 vnardoni/hit1