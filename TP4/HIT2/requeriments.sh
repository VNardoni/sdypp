#!/bin/bash

sudo apt update
sudo apt install python3
sudo apt install python3-pip -y
pip install opencv-python numpy
pip install pika
pip install Flask


#Docker
sudo apt install docker.io

# Esperar  que Docker esté cargado
sleep 10

# Clonar los contenedores
sudo docker pull lucasrueda01/worker-app

# Esperar  antes de ejecutar el contenedor
sleep 30

# Correr el contenedor
sudo docker run --rm --name servidor_sobel -p 5000:5000 lucasrueda01/worker-app