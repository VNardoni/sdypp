FROM python:3

WORKDIR /pythonapp

RUN pip install flask requests docker

ADD server/server.py /pythonapp/server.py

EXPOSE 8210

ENTRYPOINT ["python3", "server.py"]
