FROM python:3.13.0a5-alpine3.19
RUN mkdir -p usr/local/src/pythonapp
COPY ./registro_de_contactos.py /usr/local/src/pythonapp/registro_de_contactos.py

ENTRYPOINT ["python3", "usr/local/src/pythonapp/registro_de_contactos.py"]
