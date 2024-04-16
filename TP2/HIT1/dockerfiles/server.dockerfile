FROM  python:3.9.19-alpine3.19

WORKDIR /usr/local/src/pythonapp
RUN pip install Flask
RUN pip install requests
RUN pip install docker

RUN mkdir /usr/local/src/python

ADD server.py /usr/local/src/pythonapp/server.py

EXPOSE 8080
WORKDIR /usr/local/src/pythonapp
ENV FLASK_APP=server.py    
CMD ["python", "server.py"]