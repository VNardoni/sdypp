# Instrucciones

## En la VM

`sudo apt update`
`sudo apt install docker.io`
`sudo docker pull lucasrueda01/server`
`sudo docker run -d --rm  -v /var/run/docker.sock:/var/run/docker.sock -p 8080:8080 lucasrueda01/server`

## De forma local

`cd TP2\HIT1`
`python client.py lucasrueda01/tarea_remota`
