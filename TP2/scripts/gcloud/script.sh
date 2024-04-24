sudo apt update
sudo apt install docker.io

#Nomenclatura puertos: 8|TP|HIT|x
#TP1
# Pull imagenes
sudo docker pull vnardoni/hit1
sudo docker pull vnardoni/hit2
sudo docker pull vnardoni/hit3
sudo docker pull vnardoni/hit4
sudo docker pull vnardoni/hit5
sudo docker pull vnardoni/hit6server
sudo docker pull vnardoni/hit6cliente
sudo docker pull vnardoni/hit7server
sudo docker pull vnardoni/hit7cliente
#Ejecutar
sudo docker run --name hit1 --rm -p 8110:8110 vnardoni/hit1
sudo docker run --name hit2 --rm -p 8120:8120 vnardoni/hit2
sudo docker run --name hit3 --rm -p 8130:8130 vnardoni/hit3
sudo docker run --name hit4 --rm -p 8140:8140 vnardoni/hit4 localhost 8140
sudo docker run --name hit5 --rm -p 8150:8150 vnardoni/hit5 localhost 8150
sudo docker run --name hit6server --network host --rm -p 8160:8160 vnardoni/hit6server localhost 8160
sudo docker run --name hit6cliente --network host --rm -p 8161:8161 vnardoni/hit6cliente localhost 8161
sudo docker run --name hit7server --network host --rm -p 8170:8170 vnardoni/hit7server localhost 8170
sudo docker run --name hit7cliente --network host --rm -p 8171:8171 vnardoni/hit7cliente localhost 8171

#TP2
# Pull imagenes
sudo docker pull lucasrueda01/server
#Ejecutar
sudo docker run --name tp2hit1 -d --rm -v /var/run/docker.sock:/var/run/docker.sock -p 8210:8210 lucasrueda01/server
