FROM  python:3.9.19-alpine3.19

RUN pip install flask

RUN mkdir -p /usr/local/src/pythonapp

ADD tarea_remota.py /usr/local/src/pythonapp/tarea_remota.py

EXPOSE 5000
WORKDIR /usr/local/src/pythonapp
ENV FLASK_APP=tarea_remota.py    
CMD ["python", "tarea_remota.py"]