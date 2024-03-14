# VARIABLES

USER = "grupo2sdypp"
ZONE = "us-east1-b"


# CREAMOS IP PUBLICA

gcloud compute addresses create instance-public-ip --region="us-east1"
# gcloud services enable logging.googleapis.com
# gcloud logging read "resource.type=gce_instance AND protoPayload.methodName=beta.compute.instances.insert"

# AGREGAMOS LA REGLAS DE FIREWALL
gcloud compute firewall-rules create allow-ssh --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:22 --source-ranges=0.0.0.0/0
gcloud compute firewall-rules create allow-http --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:80 --source-ranges=0.0.0.0/0

# GENERACION DE CLAVES 

ssh-keygen -t rsa -b 4096 -C "${USER}@example.com" -f ./id_rsa_example -q -N ""

gcloud compute project-info add-metadata --metadata "ssh-keys=${USER}:$(cat ./id_rsa_example.pub)"

# CREACION DE LA MAQUINA VIRTUAL

gcloud compute instances create vm1 \
 --zone="$ZONE" \
    --machine-type=e2-micro \
    --preemptible \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --tags=http-server \
    --metadata="ssh-keys=$USER:$(cat ./id_rsa_example.pub)" \
 --metadata-from-file user-data=./script.sh \
 --address=instance-public-ip

# CONEXION A LA VM

gcloud compute ssh vm1 --zone=us-east1-b --ssh-key-file=./id_rsa_example
