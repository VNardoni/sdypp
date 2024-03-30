FROM python:3
RUN mkdir usr/local/src/pythonapp
ADD /server.py usr/local/src/pythonapp/server.py 
EXPOSE 8080
WORKDIR usr/local/src/pythonapp
ENTRYPOINT ["python3", "server.py"]