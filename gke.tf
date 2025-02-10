provider "google" {
  project = "tactile-visitor-449316-h6"
  region  = "us-east1"
}

terraform {
  backend "gcs" {
    bucket  = "terraform-state-sensay"  # ✅ Your GCS bucket name
    prefix  = "terraform/state"         # ✅ Path inside the bucket
  }
}


resource "google_container_cluster" "primary" {
  name     = "gke-cluster"
  location = "us-east1"

  remove_default_node_pool = true
  initial_node_count       = 1  # ✅ Required, even though it's removed immediately
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "default-pool"
  cluster    = google_container_cluster.primary.name
  location   = google_container_cluster.primary.location
  node_count = 1

   node_config {
    machine_type = "e2-medium"
    disk_size_gb = 50  # 🔹 Reduce disk size to fit within quota
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }
}
