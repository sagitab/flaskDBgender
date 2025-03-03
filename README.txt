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

