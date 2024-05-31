from google.cloud import storage
def listar_imagenes(bucket_name):
    """Lista los blobs (archivos) en el bucket."""
    # Crear el cliente de Google Cloud Storage
    storage_client = storage.Client()

    # Obtener el bucket
    bucket = storage_client.bucket(bucket_name)

    # Listar blobs en el bucket
    blobs = bucket.list_blobs()

    print(f"Imágenes en el bucket {bucket_name}:")
    for blob in blobs:
        # Filtrar por tipo de contenido si solo deseas listar imágenes
        if blob.content_type.startswith('image/'):
            print(f"  {blob.name}")

if __name__ == "__main__":
    # Nombre del bucket
    bucket_name = "bucket_imagenes_sdypp"

    # Listar imágenes en el bucket
    listar_imagenes(bucket_name)