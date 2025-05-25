# DevOps Project

This project involves a Flask-based web application containerized with Docker and deployed on **Google Kubernetes Engine (GKE)** using **ArgoCD** for GitOps-based continuous deployment. CI/CD is managed using **GitHub Actions**, handling Docker image builds, testing, and image lifecycle automation.

The application is monitored using **Prometheus**, **Loki**, and **Grafana**, with dashboards accessible via **LoadBalancer**. Sensitive data is securely stored using **GitHub Secrets**.

---

## 🔹 Key Features

- **Flask Web Application**  
  Built with Flask and Dockerized for portability.

- **CI/CD Pipeline with GitHub Actions**  
  - **CI**: Builds Docker image, runs tests, and pushes to Docker Hub or Artifact Registry.  
  - **CD**: Uses ArgoCD to sync and deploy the application to GKE via Helm.

- **GitOps with ArgoCD**  
  Declarative deployment managed through GitHub repository. ArgoCD ensures cluster state matches the Git source.

- **Image Lifecycle Management**  
  Old Docker images are automatically cleaned up to optimize storage.

- **Monitoring Stack**  
  Prometheus, Loki, and Grafana used for metrics, logs, and visualizations.

---
![Alt text](devops-project%20(1).jpg)

## 📌 Setup Instructions

### Prerequisites

Install:

- Docker
- `kubectl`
- Helm
- Terraform
- Google Cloud SDK (`gcloud`)
- GitHub CLI
- ArgoCD CLI (optional)

---

## 🔧 Local Setup

```bash
git clone https://github.com/sagitab/flaskDBgender.git
cd flaskDBgender
docker-compose up -d
```

App URL (local):  
**http://localhost:5002**

---

## 🚀 CI/CD Workflow

### Continuous Integration (CI)

- Triggered on each commit.
- Builds and tests the Docker image.
- Pushes image to container registry on success.

### Continuous Deployment (CD)

- GKE infrastructure is provisioned with Terraform.
- ArgoCD watches the GitHub repo and syncs the Kubernetes manifests automatically using Helm.

---

## 📦 Deployment Steps

### 1. Authenticate with GCP

```bash
gcloud auth login
gcloud container clusters get-credentials cluster --region us-central1-a
```

### 2. Provision GKE with Terraform

```bash
terraform init
terraform apply -auto-approve
```

### 3. Install ArgoCD

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 4. Access ArgoCD UI

```bash
kubectl get svc argocd-server -n argocd
```

Open in browser using the `EXTERNAL-IP` of the ArgoCD server (port 443):  
**https://<external-ip>**

**Default Login:**

```bash
Username: admin
Password: $(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
```

> 🔒 Change the default password after first login.

---

## 📊 Monitoring Stack

### Prometheus (Metrics Collection)

Collects app metrics like response time and request volume.

### Loki (Log Aggregation)

Streams logs from app containers.

### Grafana (Visualization)

Grafana is exposed via **LoadBalancer**. To access it:

```bash
kubectl get svc -n monitoring
```

Open your browser at the EXTERNAL-IP of the `grafana` service (port 80):  
**http://<external-ip>**

**Login:**

- Username: `admin`  
- Password: `admin` *(or as configured in your Helm values)*

> 🔐 Change the password after first login.

---

## 🔒 Security

- All secrets (API keys, DB credentials) are securely stored in **GitHub Secrets**.
- `.gitignore`, `.dockerignore`, and `.helmignore` prevent sensitive files from being committed.
