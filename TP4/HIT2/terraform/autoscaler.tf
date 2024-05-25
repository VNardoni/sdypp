resource "google_compute_region_autoscaler" "cras" {

  name   = "autoscaler"
  region = var.region
  target = google_compute_region_instance_group_manager.rmig.self_link

  autoscaling_policy {
    max_replicas    = 8
    min_replicas    = 1
    cooldown_period = 30


    cpu_utilization {
      target = 0.75
    }
  }
}
