FROM python:3

RUN pip install flask

WORKDIR /pythonapp

ADD tarea_remota/tarea_remota.py /pythonapp/tarea_remota.py

EXPOSE 5000

ENTRYPOINT ["python3", "tarea_remota.py"]
