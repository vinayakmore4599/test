# Docker to Kubernetes Deployment Guide

This document outlines the complete process of building a Docker image and deploying it to Kubernetes.

## Step 1: Build Docker Image

Build the Docker image from the Dockerfile in your project directory.

```bash
docker build -t vinumore/test_vin:latest .
```

**What happens:**
- Docker reads the `Dockerfile` in the current directory
- Creates a container image with your Flask application
- Tags it as `vinumore/test_vin:latest`
- Uses Python 3.9.6 as the base image
- Installs dependencies from `requirements.txt`

## Step 2: Push Image to Docker Registry

Push the built image to Docker Hub (or your preferred registry).

```bash
docker push vinumore/test_vin:latest
```

**What happens:**
- Authenticates with Docker Hub (must be logged in via `docker login`)
- Uploads the image to your Docker Hub repository
- Makes it publicly available for Kubernetes to pull

## Step 3: Update Kubernetes Deployment

Update the `k8s/deployment.yaml` file to reference your Docker image.

Change from:
```yaml
image: flask-app:latest  # Local image
```

To:
```yaml
image: vinumore/test_vin:latest  # Your Docker Hub image
```

**Why:**
- Tells Kubernetes which image to pull and run in containers
- Must match the exact image name and tag from your registry

## Step 4: Deploy Kubernetes Manifests

Apply all Kubernetes configuration files to your cluster.

```bash
# Option 1: Deploy in order (recommended for first time)
kubectl apply -f k8s/namespace.yaml && sleep 2
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa.yaml

# Option 2: Deploy all at once (after first deployment)
kubectl apply -f k8s/
```

**What each file does:**
- **namespace.yaml**: Creates isolated namespace `flask-app`
- **configmap.yaml**: Stores public configuration (FLASK_ENV, FLASK_DEBUG)
- **secret.yaml**: Stores sensitive data (PERPLEXITY_API_KEY)
- **deployment.yaml**: Defines pod replicas and container specs
- **service.yaml**: Exposes app internally and externally
- **ingress.yaml**: Routes external traffic to your service
- **hpa.yaml**: Auto-scales based on CPU/memory usage

## Step 5: Verify Deployment

Check that all resources are running correctly.

```bash
# View all resources in namespace
kubectl get all -n flask-app

# Check pod status
kubectl get pods -n flask-app

# View deployment details
kubectl describe deployment flask-app -n flask-app

# Check logs
kubectl logs -n flask-app deployment/flask-app

# Watch logs in real-time
kubectl logs -n flask-app deployment/flask-app -f
```

**Expected output:**
- Pods should show as `Running`
- Replicas should match desired count (2 by default)
- Service should have a Cluster IP assigned
- No error messages in logs

## Step 6: Access the Application

Use port forwarding to access your application locally.

```bash
kubectl port-forward -n flask-app svc/flask-app-service 8080:80
```

**Access at:** http://localhost:8080

## Complete Workflow Summary

```
┌─────────────────────────────────────┐
│ 1. Build Docker Image               │
│    docker build -t image:tag .      │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│ 2. Push to Registry                 │
│    docker push image:tag            │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│ 3. Update deployment.yaml           │
│    Change image reference           │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│ 4. Deploy to Kubernetes             │
│    kubectl apply -f k8s/            │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│ 5. Verify Deployment                │
│    kubectl get pods -n flask-app    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│ 6. Access Application               │
│    Port forward & access localhost  │
└─────────────────────────────────────┘
```

## Key Files

- **Dockerfile**: Defines how to build the image
- **requirements.txt**: Python dependencies
- **k8s/deployment.yaml**: Kubernetes deployment configuration
- **k8s/service.yaml**: Service that exposes your application
- **k8s/configmap.yaml**: Non-sensitive environment variables
- **k8s/secret.yaml**: Sensitive data like API keys

## Troubleshooting

### Pods won't start
```bash
kubectl describe pod <pod-name> -n flask-app
kubectl logs <pod-name> -n flask-app
```

### Image pull errors
- Ensure image is available in your Docker Hub account
- Verify the image name matches exactly in deployment.yaml
- Check internet connectivity to Docker Hub

### Service not accessible
```bash
# Test with port forwarding
kubectl port-forward svc/flask-app-service 8080:80 -n flask-app

# Check service endpoints
kubectl get endpoints -n flask-app
```

### API key not working
```bash
# Update the secret
kubectl set env secret/flask-app-secret PERPLEXITY_API_KEY=<new-key> -n flask-app
```

## Useful Commands

```bash
# Get all resources
kubectl get all -n flask-app

# Get specific pod
kubectl get pods -n flask-app

# Get deployment status
kubectl get deployment flask-app -n flask-app

# Describe deployment
kubectl describe deployment flask-app -n flask-app

# Scale deployment
kubectl scale deployment flask-app --replicas=5 -n flask-app

# Delete deployment
kubectl delete -f k8s/ -n flask-app
```

## Environment Variables

The application uses two sources for configuration:

**ConfigMap (k8s/configmap.yaml):**
- `FLASK_ENV=production`
- `FLASK_DEBUG=False`

**Secret (k8s/secret.yaml):**
- `PERPLEXITY_API_KEY=<your-api-key>`

## Auto-scaling

HPA (Horizontal Pod Autoscaler) is configured to:
- Scale between 2-5 replicas
- Scale up when CPU usage > 70%
- Scale up when memory usage > 80%

Monitor with:
```bash
kubectl get hpa -n flask-app -w
```

## Stopping Everything

### Stop Port Forwarding

```bash
kill %1
```

Or if you need to find the process:
```bash
lsof -i :8080
kill <PID>
```

### Delete All Kubernetes Resources

Delete all resources in the namespace:
```bash
kubectl delete -f k8s/ -n flask-app
```

Or delete the entire namespace (removes everything inside it):
```bash
kubectl delete namespace flask-app
```

### Complete Shutdown (All at Once)

Stop port forwarding and delete all resources:
```bash
kill %1 && kubectl delete -f k8s/ -n flask-app
```

### Verify Everything is Stopped

Check if resources are gone:
```bash
# Check if pods are gone
kubectl get pods -n flask-app

# Check if namespace still exists
kubectl get ns | grep flask-app

# Verify no services running
kubectl get svc -n flask-app
```

### Important Notes

- **Deleting the namespace** removes everything (pods, services, deployments, configmaps, secrets, etc.)
- **Deleting resources individually** is slower but gives more control
- To **keep the namespace but delete resources**, use `kubectl delete -f k8s/`
- To **stop and restart later**, use `delete` (resources are gone but can be redeployed easily)
