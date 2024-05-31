from google.cloud import storage

def subir_imagen(bucket_name, imagen_local, nombre_remoto):
    """Sube una imagen local al bucket."""
    # Crear el cliente de Google Cloud Storage
    storage_client = storage.Client()

    # Obtener el bucket
    bucket = storage_client.bucket(bucket_name)

    # Crear un blob (objeto en el bucket) con el nombre deseado
    blob = bucket.blob(nombre_remoto)

    # Subir la imagen al blob
    blob.upload_from_filename(imagen_local)

    print(f"Imagen {imagen_local} subida a {bucket_name}/{nombre_remoto}")

def descargar_imagen(bucket_name, nombre_remoto, destino_local):
    """Descarga una imagen del bucket al sistema local."""
    # Crear el cliente de Google Cloud Storage
    storage_client = storage.Client()

    # Obtener el bucket
    bucket = storage_client.bucket(bucket_name)

    # Obtener el blob (archivo) especificado por nombre_remoto
    blob = bucket.blob(nombre_remoto)

    # Descargar el blob a un archivo local
    blob.download_to_filename(destino_local)

    print(f"Imagen {nombre_remoto} descargada a {destino_local}")

if __name__ == "__main__":
    # Nombre del bucket
    bucket_name = "bucket_imagenes_sdypp"

    # Ruta de la imagen local que quieres subir
    imagen_local = "imagen.jpg"

    # Nombre que deseas darle al archivo en el bucket
    nombre_remoto = "nombre-unico.jpg"

    # Subir la imagen al bucket
    subir_imagen(bucket_name, imagen_local, nombre_remoto)

    # Descargar la imagen del bucket a un archivo local
    destino_local = "imagen_descargada.jpg"
    descargar_imagen(bucket_name, nombre_remoto, destino_local)
