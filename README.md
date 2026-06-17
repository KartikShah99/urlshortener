# URL Shortener — Full Stack GitOps Project

## Stack
- **Backend**: FastAPI + PostgreSQL + Redis + Celery
- **Frontend**: Next.js
- **CI/CD**: GitHub Actions
- **GitOps**: Argo CD
- **Packaging**: Helm
- **Runtime**: k3s on EC2

## Setup Steps

### 1. Before pushing — update these values

In `helm/urlshortener/values.yaml`:
- Replace `DOCKERHUB_USERNAME` with your actual Docker Hub username (2 places)
- Replace `13.203.59.255` with your actual EC2 IP

In `argocd/app-dev.yaml`:
- Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username

### 2. Add GitHub Secrets
Go to repo Settings → Secrets and variables → Actions:
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

Enable: Settings → Actions → General → Workflow permissions → Read and write permissions

### 3. Push to GitHub
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 4. On EC2 — install Argo CD (if not already done)
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml --server-side
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "NodePort"}}'
```

### 5. Apply Argo CD Application
```bash
kubectl apply -f argocd/app-dev.yaml
```

### 6. Watch deployment
```bash
kubectl get pods -n urlshortener-dev -w
```

### 7. Access
- Frontend: http://13.203.59.255.nip.io
- Backend API: http://api.13.203.59.255.nip.io
- Flower (Celery monitor): http://flower.13.203.59.255.nip.io

## Test the API directly
```bash
# Shorten a URL
curl -X POST http://api.13.203.59.255.nip.io/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'

# Get stats
curl http://api.13.203.59.255.nip.io/api/stats/<short_code>

# Health check
curl http://api.13.203.59.255.nip.io/health
```
