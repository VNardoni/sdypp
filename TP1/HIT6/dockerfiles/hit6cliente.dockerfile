FROM python:3.13.0a5-alpine3.19
RUN mkdir -p usr/local/src/pythonapp
COPY ./cliente.py /usr/local/src/pythonapp/cliente.py

ENTRYPOINT ["python3", "usr/local/src/pythonapp/cliente.py"]
