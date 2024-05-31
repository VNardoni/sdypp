variable "region" {
  type    = string
  default = "us-east1"
}

variable "zone" {
  type    = string
  default = "us-east1-c"
}

variable "credentials_file_path" {

  type    = string
  default = "credentials.json"

}

variable "project_id" {

  type    = string
  default = "continual-air-416912"

}

variable "instancias" {
  type    = number
  default = 1

}

variable "tipo_vm" {
  type    = string
  default = "e2-micro"

}

variable "imagen" {
  type    = string
  default = "worker-image-sdypp2024"
}
variable "metadata_startup_script" {
  type    = string
  default = "../requeriments.sh"
}

#####Balancer####

variable "balancer_name" { default = "balancer" }

variable "base_instance_name" { default = "instancia" }

# Instance Template
variable "prefix" { default = "worker-" }
variable "desc" { default = "Worker que realiza funcion sobel." }
variable "tags" { default = "servicio" }
variable "desc_inst" { default = "worker sobel instance" }
variable "machine_type" { default = "n1-standard-1" }
variable "source_image" { default = "ubuntu-os-cloud/ubuntu-2204-lts" } //This is the family tag used when building the Golden Image with Packer.




variable "network" { default = "default" }


# Healthcheck
variable "hc_name" {
  type    = string
  default = "sobel-healthcheck"
}

variable "hc_port" {
  type    = string
  default = "80"
}


##backend
variable "be_name" { default = "http-backend" }
variable "be_protocol" { default = "HTTP" }
variable "be_port_name" { default = "http" }
variable "be_timeout" { default = "10" }
variable "be_session_affinity" { default = "NONE" }

# Global Forwarding Rule
variable "gfr_name" { default = "website-forwarding-rule" }
variable "gfr_portrange" { default = "80" }
variable "thp_name" { default = "http-proxy" }
variable "urlmap_name" { default = "http-lb-url-map" }
#
# Firewall Rules
variable "fwr_name" { default = "allow-http-https" }

#Autoscaler

variable "min_replicas" {
  type    = string
  default = 1
}

variable "max_replicas" {
  type    = string
  default = 10
}

###Rabbit 

variable "imagen_rabbit" {
  type    = string
  default = "rabbitimage2024"
}

variable "startup_rabbit" {
  type    = string
  default = "rabbit.sh"
}

##Redis

variable "imagen_redis" {
  type    = string
  default = "redis-image"
}

variable "startup_redis" {
  type    = string
  default = "redis.sh"
}