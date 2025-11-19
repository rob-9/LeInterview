# Kubernetes Deployment Guide

This guide covers deploying the interview platform to Kubernetes with secure, scalable code execution.

## Overview

The Kubernetes implementation replaces Docker-based code execution with:

- **Kubernetes Jobs** for isolated code execution
- **Auto-scaling** via Horizontal Pod Autoscaler
- **Resource limits** to prevent resource exhaustion
- **Network policies** for security isolation
- **RBAC** for least-privilege access

## Architecture

```
┌─────────────────────────────────────────────┐
│  Load Balancer / Ingress                    │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│  Flask App Pods (2-10 replicas)             │
│  - HPA: scales based on CPU/Memory          │
│  - Service Account: code-executor           │
└──────────────────┬──────────────────────────┘
                   │
         ┌─────────▼──────────┐
         │ Creates K8s Jobs   │
         └─────────┬──────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
┌───▼───┐    ┌────▼────┐    ┌───▼────┐
│Python │    │  Java   │    │  C++   │
│ Job   │    │  Job    │    │  Job   │
└───────┘    └─────────┘    └────────┘
```

## Prerequisites

1. **Kubernetes cluster** (v1.25+)
   - Minikube, EKS, GKE, AKS, or any managed K8s
2. **kubectl** configured to access your cluster
3. **Docker** (for building images)

## Deployment Steps

### 1. Build and Push Docker Image

```bash
# Build the image
docker build -t interview-platform:latest .

# Tag for your registry
docker tag interview-platform:latest <your-registry>/interview-platform:latest

# Push to registry
docker push <your-registry>/interview-platform:latest
```

Update `k8s/base/deployment.yaml` with your image:
```yaml
image: <your-registry>/interview-platform:latest
```

### 2. Create Kubernetes Resources

```bash
# Create namespace
kubectl apply -f k8s/base/namespace.yaml

# Create RBAC (ServiceAccount, Role, RoleBinding)
kubectl apply -f k8s/base/rbac.yaml

# Create network policies
kubectl apply -f k8s/base/network-policy.yaml

# Create secret for Gemini API key
kubectl create secret generic gemini-secret \
  --from-literal=api-key=YOUR_GEMINI_API_KEY \
  -n interview-platform

# Deploy the application
kubectl apply -f k8s/base/deployment.yaml
```

### 3. Verify Deployment

```bash
# Check pods
kubectl get pods -n interview-platform

# Check HPA
kubectl get hpa -n interview-platform

# Check service
kubectl get svc -n interview-platform

# View logs
kubectl logs -f deployment/interview-platform -n interview-platform
```

### 4. Access the Application

```bash
# Get the LoadBalancer IP (or use port-forward for testing)
kubectl get svc interview-platform-service -n interview-platform

# Or use port-forward for local testing
kubectl port-forward svc/interview-platform-service 8080:80 -n interview-platform
```

Access at: `http://localhost:8080`

## Configuration

### Enable Kubernetes Execution

Set the `USE_KUBERNETES` environment variable in `k8s/base/deployment.yaml`:

```yaml
env:
  - name: USE_KUBERNETES
    value: "true"
```

### Resource Limits

Adjust resources in `k8s/base/deployment.yaml`:

**Flask App:**
```yaml
resources:
  requests:
    cpu: "200m"
    memory: "256Mi"
  limits:
    cpu: "1000m"
    memory: "512Mi"
```

**Code Execution Jobs** (in `k8s/code-runners/*.yaml`):
```yaml
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
```

### Auto-scaling Configuration

Edit HPA settings in `k8s/base/deployment.yaml`:

```yaml
spec:
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70  # Scale at 70% CPU
```

## Monitoring

### Health Checks

```bash
# Health endpoint
curl http://<service-ip>/health

# Metrics endpoint
curl http://<service-ip>/metrics
```

### View Active Jobs

```bash
# List all code execution jobs
kubectl get jobs -n interview-platform -l role=code-executor

# Watch jobs in real-time
kubectl get jobs -n interview-platform -l role=code-executor -w

# View job logs
kubectl logs job/<job-name> -n interview-platform
```

### View Metrics

```bash
# Pod metrics
kubectl top pods -n interview-platform

# Node metrics
kubectl top nodes
```

## Security Features

### 1. Network Isolation
- Code execution pods have **no ingress** traffic allowed
- Egress limited to **DNS only**
- Prevents network-based attacks

### 2. RBAC
- Dedicated `ServiceAccount` for job creation
- Minimal permissions (create/get/list/delete jobs)
- No cluster-wide access

### 3. Pod Security
- `runAsNonRoot: true` - Cannot run as root
- `allowPrivilegeEscalation: false`
- `readOnlyRootFilesystem: true` (Python)
- All capabilities dropped

### 4. Resource Limits
- CPU: 100m-500m per job
- Memory: 128Mi-512Mi per job
- Prevents resource exhaustion attacks

### 5. Job TTL
- Jobs auto-delete after 60 seconds
- Prevents job accumulation

## Troubleshooting

### Jobs Not Creating

```bash
# Check RBAC permissions
kubectl auth can-i create jobs --as=system:serviceaccount:interview-platform:code-executor -n interview-platform

# Check service account
kubectl get sa code-executor -n interview-platform

# Check role bindings
kubectl get rolebinding -n interview-platform
```

### Jobs Failing

```bash
# View job status
kubectl describe job <job-name> -n interview-platform

# View pod logs
kubectl logs -l job-name=<job-name> -n interview-platform

# Check pod events
kubectl get events -n interview-platform --sort-by='.lastTimestamp'
```

### HPA Not Scaling

```bash
# Check metrics server
kubectl get deployment metrics-server -n kube-system

# View HPA status
kubectl describe hpa interview-platform-hpa -n interview-platform

# Install metrics-server if missing
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

## Cost Optimization

### 1. Node Auto-scaling
Configure cluster auto-scaler for cloud providers:

**GKE:**
```bash
gcloud container clusters update CLUSTER_NAME \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=5
```

**EKS:**
```bash
eksctl create cluster \
  --node-type=t3.medium \
  --nodes-min=1 \
  --nodes-max=5
```

### 2. Spot Instances
Use spot/preemptible instances for cost savings:

**Node selector in deployment.yaml:**
```yaml
nodeSelector:
  node.kubernetes.io/instance-type: spot
```

### 3. Resource Quotas
Limit namespace resources:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: interview-platform
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
```

## Production Checklist

- [ ] Set `USE_KUBERNETES=true` environment variable
- [ ] Configure Gemini API key secret
- [ ] Set appropriate resource limits
- [ ] Enable HPA with proper thresholds
- [ ] Configure ingress/LoadBalancer
- [ ] Enable cluster auto-scaling
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Configure logging (ELK/Loki)
- [ ] Enable network policies
- [ ] Review RBAC permissions
- [ ] Set up backup strategy
- [ ] Configure SSL/TLS certificates
- [ ] Test auto-scaling behavior
- [ ] Load test the platform

## Monitoring with Prometheus

Example ServiceMonitor for Prometheus:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: interview-platform-monitor
  namespace: interview-platform
spec:
  selector:
    matchLabels:
      app: interview-platform
  endpoints:
    - port: http
      path: /metrics
      interval: 30s
```

## Benefits Over Docker

| Feature | Docker | Kubernetes |
|---------|--------|------------|
| Auto-scaling | Manual | Automatic (HPA) |
| Resource limits | Per container | Per job + cluster-wide |
| Network isolation | Manual | NetworkPolicy |
| Job queuing | Manual | Built-in |
| High availability | Single instance | Multiple replicas |
| Rolling updates | Manual | Automated |
| Self-healing | Manual restart | Automatic |
| Load balancing | nginx | K8s Service |

## Next Steps

1. Set up CI/CD pipeline for automated deployments
2. Configure monitoring dashboards
3. Set up alerting for critical metrics
4. Implement rate limiting at ingress level
5. Add request authentication/authorization
