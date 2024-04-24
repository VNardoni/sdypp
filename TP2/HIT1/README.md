# Instrucciones

## En la VM

`sudo apt update`
`sudo apt install docker.io`
`sudo docker pull vnardoni/server`
`sudo docker run -d --rm  -v /var/run/docker.sock:/var/run/docker.sock -p 8210:8210 vnardoni/server`

## De forma local

`cd TP2\HIT1`
`python client.py vnardoni/tarearemota`
