FROM python:3
RUN mkdir usr/local/src/pythonapp
ADD /tarea_remota.py usr/local/src/pythonapp/tarea_remota.py 
RUN pip install Flask
EXPOSE 5001

ENTRYPOINT ["python3", "usr/local/src/pythonapp/tarea_remota.py"]