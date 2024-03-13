# VARIABLES

USER = "grupodos"
ZONE = "us-east1"

# CREAMOS IP PUBLICA

# gcloud services enable logging.googleapis.com
# gcloud logging read "resource.type=gce_instance AND protoPayload.methodName=beta.compute.instances.insert"

# AGREGAMOS LA REGLAS DE FIREWALL


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