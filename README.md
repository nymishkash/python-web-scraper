# Python Web Scraper - DevOps CI/CD Project

A Python-based web scraper demonstrating advanced DevOps practices with a security-first CI pipeline and Kubernetes-based CD pipeline.

## 📋 Project Overview

This project implements a **two-pipeline architecture**: a security-first CI pipeline that produces a trusted container image, and a separate CD pipeline that deploys the image to Kubernetes. This separation reflects real-world DevOps practices and enforces promotion-based delivery.

### Why This Application?

- **Stateless workload** → Ideal for containerization
- **No database dependencies** → Simple Kubernetes deployment
- **Real dependencies** → Strong Software Composition Analysis (SCA) story
- **Network-facing** → Security relevance for SAST/DAST

> **Note**: This project focuses on **CI/CD maturity and security practices**, not application complexity. The Kubernetes deployment demonstrates operational readiness, not scale.

---

## 🏗️ Repository Structure

```
project-root/
├── scraper/
│   ├── __init__.py
│   └── main.py              # Main scraper application
├── tests/
│   └── test_int_extractor.py  # Unit tests
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container definition
├── k8s/
│   ├── deployment.yaml     # Kubernetes deployment
│   └── service.yaml        # Kubernetes service
├── .github/
│   └── workflows/
│       ├── ci.yml          # CI pipeline
│       └── cd.yml          # CD pipeline
├── README.md
└── .gitignore
```

---

## 🔄 CI Pipeline (`.github/workflows/ci.yml`)

### Trigger
- Push to `main` branch
- Manual `workflow_dispatch`

### Pipeline Stages (Strict Order)

#### 1. **Checkout**
- Clones repository using `actions/checkout@v4`

#### 2. **Setup Python Runtime**
- Uses `actions/setup-python@v5`
- Python 3.11 with pip caching

#### 3. **Dependency Installation**
- Installs packages from `requirements.txt`
- Upgrades pip to latest version

#### 4. **Linting**
- Runs `flake8` for code quality
- Checks style and basic code issues
- Max line length: 100 characters

#### 5. **SAST (Static Application Security Testing)**
- **Tool**: GitHub CodeQL
- **Language**: Python
- Scans source code for security vulnerabilities
- Findings visible in GitHub Security tab
- Automated analysis on every push

#### 6. **SCA (Software Composition Analysis)**
- **Tool**: `pip-audit`
- Scans dependencies for known vulnerabilities
- **Fails on High/Critical** vulnerabilities
- Generates JSON report for tracking

#### 7. **Unit Tests**
- **Tool**: `pytest`
- Runs test suite in `tests/`
- Tests `int_extractor` function with various inputs
- Verbose output for debugging

#### 8. **Docker Build**
- Builds container image using Docker Buildx
- Tags with commit SHA and `latest`
- Uses GitHub Actions cache for faster builds
- Image: `docker.io/<username>/web-scraper:<sha>`

#### 9. **Container Image Scan**
- **Tool**: Trivy
- Scans built image for CVEs
- **Fails on High/Critical** vulnerabilities
- Outputs SARIF format for GitHub Security tab
- Checks both OS packages and application dependencies

#### 10. **Runtime Smoke Test**
- Validates container is runnable
- Tests that `int_extractor` function works in container
- Ensures build success ≠ runnable container
- Runs: `docker run --rm <image> python -c "from scraper.main import int_extractor; assert int_extractor('Rs. 999') == 999"`

#### 11. **DockerHub Push**
- Authenticates with DockerHub using GitHub Secrets
- Pushes image with commit SHA tag
- Also tags as `latest`
- Image is now available for deployment

### Security Gates

| Stage | Tool | Failure Condition |
|-------|------|-------------------|
| SAST | CodeQL | Security findings in code |
| SCA | pip-audit | High/Critical in dependencies |
| Container Scan | Trivy | High/Critical in image |

### Required GitHub Secrets

- `DOCKERHUB_USERNAME` - DockerHub username
- `DOCKERHUB_TOKEN` - DockerHub access token

> ⚠️ **Never hardcode secrets** - Always use GitHub Secrets

---

## 🚀 CD Pipeline (`.github/workflows/cd.yml`)

### Trigger
- Manual `workflow_dispatch`
- **OR** automatic after CI pipeline succeeds on `main` branch

> 📌 **CD must not bypass CI** - Deployment only happens after successful CI

### Pipeline Stages

#### 1. **Checkout**
- Clones repository

#### 2. **Setup kubectl**
- Installs kubectl using `azure/setup-kubectl@v3`
- Latest stable version

#### 3. **Configure kubeconfig**
- Sets up Kubernetes cluster access
- Uses `KUBE_CONFIG` secret (base64-encoded kubeconfig)
- Validates configuration

#### 4. **Deploy Manifests**
- Substitutes `IMAGE_TAG` in `deployment.yaml`
- Uses image built by CI pipeline
- Applies deployment and service manifests
- Uses `kubectl apply` for idempotent operations

#### 5. **Verify Pod Status**
- Waits for deployment rollout (300s timeout)
- Checks pod status
- Verifies service is created
- Shows deployment details

#### 6. **DAST (Dynamic Application Security Testing)**
- **Conceptual/Adapted DAST** for non-HTTP application
- Verifies container runtime
- Checks non-root user execution
- Validates pod health
- Documents approach for non-HTTP services

> **Note**: Traditional DAST tools (OWASP ZAP, Burp Suite) target HTTP endpoints. Since this is a CLI scraper, DAST is demonstrated at a conceptual level to show awareness of runtime security testing.

### Required GitHub Secrets

- `KUBE_CONFIG` - Base64-encoded Kubernetes kubeconfig file

---

## ☸️ Kubernetes Deployment

### Scope (Intentionally Simple)

- **Single Deployment** - 1 replica
- **Single Service** - ClusterIP type
- **No Ingress** - Internal access only
- **No Autoscaling** - Fixed replica count
- **No Helm** - Plain YAML manifests

> This is a **delivery demo**, not infrastructure engineering. Focus is on deployment verification, not scale.

### Resources

#### Deployment (`k8s/deployment.yaml`)
- Uses image from DockerHub (built by CI)
- Resource limits: 256Mi memory, 500m CPU
- Non-root user (handled by Dockerfile)
- Stateless pod design

#### Service (`k8s/service.yaml`)
- ClusterIP service
- Exposes port 8080
- Minimal configuration

### Cluster Requirements

You can use:
- **kind** (local Kubernetes)
- **minikube** (local development)
- **Cloud free-tier cluster** (GKE, EKS, AKS)

The evaluator cares about:
- ✅ Pipeline logic
- ✅ Deployment verification
- ✅ Clear explanation

The evaluator does NOT care about:
- ❌ High availability
- ❌ Load testing
- ❌ Production-grade infrastructure

---

## 🧪 Local Development

### Prerequisites
- Python 3.11+
- pip
- Docker (for container testing)

### Setup

```bash
# Clone repository
git clone <repo-url>
cd python-web-scraper

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run application
python -m scraper.main
```

### Docker Testing

```bash
# Build image
docker build -t web-scraper:local .

# Run smoke test
docker run --rm web-scraper:local python -c "from scraper.main import int_extractor; assert int_extractor('Rs. 999') == 999; print('✓ Test passed')"
```

### Kubernetes Testing (Local)

```bash
# Using kind
kind create cluster
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Check status
kubectl get pods
kubectl get svc
```

---

## 📊 Failure Scenarios

### CI Pipeline Failures

| Stage | Failure Reason | Action |
|-------|---------------|--------|
| Linting | Code style issues | Fix style violations |
| SAST | Security vulnerability | Review CodeQL findings |
| SCA | High/Critical CVE | Update vulnerable dependency |
| Tests | Test failure | Fix failing tests |
| Container Scan | High/Critical CVE | Update base image or dependencies |
| Smoke Test | Container won't run | Check Dockerfile and dependencies |

### CD Pipeline Failures

| Stage | Failure Reason | Action |
|-------|---------------|--------|
| Kubeconfig | Invalid credentials | Verify `KUBE_CONFIG` secret |
| Deploy | Image not found | Ensure CI completed successfully |
| Verify | Pod won't start | Check pod logs: `kubectl logs <pod-name>` |

---

## 🎓 Viva Defense Points

### Why CI and CD are Separate?

**Answer**: Separation of concerns. CI validates code quality, security, and produces trusted artifacts. CD consumes those artifacts and deploys them. This reflects real-world promotion-based delivery where artifacts are built once and deployed many times.

### Why Kubernetes is in CD, not CI?

**Answer**: Deployment is a delivery concern, not a build concern. CI focuses on validation and artifact creation. CD focuses on operational deployment. Mixing them would violate single responsibility and make pipelines harder to maintain.

### Why is Deployment Simple?

**Answer**: This project demonstrates operational readiness and deployment maturity, not infrastructure engineering. A single replica deployment proves the application can run in Kubernetes. Production concerns (HA, autoscaling) are out of scope.

### Why is DAST Optional?

**Answer**: Traditional DAST targets HTTP endpoints. This CLI scraper doesn't expose HTTP services. The DAST stage demonstrates awareness of runtime security testing at a conceptual level, which is acceptable when explained.

### Why is a Scraper Valid for This Project?

**Answer**: 
- **Stateless** → Perfect for containers
- **Real dependencies** → Strong SCA story (requests, beautifulsoup4)
- **Network-facing** → Security relevance
- **Testable** → Unit tests validate core logic
- **Simple** → Focus stays on CI/CD, not app complexity

---

## 🔒 Security Best Practices

1. **No secrets in code** - All secrets via GitHub Secrets
2. **Non-root container** - Dockerfile uses non-root user
3. **Multi-stage build** - Minimal final image
4. **Security scanning** - SAST, SCA, and container scanning
5. **Fail on High/Critical** - Security gates prevent vulnerable deployments

---

## 📝 License

This project is for educational/demonstration purposes.

---

## 🤝 Contributing

This is a DevOps demonstration project. For questions or improvements, please open an issue.

---

**Last Updated**: 2024
