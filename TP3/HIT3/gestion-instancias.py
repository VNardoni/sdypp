from google.cloud import compute_v1

def listar_instancias(project_id, zone):
    instancia = compute_v1.InstancesClient()
    instances = instancia.list(project=project_id, zone=zone)
    for instance in instances:
        print(f"[{instance.name}] {instance.status}")

def iniciar_instancia(project_id, zone, instance_name):
    instancia = compute_v1.InstancesClient()
    instancia.start(project=project_id, zone=zone, instance=instance_name)

    print(f"Iniciando instancia {instance_name}.")

def pausar_instancia(project_id, zone, instance_name):
    instancia = compute_v1.InstancesClient()
    instancia.stop(project=project_id, zone=zone, instance=instance_name)

    print(f"Instancia {instance_name} pausada.")

def reiniciar_instancia(project_id, zone, instance_name):
    instancia = compute_v1.InstancesClient()
    instancia.start(project=project_id, zone=zone, instance=instance_name)

    print(f"Reiniciando instancia {instance_name}.")

def borrar_instancia(project_id, zone, instance_name):
    instancia = compute_v1.InstancesClient()
    instancia.delete(project=project_id, zone=zone, instance=instance_name)
    print(f"Eliminando instancia {instance_name}.")


def crear_instancia(project_id, zone, instance_name):
    instancia = compute_v1.InstancesClient()
    image_project = "ubuntu-os-cloud"
    image_family = "ubuntu-2204-lts"

    instance_body = {
        "name": instance_name,
        "machine_type": f"zones/{zone}/machineTypes/e2-micro",
        "disks": [
            {
                "boot": True,
                "initialize_params": {
                    "source_image": f"projects/{image_project}/global/images/family/{image_family}"
                }
            }
        ],
        "network_interfaces": [
            {
                "network": "global/networks/default",
                "access_configs": [{
                }]
            }
        ],
    }
    instancia.insert(project=project_id, zone=zone, instance_resource=instance_body)
    print(f"Creando instancia {instance_name}.")





def mostrar_menu():
    print("Seleccione una opción:")
    print("1. Listar instancias")
    print("2. Iniciar instancia")
    print("3. Pausar instancia")
    print("4. Reiniciar instancia")
    print("5. Borrar instancia")
    print("6. Crear instancia")
    print("0. Salir")

def ejecutar_opcion(opcion):
    if opcion == '1':
        listar_instancias(project_id, zone)
    elif opcion == '2':
        instance_name = input("Ingrese el nombre de la instancia: ")
        iniciar_instancia(project_id, zone, instance_name)
    elif opcion == '3':
        instance_name = input("Ingrese el nombre de la instancia: ")
        pausar_instancia(project_id, zone, instance_name)
    elif opcion == '4':
        instance_name = input("Ingrese el nombre de la instancia: ")
        reiniciar_instancia(project_id, zone, instance_name)
    elif opcion == '5':
        instance_name = input("Ingrese el nombre de la instancia: ")
        borrar_instancia(project_id, zone, instance_name)
    elif opcion == '6':
        instance_name = input("Ingrese el nombre de la instancia: ")
        
        
        crear_instancia(project_id, zone, instance_name)
    
    elif opcion == '0':
        print("Saliendo del programa...")
        exit()
    else:
        print("Opción no válida")

project_id = "ultra-reflector-421322"
zone = "us-east1-b"

while True:
    mostrar_menu()
    opcion = input("Ingrese la opción deseada: ")
    ejecutar_opcion(opcion)
