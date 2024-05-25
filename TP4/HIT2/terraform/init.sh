#!/bin/bash

sudo apt update -y

#Docker
sudo apt install docker.io -y

# Esperar que Docker esté cargado
sleep 15

# Clonar los contenedores
sudo docker pull lucasrueda01/worker-app

# Esperar  antes de ejecutar el contenedor
# sleep 30

# Correr el contenedor
sudo docker run --rm --name servidor_sobel -p 5000:5000 lucasrueda01/worker-app