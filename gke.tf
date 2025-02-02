provider "google" {
  project = "tactile-visitor-449316-h6"
  region  = "us-east1"
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
  node_count = 2

  node_config {
    machine_type = "e2-medium"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }
}
