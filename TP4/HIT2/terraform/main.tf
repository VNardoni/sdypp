provider "google" {
  credentials = file(var.credentials_file_path)
  project     = var.project_id
  zone        = var.zone
  region      = var.region
}

data "google_client_openid_userinfo" "me" {}




resource "google_compute_instance" "vm_instance" {
  count        = var.instancias
  name         = "worker"
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

  # metadata_startup_script = file(var.metadata_startup_script)

  metadata = {
    ssh-keys = "${split("@", data.google_client_openid_userinfo.me.email)[0]}:${tls_private_key.ssh_key.public_key_openssh}"
  }
}

resource "google_compute_instance" "rabbit_instance" {
  count        = 1
  name         = "rabbit-mq"
  machine_type = var.tipo_vm
  zone         = var.zone
  metadata_startup_script = file(var.startup_rabbit)

  boot_disk {
    initialize_params {
      image = var.imagen_rabbit
    }
  }

network_interface {
    network = "default"
    access_config {}
  }

  
 
  metadata = {
    ssh-keys = "${split("@", data.google_client_openid_userinfo.me.email)[0]}:${tls_private_key.ssh_key.public_key_openssh}"
  }


}


resource "google_compute_firewall" "allow-ssh" {
  name    = "allow-ssh"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
}





resource "google_compute_firewall" "allow-http" {
  name    = "allow-http"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "allow-https" {
  name    = "allow-https"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["443"]
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}
resource "local_file" "ssh_private_key_pem" {
  content         = tls_private_key.ssh_key.private_key_pem
  filename        = ".ssh/google_compute_engine"
  file_permission = "0600"
}


resource "google_compute_firewall" "flask" {
  name    = "permitir-flask"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["5000"]
  }

  source_ranges = ["0.0.0.0/0"]
}