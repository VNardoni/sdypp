

output "instance_ip" {
  value = google_compute_instance.pruebavm [0].network_interface[0].access_config[0].nat_ip
}


output "ssh_username" {
  value       = split("@", data.google_client_openid_userinfo.me.email)[0]
  description = "Los nombres de usuario SSH para conectarse por SSH a las instancias."
}

output "ssh_private_key" {
  value     = tls_private_key.ssh_key.private_key_pem
  sensitive = true
}

output "ssh_public_key" {
  value = tls_private_key.ssh_key.public_key_openssh
}
