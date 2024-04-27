provider "google" {

credentials= file(var.credentials_file_path)
project = var.project_id
zone= var.zone
region=var.region
}

resource "google_compute_instance" "pruebavm" {
  count        = var.instancias
  name         = "vm-${count.index + 1}"
  machine_type = var.tipo_vm
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = var.imagen
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }
}