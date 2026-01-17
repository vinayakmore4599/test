# Flask Application - Docker & Kubernetes Deployment

A complete guide for deploying a Flask application using Docker and Kubernetes.

## Quick Start Commands (In Chronological Order)

### 1. Git: Initial Setup and Configuration

#### Configure Git Identity
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### Verify Configuration
```bash
git config --list
```

---

### 2. Git: Initialize Repository and Add Remote

#### Initialize Git
```bash
git init
```

#### Add Remote Repository
```bash
git remote add origin https://github.com/username/repository.git
```

#### Verify Remote
```bash
git remote -v
```

---

### 3. Docker: Build and Push Image

#### Build Docker Image
```bash
docker build -t vinumore/test_vin:latest .
```

#### Push to Docker Hub
```bash
docker push vinumore/test_vin:latest
```

---

### 4. Update Kubernetes Configuration

#### Update deployment.yaml with Docker Image
Edit `k8s/deployment.yaml` and change:
```yaml
image: vinumore/test_vin:latest
```

---

### 5. Deploy to Kubernetes

#### Create Namespace First
```bash
kubectl apply -f k8s/namespace.yaml && sleep 2
```

#### Apply ConfigMap
```bash
kubectl apply -f k8s/configmap.yaml
```

#### Apply Secrets
```bash
kubectl apply -f k8s/secret.yaml
```

#### Apply Deployment
```bash
kubectl apply -f k8s/deployment.yaml
```

#### Apply Service
```bash
kubectl apply -f k8s/service.yaml
```

#### Apply Ingress
```bash
kubectl apply -f k8s/ingress.yaml
```

#### Apply HPA (Auto-scaling)
```bash
kubectl apply -f k8s/hpa.yaml
```

#### Deploy All at Once (After First Deployment)
```bash
kubectl apply -f k8s/
```

---

### 6. Verify Kubernetes Deployment

#### Check All Resources
```bash
kubectl get all -n flask-app
```

#### Check Pods Status
```bash
kubectl get pods -n flask-app
```

#### Check Deployment Details
```bash
kubectl describe deployment flask-app -n flask-app
```

#### View Application Logs
```bash
kubectl logs -n flask-app deployment/flask-app
```

#### Stream Logs in Real-time
```bash
kubectl logs -n flask-app deployment/flask-app -f
```

#### Check Services
```bash
kubectl get svc -n flask-app
```

#### Check Ingress
```bash
kubectl get ingress -n flask-app
```

#### Check HPA Status
```bash
kubectl get hpa -n flask-app
```

---

### 7. Access the Application

#### Port Forward to Local Machine
```bash
kubectl port-forward -n flask-app svc/flask-app-service 8080:80
```

#### Access Application
- Open browser: `http://localhost:8080`

---

### 8. Git: Stage, Commit, and Push Changes

#### Check Status
```bash
git status
```

#### Stage All Changes
```bash
git add .
```

#### Create .gitignore for Sensitive Files
```bash
echo "k8s/secret.yaml" >> .gitignore
echo ".env" >> .gitignore
git add .gitignore
```

#### Commit Changes
```bash
git commit -m "Chore: Add sensitive files to .gitignore"
```

#### Push to Remote
```bash
git push origin main
```

---

### 9. Git: Handle Secrets Already in History

If you accidentally committed sensitive files, remove them from history:

#### Remove Files from All Commits
```bash
git filter-branch --tree-filter 'rm -f .env.example k8s/secret.yaml' HEAD
```

#### Force Push to Update Remote
```bash
git push --force-with-lease
```

---

### 10. Monitoring and Scaling

#### Watch Auto-scaling
```bash
kubectl get hpa -n flask-app -w
```

#### Scale Manually
```bash
kubectl scale deployment flask-app --replicas=5 -n flask-app
```

#### Check Deployment Replicas
```bash
kubectl get deployment flask-app -n flask-app
```

---

### 11. Cleanup and Shutdown

#### Stop Port Forwarding
```bash
kill %1
```

#### Delete All Resources
```bash
kubectl delete -f k8s/ -n flask-app
```

#### Delete Entire Namespace
```bash
kubectl delete namespace flask-app
```

#### Verify Everything is Stopped
```bash
kubectl get pods -n flask-app
kubectl get ns | grep flask-app
```

---

## Complete Workflow Summary

```
1. Build Docker Image
   └─> docker build -t vinumore/test_vin:latest .

2. Push to Docker Hub
   └─> docker push vinumore/test_vin:latest

3. Update k8s/deployment.yaml
   └─> image: vinumore/test_vin:latest

4. Deploy to Kubernetes
   └─> kubectl apply -f k8s/namespace.yaml && sleep 2
   └─> kubectl apply -f k8s/

5. Verify Deployment
   └─> kubectl get all -n flask-app
   └─> kubectl logs -n flask-app deployment/flask-app

6. Access Application
   └─> kubectl port-forward -n flask-app svc/flask-app-service 8080:80
   └─> http://localhost:8080

7. Git: Manage Source Code
   └─> git add .
   └─> git commit -m "message"
   └─> git push origin main

8. Cleanup
   └─> kill %1
   └─> kubectl delete -f k8s/ -n flask-app
```

---

## File Structure

```
.
├── app.py                          # Flask application
├── Dockerfile                      # Docker image definition
├── requirements.txt                # Python dependencies
├── docker-compose.yml              # Docker Compose config
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
├── DEPLOYMENT_GUIDE.md             # Detailed deployment guide
├── GIT_GUIDE.md                    # Git commands reference
├── K8S_SETUP.md                    # Kubernetes setup guide
├── templates/
│   └── index.html                  # Web template
└── k8s/
    ├── namespace.yaml              # Kubernetes namespace
    ├── deployment.yaml             # Kubernetes deployment
    ├── service.yaml                # Kubernetes service
    ├── configmap.yaml              # Configuration
    ├── secret.yaml                 # Secrets (DO NOT COMMIT)
    ├── ingress.yaml                # Ingress routing
    └── hpa.yaml                    # Auto-scaling policy
```

---

## Key Tools Used

| Tool | Purpose | Command |
|------|---------|---------|
| **Docker** | Build container images | `docker build`, `docker push` |
| **Kubernetes** | Orchestrate containers | `kubectl apply`, `kubectl get` |
| **kubectl** | CLI for Kubernetes | `kubectl logs`, `kubectl port-forward` |
| **Git** | Version control | `git push`, `git commit` |
| **Docker Hub** | Container registry | Docker image storage |
| **GitHub** | Code repository | Source code management |

---

## Environment Variables

### ConfigMap (Public)
- `FLASK_ENV=production`
- `FLASK_DEBUG=False`

### Secret (Sensitive - DO NOT COMMIT)
- `PERPLEXITY_API_KEY=<your-api-key>`

---

## Important Notes

### Security
- Never commit `k8s/secret.yaml` to git
- Add to `.gitignore`: `echo "k8s/secret.yaml" >> .gitignore`
- If accidentally committed, use `git filter-branch` to remove from history

### Docker Hub
- Image: `vinumore/test_vin:latest`
- Registry: Docker Hub
- Authentication: `docker login`

### Kubernetes
- Namespace: `flask-app`
- Replicas: 2 (min: 2, max: 5 with HPA)
- Port: 8000 (internal), 80 (service), 8080 (port-forward)

### Git
- Main branch: `main`
- Remote: `origin`
- Always use `--force-with-lease` instead of `--force`

---

## Related Documentation

- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Step-by-step deployment instructions
- [Git Guide](GIT_GUIDE.md) - Comprehensive Git commands reference
- [Kubernetes Setup](K8S_SETUP.md) - Kubernetes configuration details
- [Docker Guide](README.Docker.md) - Docker-specific instructions
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues and solutions

---

## Contact & Support

For issues or questions, refer to the troubleshooting guides or check the logs:

```bash
kubectl logs -n flask-app deployment/flask-app -f
```