FROM python:3

RUN pip install flask

WORKDIR /pythonapp

ADD tarea_remota/tarea_op_logicas.py /pythonapp/tarea_op_logicas.py

EXPOSE 5000

ENTRYPOINT ["python3", "tarea_op_logicas.py"]
