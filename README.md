# 🚀 DevOps Project

This project involves a **Flask-based web application** that is containerized with **Docker**. The application is deployed in **Google Kubernetes Engine (GKE)**, with automated **CI/CD pipelines** managed using **GitHub Actions**. The pipeline handles **building and pushing the Docker image, testing, and managing image lifecycle**.

The application is monitored using **Prometheus** for data collection, **Loki** for log aggregation, and **Grafana** for real-time data visualization.  
Sensitive data and credentials are securely handled using **GitHub Secrets**.

---

## 🔹 Key Features

- **Flask Web Application**: Built with Flask and exposed as a web service. Containerized using **Docker** for portability.
- **CI/CD Pipeline**: Managed with **GitHub Actions**, including:
  - **CI**: Builds the Docker image, runs tests, and pushes to Docker Hub.
  - **CD**: Provisions a **GKE cluster with Terraform** and deploys via **Helm**.
- **Docker Image Lifecycle**: Old Docker images are cleaned up automatically.
- **Testing**: The CI pipeline ensures the application functions correctly before deployment.
- **GKE & Kubernetes**: The app is deployed to **GKE**, and **Helm charts** simplify deployment management.

---

## 📌 Setup Instructions

### Prerequisites

Ensure you have the following installed:

- **Docker** (for containerization)
- **kubectl** (Kubernetes CLI)
- **Helm** (Kubernetes package manager)
- **Terraform** (for infrastructure provisioning)
- **Google Cloud SDK** (for GKE authentication)
- **GitHub CLI** (for managing GitHub Actions)

### Steps to Set Up Locally

#### Clone the Repository

```
git clone https://github.com/sagitab/flaskDBgender.git
cd flaskDBgender
```

#### Build and Run the Application Locally

```
docker-compose up -d
```

#### Test the Application Locally

Access the Flask app at:

```
http://localhost:5002
```

---

## 🚀 CI/CD Workflow Explanation

### Continuous Integration (CI)

- The GitHub Actions workflow is triggered on every commit.
- The pipeline builds the Docker image and runs automated tests.
- If tests pass, the image is pushed to Docker Hub or Google Artifact Registry.

### Continuous Deployment (CD)

- Terraform provisions the GKE cluster.
- The Helm chart is used to deploy the application to Kubernetes.

---

## 📦 Deployment Steps

### Authenticate with GCP & Configure GKE

```
gcloud auth login
gcloud container clusters get-credentials cluster --region us-central1-a
```

### Apply Terraform to Provision Infrastructure

```
terraform init
terraform apply -auto-approve
```

### Deploy Application with Helm

```
helm install flask-app ./helm-chart
```

### Verify Deployment

```
kubectl get pods
kubectl get services
```

---

## 🔒 Security Considerations

- **Secrets Management**: All sensitive data (API keys, database credentials) are stored securely in GitHub Secrets and never committed to the repository.
- **Ignore files**: `.dockerignore`, `.gitignore`, `.helmignore`

---

## 📊 Monitoring Setup

### Prometheus (Metrics Collection)

- Collects application metrics such as request count and response times.

### Loki (Log Aggregation)

- Collects and centralizes logs from application pods.

### Grafana (Visualization)

#### Port forward Grafana:

```
kubectl port-forward svc/grafana 3000:80
```

#### Open Grafana Dashboard:

```
http://localhost:3000
```

#### Default Login:

- **User:** `admin`
- **Password:** `prom-operator` (Change immediately after logging in)
