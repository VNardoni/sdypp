# DESDE EL CLIENTE

• HACEMOS BUILD DE LA IMAGEN 'HIT' •

Pararse en ../TP1/HIT1

docker build . -t hit1 -f dockerfiles/hit1.dockerfile

• COLOCAMOS EL TAG A LA IMAGEN 'hit1' •

docker tag hit1 vnardoni/hit1

• LOGIN •

docker login

• HACEMOS PUSH DE LA IMAGEN •

docker push vnardoni/hit1

==========================================================

# DESDE LA VM DE GCLOUD

• INSTALAMOS DOCKER • 

sudo apt install docker.io

• LOGIN •

sudo docker login

• HACEMOS EL PULL DE LA IMAGEN •

sudo docker pull vnardoni/hit1

• HACMOE RUN A LA IMAGEN •

sudo docker run --name hit1 --rm -p 8080:8080 vnardoni/hit1