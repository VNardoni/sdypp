FROM python:3
RUN mkdir usr/local/src/pythonapp
ADD /server.py usr/local/src/pythonapp/server.py 
RUN pip install Flask
EXPOSE 5000

ENTRYPOINT ["python3", "usr/local/src/pythonapp/server.py"]