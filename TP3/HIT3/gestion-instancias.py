from google.cloud import compute_v1

def listar_instancias(project_id, zone):
    compute_client = compute_v1.InstancesClient()
    instances = compute_client.list(project_id, zone)
    for instance in instances:
        print(f"[{instance.name}] {instance.status}")

def iniciar_instancia(project_id, zone, instance_name):
    compute_client = compute_v1.InstancesClient()
    operation = compute_client.start(project_id, zone, instance_name)
    print(f"Iniciando instancia {instance_name}. Operación: {operation.name}")

def pausar_instancia(project_id, zone, instance_name):
    compute_client = compute_v1.InstancesClient()
    operation = compute_client.stop(project_id, zone, instance_name)
    print(f"Instancia {instance_name} pausada. Operación: {operation.name}")

def reiniciar_instancia(project_id, zone, instance_name):
    compute_client = compute_v1.InstancesClient()
    operation = compute_client.start(project_id, zone, instance_name)
    print(f"Reiniciando instancia {instance_name}. Operación: {operation.name}")

def borrar_instancia(project_id, zone, instance_name):
    compute_client = compute_v1.InstancesClient()
    operation = compute_client.delete(project_id, zone, instance_name)
    print(f"Eliminando instancia {instance_name}. Operación: {operation.name}")
    
project_id = "ultra-reflector-421322"
zone = "us-east1-b"