variable "credentials_file_path"{

type =string
default ="/credentials/credentials.json" 

}

variable "project_id"{

type= string 
default="ultra-reflector-421322"

}

variable "region" {
  type= string 
  default     = "us-east1"  
}

variable "zone" {
  type= string 
  default     = "us-east1-b"  
}


variable "instancias" {
    type=number
    default= 3
    
    }

variable "tipo_vm" {
      type=string
       default="e2-micro"
      
      }
variable "imagen"{
      type=string
      default= "ubuntu-os-cloud/ubuntu-2204-lts"
        
        }