DevOps Project
This project involves a Flask-based web application that is containerized with Docker. The application is deployed in Google Kubernetes Engine (GKE), with automated CI/CD pipelines managed using GitHub Actions. The pipeline handles building and pushing the Docker image, testing, and managing image lifecycle. The application is monitored using Prometheus for data collection, Loki for log aggregation, and Grafana for real-time data visualization. Sensitive data and credentials are securely handled using GitHub Secrets.

Key Features:
Flask Web Application: The application is built using the Flask framework and exposed as a web service. It is containerized using Docker to ensure portability across environments.

CI/CD Pipeline: The project includes a CI/CD pipeline managed with GitHub Actions. The CI pipeline builds the Docker image, pushes it to Docker Hub, and ensures the image is up to date. The CD pipeline provisions a GKE cluster using Terraform and deploys the application to Kubernetes with Helm.

Docker Image Lifecycle: The pipeline manages the lifecycle of the Docker image by removing outdated versions to ensure the container registry stays clean and optimized.

Testing: A testing phase is included in the CI pipeline, ensuring that the application functions as expected before being deployed to production.

GKE and Kubernetes: The application is deployed to a Google Kubernetes Engine (GKE) cluster. Helm charts are used to simplify the Kubernetes deployment and management process.

Monitoring & Logging:

Prometheus: Used for collecting application metrics, such as request count and response times.
Loki: Aggregates logs from the application, allowing for efficient searching and troubleshooting.
Grafana: Visualizes data from Prometheus and Loki, providing real-time dashboards to monitor application performance and logs.
Security: Sensitive data and credentials, such as database passwords and API keys, are securely managed using GitHub Secrets and ignore files to prevent them from being exposed in version control.


![Alt text](https://drive.google.com/file/d/1xh4xzFGIwok6LDPFQeqw5xX-J-AcRP0H/view)

Setup Instructions
Prerequisites:
Ensure you have the following installed:

Docker (for containerization)
kubectl (Kubernetes CLI)
Helm (Kubernetes package manager)
Terraform (for infrastructure provisioning)
Google Cloud SDK (for GKE authentication)
GitHub CLI (for managing GitHub Actions)
Steps to Set Up Locally:
Clone the Repository:

bash
Copy
Edit
git clone https://github.com/your-repo-name.git
cd your-repo-name!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Build and Run the Application Locally:

bash
Copy
Edit
docker-compose up -d
Test the Application Locally:
Access the Flask app at:

arduino
Copy
Edit
http://localhost:5002/
CI/CD Workflow Explanation
Continuous Integration (CI)
The GitHub Actions workflow is triggered on every commit.
The pipeline builds the Docker image and runs automated tests.
If tests pass, the image is pushed to Docker Hub or Google Artifact Registry.
Continuous Deployment (CD)
Terraform provisions the GKE cluster.
The Helm chart is used to deploy the application to Kubernetes.

Authenticate with GCP & Configure GKE:

bash
Copy
Edit
gcloud auth login
gcloud container clusters get-credentials cluster --region us-central1
Apply Terraform to Provision Infrastructure:

bash
Copy
Edit
terraform init
terraform apply -auto-approve
Deploy Application with Helm:

bash
Copy
Edit
helm install flask-app ./helm-chart
Verify Deployment:

bash
Copy
Edit
kubectl get pods
kubectl get services
Security Considerations
Secrets Management: All sensitive data (API keys, database credentials) are stored securely in GitHub Secrets and never committed to the repository.
ignores files: .dockerignor .gitignore .helmignore
Monitoring Setup

Collects and centralizes logs from application pods.
Grafana (Visualization):
Port forward Grafana:
bash
Copy
Edit
kubectl port-forward svc/grafana 3000:80
Open Grafana Dashboard:
arduino
Copy
Edit
http://localhost:3000
Default login:
User: admin
Password: prom-operator (Change immediately after logging in).