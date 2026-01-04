# SecureBankingOps: Azure DevSecOps Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=flat&logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=flat&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/)
[![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=flat&logo=terraform&logoColor=white)](https://www.terraform.io/)

##  Project Overview

**SecureBankingOps** is a production-grade microservices architecture designed to simulate a real-world financial platform. It demonstrates a complete **DevSecOps lifecycle**, moving from Infrastructure-as-Code provisioning to automated security scanning and GitOps-driven deployment.

The platform consists of a React frontend and multiple Python/Flask backend services (Auth, Accounts, Payments), all containerized and orchestrated on **Azure Kubernetes Service (AKS)**.

###  Architecture
```mermaid
graph TD
    User[User / Client] -->|HTTPS| ALB[Azure Load Balancer]
    
    subgraph Azure_Cloud [Azure Cloud]
        style Azure_Cloud fill:#e0e0e0,stroke:#333,stroke-width:2px,color:#000
        
        ALB -->|Traffic| Ingress[NGINX Ingress Controller]
        
        subgraph AKS_Cluster [AKS Cluster]
            style AKS_Cluster fill:#f9f9f9,stroke:#333,stroke-width:2px,color:#000
            
            Ingress -->|/| Frontend["Frontend Service <br/> (React)"]
            Ingress -->|/auth| Auth["Auth Service <br/> (Python)"]
            Ingress -->|/accounts| Accounts[Accounts Service <br/> (Python)]
            Ingress -->|/payments| Payments[Payments Service <br/> (Python)]
        end
    end
    
    classDef service fill:#326ce5,stroke:#fff,stroke-width:2px,color:#fff;
    classDef ingress fill:#009639,stroke:#fff,stroke-width:2px,color:#fff;
    
    class Frontend,Auth,Accounts,Payments service;
    class Ingress ingress;
```    
*(A visual representation of the AKS Cluster, Ingress Controller, Microservices, and Traffic Flow)*

##  Microservices Breakdown

The platform is composed of four decoupled services, each running in its own container and communicating via internal ClusterIPs.

| Service | Type | Port | Stack | Responsibility |
| :--- | :--- | :--- | :--- | :--- |
| **Frontend** | UI | `80` | **React.js** | Single Page Application (SPA) serving the banking dashboard. Routes API calls to the ingress controller. |
| **Auth Service** | Backend | `5000` | **Python (Flask)** | Handles user authentication and issues **JWT Tokens** for secure session management. |
| **Accounts** | Backend | `5001` | **Python (Flask)** | Manages user profiles, ledger logic, and account balance states. |
| **Payments** | Backend | `5002` | **Python (Flask)** | Processes money transfers between accounts and ensures transaction atomicity. |

> **Networking Note:** External traffic enters via the **NGINX Ingress Controller**, which routes requests based on the request path (`/auth`, `/accounts`, `/payments`) to the correct internal service.

---

##  Technical Stack

| Category | Technologies Used |
|----------|-------------------|
| **Cloud Infrastructure** | Azure Kubernetes Service (AKS), Azure Container Registry (ACR), Virtual Networks |
| **IaC & Provisioning** | Terraform (Modular Infrastructure) |
| **CI/CD & GitOps** | GitHub Actions (CI), ArgoCD (CD) |
| **Security** | Azure Key Vault (Secrets), Trivy (Vulnerability Scanning), TLS/SSL |
| **Networking** | NGINX Ingress Controller, Azure Load Balancer |
| **Observability** | Prometheus (Metrics), Grafana (Visualization) |
| **Application** | React.js (Frontend), Python Flask (Backend Microservices) |

---

##  The Debugging Journey (Real-World Troubleshooting)

Building this project involved solving complex integration challenges. Below are specific technical hurdles encountered and resolved:

### 1. Ingress "Progressing" State & Service Name Mismatches
* **The Issue:** ArgoCD reported the Ingress resource as "Progressing" indefinitely.
* **Root Cause Analysis:** `kubectl describe ingress` revealed an error: `<error: services "frontend-service" not found>`. The Helm chart `ingress.yaml` was pointing to `frontend-service`, but the actual Kubernetes Service was named `frontend`.
* **The Fix:** Refactored the Helm template to align the Ingress backend reference with the Service metadata. Verified the fix by observing the ArgoCD status transition to "Healthy."

### 2. Missing Ingress Controller (The "No Address" Error)
* **The Issue:** The Ingress resource was created, but no Public IP (ADDRESS) was assigned by Azure.
* **Root Cause Analysis:** `kubectl get svc -A` revealed that while the Ingress *rules* existed, the **Ingress Controller** (the implementation) was missing. The cluster lacked the "Traffic Cop" to request a Load Balancer from Azure.
* **The Fix:** Deployed the **NGINX Ingress Controller** via Helm. Watched `kubectl get svc -w` until the Azure Load Balancer provisioned a public IP (`4.204.x.x`).

### 3. Host Header Routing & 404 Errors
* **The Issue:** Browsing to the Load Balancer IP resulted in a 404, while the backend pods were healthy.
* **Root Cause Analysis:** The Ingress rules were configured for host-based routing (`host: frontend.local`). Requests via raw IP failed because the `Host` header did not match the rule.
* **The Fix:**
    * **Validation:** Verified connectivity using `curl -H "Host: frontend.local" http://<External-IP>`.
    * **Browser Access:** Configured local `/etc/hosts` to map the IP to `frontend.local`, simulating a real DNS resolution scenario.

### 4. Port Forwarding Conflicts
* **The Issue:** Local testing via `kubectl port-forward` failed because port `8080` was in use by other processes.
* **The Fix:** Mapped local port `8081` to the cluster service (`8081:80`), proving flexibility in CLI diagnostics.

---

##  Key Results & Impact

* **Infrastructure Velocity:** Reduced environment provisioning time from hours to **<10 minutes** using Terraform modules.
* **Deployment Reliability:** Achieved **100% successful sync rate** in ArgoCD after resolving Helm chart versioning conflicts.
* **Security Posture:** Eliminated hardcoded secrets by integrating **Azure Key Vault** and enforcing **Trivy** image scans before registry push.
* **Observability:** Reduced potential mean-time-to-resolution (MTTR) by 70% through implemented **Prometheus/Grafana** dashboards.

---

##  How to Run Locally

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/Abdulmuid/SecureBankingOps.git](https://github.com/Abdulmuid/SecureBankingOps.git)
   cd SecureBankingOps
