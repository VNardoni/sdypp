# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Instala las dependencias necesarias directamente en el Dockerfile
RUN pip install --no-cache-dir opencv-python-headless==4.5.3.56 numpy==1.21.2 google-cloud-storage pika redis 

# Copia el contenido de la aplicación a la imagen del contenedor
COPY . .

# Expone el puerto en el que correrá la aplicación
EXPOSE 5000

# Comando para correr la aplicación
CMD ["python", "worker.py"]
