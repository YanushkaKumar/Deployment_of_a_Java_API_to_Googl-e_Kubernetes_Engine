# Java Spring Boot API Deployment to Kubernetes on GKE

![Project Status](https://img.shields.io/badge/status-complete-brightgreen.svg)
![Kubernetes](https://img.shields.io/badge/kubernetes-v1.24-blue.svg)
![Spring Boot](https://img.shields.io/badge/spring%20boot-3.1.0-green.svg)
![GCP](https://img.shields.io/badge/GCP-GKE-blue.svg)

## Project Overview

This repository contains the source code, configuration, and documentation for deploying a Java Spring Boot API to a Google Kubernetes Engine (GKE) cluster, as part of the DevOps Assignment. The project demonstrates production-grade practices, including containerization, secure image storage, Kubernetes orchestration, HTTPS with automated TLS, and monitoring with Prometheus and Grafana.

**Author**: Yanushka  
**Date**: August 10, 2025  
**Course**: DevOps Assignment  

### Objectives
- Containerize a Java Spring Boot application using a multi-stage Dockerfile.
- Push the container image to Google Artifact Registry.
- Deploy to GKE using declarative Kubernetes manifests.
- Configure NGINX Ingress for external access.
- Implement automated HTTPS with cert-manager and Let's Encrypt.
- Set up monitoring with Prometheus and Grafana (bonus feature).

The API provides endpoints like `/health` and `/api/users`, serving sample JSON data.

## Prerequisites

- **Docker**: Installed and configured for building images.
- **kubectl**: Configured to connect to a GKE cluster.
- **gcloud CLI**: Installed and authenticated with a GCP project.
- **GCP Project**: Artifact Registry API enabled.
- **Helm**: Installed for monitoring setup.
- **Domain**: A domain or dynamic DNS (e.g., `apiyanushka.duckdns.org` used in this project).
- **Knowledge**: Familiarity with Java, Docker, Kubernetes, and GCP.

## Repository Structure

```bash
├── src/                            # Java source code
│   └── main/java/com/example/api/   # Spring Boot application
├── k8s/                            # Kubernetes manifests
│   ├── 01-namespace.yaml
│   ├── 02-configmap.yaml
│   ├── 03-secret.yaml
│   ├── 04-deployment.yaml
│   ├── 05-service.yaml
│   ├── 06-hpa.yaml
│   ├── 07-certificate.yaml
│   └── 08-ingress.yaml
├── scripts/                        # Utility scripts
│   ├── monitor.sh
│   └── cleanup.sh
├── Dockerfile                      # Multi-stage Dockerfile
├── pom.xml                         # Maven configuration
├── .dockerignore                   # Docker ignore file
└── docs/Final_Report.pdf           # Detailed project report
```

## Setup Instructions

### Phase 1: Application Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Build the Application**:
   ```bash
   mvn clean package -DskipTests
   ```

### Phase 2: Containerization

1. **Dockerfile Overview**:
   A multi-stage Dockerfile ensures a lightweight, secure image:
   - **Builder Stage**: Uses `openjdk:17-jdk-slim` to compile the JAR.
   - **Runtime Stage**: Uses `openjdk:17-jre-slim`, runs as non-root, includes health checks.

2. **Build and Test Locally**:
   ```bash
   docker build -t java-api:1.0.0 .
   docker run -p 8080:8080 java-api:1.0.0
   curl http://localhost:8080/health
   curl http://localhost:8080/api/users
   ```

   <img width="975" height="548" alt="image" src="https://github.com/user-attachments/assets/9d7a22ef-cd44-4a80-9dd5-7f018ee6c0e3" />

   *(e.g., Terminal showing successful Docker build and curl responses for `/health` and `/api/users`.)*

### Phase 3: Google Artifact Registry

1. **Set Environment Variables**:
   ```bash
   export PROJECT_ID="your-project-id"
   export REGION="us-central1"
   export REPOSITORY_NAME="java-api-repo"
   ```

2. **Create Repository and Push Image**:
   ```bash
   gcloud artifacts repositories create $REPOSITORY_NAME --repository-format=docker --location=$REGION --project=$PROJECT_ID
   gcloud auth configure-docker $REGION-docker.pkg.dev
   docker tag java-api:1.0.0 $REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY_NAME/java-api:1.0.0
   docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY_NAME/java-api:1.0.0
   ```

   <img width="975" height="517" alt="image" src="https://github.com/user-attachments/assets/bd67be35-2e6c-48ea-a85c-54334586ecbf" />
 
   *(e.g., GCP console or terminal output showing the image in Artifact Registry.)*

### Phase 4: Kubernetes Deployment

1. **Namespace**: Deployed in `java-api-ns-yanushka` for isolation.
2. **Manifests**:
   - **Deployment**: 3 replicas, RollingUpdate, resource limits (CPU: 250m-500m, Memory: 256Mi-512Mi), liveness/readiness probes.
   - **Service**: ClusterIP on port 80 targeting 8080.
   - **HPA**: Scales between 3-10 replicas based on 70% CPU and 80% memory utilization.

3. **Apply Manifests**:
   ```bash
   sed -i "s/REGION/$REGION/g" k8s/04-deployment.yaml
   sed -i "s/PROJECT_ID/$PROJECT_ID/g" k8s/04-deployment.yaml
   sed -i "s/REPOSITORY_NAME/$REPOSITORY_NAME/g" k8s/04-deployment.yaml
   kubectl apply -f k8s/
   ```

4. **Verify Deployment**:
   ```bash
   kubectl get all -n java-api-ns-yanushka
   ```

   <img width="975" height="548" alt="image" src="https://github.com/user-attachments/assets/89f10692-802f-453d-b119-08b47bea45ca" />

   <img width="975" height="515" alt="image" src="https://github.com/user-attachments/assets/1e26e3f0-1c8a-42d3-b1a9-0521a3e99fec" />

 
   *(e.g., Output of `kubectl get all -n java-api-ns-yanushka` showing pods, services, deployment, and HPA in READY state.)*

### Phase 5: Ingress and TLS

1. **Install NGINX Ingress Controller**:
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml
   kubectl wait --namespace ingress-nginx --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=120s
   ```

2. **Set Up Cert-Manager**:
   Install cert-manager and configure a Let's Encrypt ClusterIssuer.

3. **Apply Certificate and Ingress**:
   - Certificate: Requests TLS for `apiyanushka.duckdns.org`.
   - Ingress: Routes traffic to `java-api-service`, enforces HTTPS.

   ```bash
   kubectl apply -f k8s/07-certificate.yaml
   kubectl apply -f k8s/08-ingress.yaml
   ```

   <img width="975" height="517" alt="image" src="https://github.com/user-attachments/assets/b04de867-4451-49e1-b50b-2f92d78e1732" />

   <img width="975" height="514" alt="image" src="https://github.com/user-attachments/assets/a5432761-7a40-45a9-8cb8-0b4cea58115a" />

   <img width="975" height="519" alt="image" src="https://github.com/user-attachments/assets/bc1351b6-ba40-4f20-9854-ca9bddaf9cb3" />
   
   *(e.g., Output of `kubectl get ingress -n java-api-ns-yanushka` and `kubectl get certificate -n java-api-ns-yanushka` showing ADDRESS and READY status.)*

### Phase 6: Testing and Verification

1. **Terminal Testing**:
   ```bash
   curl https://apiyanushka.duckdns.org/api/users
   ```

   Expected response:
   ```json
   [{"id":1,"name":"John Doe","email":"john@example.com"},{"id":2,"name":"Jane Smith","email":"jane@example.com"}]
   ```

  <img width="975" height="516" alt="image" src="https://github.com/user-attachments/assets/c34c7f20-bd48-4148-9b74-cb7b00f5bf72" />
 
   *(e.g., Terminal showing curl command and JSON response over HTTPS.)*

2. **Browser Verification**:
   Access `https://apiyanushka.duckdns.org/api/users` in a browser. Verify the secure lock icon.

   <img width="975" height="548" alt="image" src="https://github.com/user-attachments/assets/a4474932-ce81-4411-b2af-cbf5bdbf2b19" />

   *(e.g., Browser displaying JSON response with HTTPS lock icon.)*

### Phase 7: Monitoring 

1. **Install Monitoring Stack**:
   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
   ```

2. **Configure ServiceMonitor**:
   Scrapes metrics from Spring Boot Actuator (`/actuator/metrics`).

3. **Grafana Dashboard**:
   Visualizes JVM memory, CPU usage, and API request rates.

  <img width="975" height="515" alt="image" src="https://github.com/user-attachments/assets/32e59029-f714-4074-a15c-9afe236bf817" />

 <img width="975" height="514" alt="image" src="https://github.com/user-attachments/assets/9773090f-54d4-4386-ac1e-9d6fdbdf018b" />

   *(e.g., Grafana showing graphs for CPU, memory, and API metrics.)*

### Utility Scripts

- **monitor.sh**: Displays status of pods, services, ingress, HPA, and events.
   ```bash
   ./scripts/monitor.sh
   ```
<img width="1919" height="1016" alt="image" src="https://github.com/user-attachments/assets/7da845c3-5b95-42f9-a005-107c2c432b63" />


- **cleanup.sh**: Removes Kubernetes resources and local images.
   ```bash
   ./scripts/cleanup.sh
   ```
<img width="1919" height="1017" alt="image" src="https://github.com/user-attachments/assets/01d13b1a-8fe7-41d5-9380-1f61f5d98a36" />


## Troubleshooting

- **Pod Issues**: Check logs (`kubectl logs -f pod/<pod-name> -n java-api-ns-yanushka`) or describe (`kubectl describe pod <pod-name>`).
- **Ingress Issues**: Verify controller logs (`kubectl logs -n ingress-nginx`) or describe (`kubectl describe ingress java-api-ingress`).
- **Image Pull Issues**: Confirm image exists (`gcloud artifacts docker images list`).

## Deliverables

- **Source Code**: Complete Java application and Dockerfile.
- **Kubernetes Manifests**: All YAML files in `k8s/`.
- **Documentation**: Final Report (`docs/Final_Report.pdf`).
- **Screenshots** (as indicated above):
  - Local Docker test output.
  - Artifact Registry push confirmation.
  - Kubernetes resources overview.
  - Ingress and TLS certificate status.
  - Curl testing output.
  - Browser API access.
  - Grafana metrics dashboard.

## Conclusion

This project successfully demonstrated the end-to-end process of deploying a containerized Java application to Kubernetes. All core objectives were met, including containerization, deployment, secure ingress configuration, and testing. The implementation of bonus features like monitoring and security policies further elevates the deployment to a production-ready standard.
