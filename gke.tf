provider "google" {
  project = "tactile-visitor-449316-h6"
  region  = "us-central1"
}

resource "google_container_cluster" "primary" {
  name     = "gke-cluster"
  location = "us-central1"

  remove_default_node_pool = true
  initial_node_count       = 1

  node_pool {
    name       = "default-pool"
    node_count = 2

    node_config {
      machine_type = "e2-medium"
      oauth_scopes = [
        "https://www.googleapis.com/auth/cloud-platform",
      ]
    }
  }
}
