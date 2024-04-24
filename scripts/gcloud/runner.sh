USER="grupodos"
gcloud services enable logging.googleapis.com
gcloud logging read "resource.type=gce_instance AND protoPayload.methodName=beta.compute.instances.insert"

# AGREGAMOS LA REGLAS DE FIREWALL
gcloud compute firewall-rules create allow-ssh --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:22 --source-ranges=0.0.0.0/0
gcloud compute firewall-rules create allow-http --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:80 --source-ranges=0.0.0.0/0
gcloud compute firewall-rules create allow-hit1 --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:8110 --source-ranges=0.0.0.0/0
gcloud compute firewall-rules create allow-hit2 --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:8120 --source-ranges=0.0.0.0/0
gcloud compute firewall-rules create allow-hit3 --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:8130 --source-ranges=0.0.0.0/0
gcloud compute firewall-rules create allow-hit4 --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:8140 --source-ranges=0.0.0.0/0
gcloud compute firewall-rules create allow-hit5 --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:8150 --source-ranges=0.0.0.0/0
gcloud compute firewall-rules create allow-hit6s --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:8160 --source-ranges=0.0.0.0/0
gcloud compute firewall-rules create allow-hit6c --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:8161 --source-ranges=0.0.0.0/0
gcloud compute firewall-rules create allow-hit7s --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:8170 --source-ranges=0.0.0.0/0
gcloud compute firewall-rules create allow-hit7c --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:8171 --source-ranges=0.0.0.0/0
gcloud compute firewall-rules create allow-tp2hit1 --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:8210 --source-ranges=0.0.0.0/0

# GENERACION DE CLAVES 
ssh-keygen -t rsa -b 4096 -C "${USER}@example.com" -f ./id_rsa_example -q -N ""
gcloud compute project-info add-metadata --metadata "ssh-keys=${USER}:$(cat ./id_rsa_example.pub)"

# CREACION DE LA MAQUINA VIRTUAL
gcloud compute instances create vm \
    --machine-type=e2-micro \
    --preemptible \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --tags=http-server \
    --metadata="ssh-keys=$(cat id_rsa_example.pub)" \
    --metadata-from-file user-data=script.sh \
    --zone="us-east1-b" \
    --address=instance-public-ip

# CONEXION A LA VM
gcloud compute ssh vm --zone=us-east1-b --ssh-key-file=./id_rsa_example

# BORRAR VM
#gcloud compute instances delete vm --zone=us-east1-b