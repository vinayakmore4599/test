# Kubernetes Setup Guide

## Prerequisites
- Docker image built and pushed to a registry
- `kubectl` installed and configured
- A Kubernetes cluster (local or cloud)

## Local Kubernetes Setup (macOS)

### Option 1: Docker Desktop (Easiest)
1. Open Docker Desktop
2. Go to Preferences → Kubernetes
3. Check "Enable Kubernetes"
4. Wait for it to start

### Option 2: Minikube
```bash
# Install minikube
brew install minikube

# Start minikube
minikube start

# Point Docker to minikube
eval $(minikube docker-env)
```

## Building and Pushing Docker Image

```bash
# Build the image
docker build -t flask-app:latest .

# For Docker Desktop: Tag for local use
docker tag flask-app:latest flask-app:latest

# For remote registry (e.g., Docker Hub):
docker tag flask-app:latest yourusername/flask-app:latest
docker push yourusername/flask-app:latest
```

## Deploying to Kubernetes

### 1. Update the image reference (if using registry)
Edit `k8s/deployment.yaml` and change:
```yaml
image: flask-app:latest  # Change to yourusername/flask-app:latest
```

### 2. Update the API key secret
Edit `k8s/secret.yaml` and replace `your-api-key-here` with your actual Perplexity API key.

### 3. Deploy all manifests
```bash
# Deploy everything in order
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa.yaml

# Or deploy all at once
kubectl apply -f k8s/
```

### 4. Verify deployment
```bash
# Check namespace
kubectl get ns

# Check pods
kubectl get pods -n flask-app

# Check services
kubectl get svc -n flask-app

# Check deployment status
kubectl describe deployment flask-app -n flask-app

# View logs
kubectl logs -n flask-app deployment/flask-app

# Stream logs
kubectl logs -n flask-app deployment/flask-app -f
```

## Accessing the Application

### Docker Desktop
The service is accessible at `http://localhost` (LoadBalancer auto-maps to localhost)

### Minikube
```bash
# Get the service URL
minikube service flask-app-service -n flask-app

# Or manually
minikube ip  # Get the IP
# Then access at http://<minikube-ip>
```

## Port Forwarding (Alternative)
```bash
kubectl port-forward -n flask-app svc/flask-app-service 8080:80
# Access at http://localhost:8080
```

## Useful Commands

```bash
# Get all resources in namespace
kubectl get all -n flask-app

# Describe a pod
kubectl describe pod <pod-name> -n flask-app

# Execute command in pod
kubectl exec -it <pod-name> -n flask-app -- /bin/bash

# Scale deployment
kubectl scale deployment flask-app --replicas=3 -n flask-app

# Update image
kubectl set image deployment/flask-app flask-app=yourusername/flask-app:v1.1 -n flask-app

# Rollout history
kubectl rollout history deployment/flask-app -n flask-app

# Rollback
kubectl rollout undo deployment/flask-app -n flask-app

# Delete deployment
kubectl delete -f k8s/ -n flask-app
```

## Environment Variables

The following environment variables are configured:

### ConfigMap (public config)
- `FLASK_ENV`: production
- `FLASK_DEBUG`: False

### Secret (sensitive data)
- `PERPLEXITY_API_KEY`: Your API key

To update secrets without redeploying:
```bash
kubectl set env secret/flask-app-secret PERPLEXITY_API_KEY=new-key-here -n flask-app
```

## Auto-scaling

The HPA is configured to:
- Scale between 2-5 replicas
- Scale up when CPU usage > 70%
- Scale up when memory usage > 80%

To monitor scaling:
```bash
kubectl get hpa -n flask-app -w
```

## Troubleshooting

### Pod won't start
```bash
kubectl describe pod <pod-name> -n flask-app
kubectl logs <pod-name> -n flask-app
```

### Image pull errors
- Ensure image is available locally or in registry
- Check image name in deployment.yaml
- For local images: use `imagePullPolicy: Never`

### Service not accessible
```bash
# Check service
kubectl get svc -n flask-app

# Port forward to test
kubectl port-forward svc/flask-app-service 8080:80 -n flask-app
```

### API key errors
```bash
# Verify secret
kubectl get secret flask-app-secret -n flask-app -o yaml

# Update secret
kubectl set env secret/flask-app-secret PERPLEXITY_API_KEY=<new-key> -n flask-app
```
