# 🚀 Venom AI - Deployment Guide

## Quick Deployment Options

### Option 1: Docker Compose (Recommended for Local/Development)

```powershell
# 1. Build and start all services
docker-compose up -d --build

# 2. Check status
docker-compose ps

# 3. View logs
docker-compose logs -f

# 4. Access services
# - Frontend: http://localhost:4200
# - API: http://localhost:8000
# - HUD Dashboard: http://localhost:8501
```

### Option 2: Kubernetes (Production)

```powershell
# 1. Apply manifests
kubectl apply -f k8s/deployment.yaml

# 2. Check deployment status
kubectl get all -n venom-system

# 3. View logs
kubectl logs -f deployment/venom-backend -n venom-system

# 4. Access services (LoadBalancer IPs)
kubectl get svc -n venom-system
```

### Option 3: Local Development

```powershell
# Quick start script
.\START.ps1

# Or comprehensive launcher
.\LAUNCH_VENOM.ps1

# Or individual components
.\.venv\Scripts\python venom_daemon.py
.\.venv\Scripts\streamlit run venom_hud.py
cd frontend && npm start
```

## 🔒 Security Setup

### Block External Port Access (Windows)

Run as Administrator:
```powershell
powershell -ExecutionPolicy Bypass -File SECURITY_PORTS.ps1
```

This blocks external access to ports 8000, 8501, 4200 (localhost only).

## 📋 Prerequisites

### For Docker:
- Docker Desktop installed
- Docker Compose v2+
- 8GB RAM minimum
- 20GB disk space

### For Kubernetes:
- kubectl installed
- Kubernetes cluster (minikube, Docker Desktop, or cloud)
- KUBE_CONFIG secret configured

### For Local:
- Python 3.10+
- Node.js 20+
- Windows PowerShell 5.1+
- NVIDIA GPU (optional, for CUDA acceleration)

## 🔧 Configuration

### Environment Variables

Create `.env` file in project root:
```env
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here  # Optional
VENOM_BOOST=true
```

### Kubernetes Secrets

```bash
# Create namespace
kubectl create namespace venom-system

# Create secrets
kubectl create secret generic venom-secrets \
  --from-literal=GEMINI_API_KEY=your_key \
  -n venom-system
```

## 📊 Monitoring & Health Checks

### Health Endpoints

- Backend: `http://localhost:8000/health`
- Frontend: `http://localhost:4200/` (should load UI)
- HUD: `http://localhost:8501/` (Streamlit dashboard)

### Docker Health Status

```powershell
docker-compose ps  # Shows health status of containers
```

### Kubernetes Health

```bash
kubectl get pods -n venom-system  # Check pod status
kubectl describe pod <pod-name> -n venom-system  # Detailed info
```

## 🐛 Troubleshooting

### Docker Issues

**Container won't start:**
```powershell
docker-compose logs <service-name>
docker-compose restart <service-name>
```

**Port conflicts:**
```powershell
# Check what's using the port
netstat -ano | findstr :8000
# Kill process
taskkill /PID <process-id> /F
```

**Build cache issues:**
```powershell
docker-compose build --no-cache
docker system prune -a  # Warning: removes all unused images
```

### Kubernetes Issues

**Pods not starting:**
```bash
kubectl describe pod <pod-name> -n venom-system
kubectl logs <pod-name> -n venom-system
```

**Image pull errors:**
```bash
# Check image exists
docker pull ghcr.io/<your-repo>/venom-backend:latest

# Update deployment with correct image
kubectl edit deployment venom-backend -n venom-system
```

**Resource limits:**
```bash
# Check node resources
kubectl top nodes
kubectl top pods -n venom-system
```

### Frontend Issues

**Angular won't load:**
- Check browser console for errors
- Verify Zone.js is imported in `main.ts`
- Clear browser cache (Ctrl+Shift+Del)
- Rebuild: `npm run build`

**API connection fails:**
- Check API is running: `curl http://localhost:8000/health`
- Verify CORS settings in `web_server.py`
- Check nginx proxy config (if using Docker)

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

Located at `.github/workflows/ci-cd.yaml`

**Triggers:**
- Push to `main` branch
- Pull requests to `main`
- Manual workflow dispatch

**Jobs:**
1. **test-backend** - Run Python tests with pytest
2. **test-frontend** - Build Angular app
3. **build-and-push** - Build Docker images, push to GHCR
4. **deploy-k8s** - Deploy to Kubernetes cluster

### Setup GitHub Secrets

Go to repo Settings → Secrets → Actions:

```
KUBE_CONFIG - Base64 encoded kubeconfig file
GEMINI_API_KEY - Your Gemini API key (if needed in CI)
```

Encode kubeconfig:
```powershell
[Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((Get-Content ~/.kube/config -Raw)))
```

## 📈 Performance Tuning

### Configuration Options

Edit `ai_core/core/config.py`:

```python
VENOM_BOOST = True           # Enable turbo mode
CACHE_SIZE = 3000            # Cache capacity
CACHE_TTL = 900              # Cache lifetime (seconds)
MAX_CONNECTIONS = 30         # Connection pool size
MAX_WORKERS_THREADS = 48     # Thread workers
MAX_WORKERS_PROCESSES = 12   # Process workers
POLL_RATE = 0.03             # Polling interval (seconds)
```

### Docker Resource Limits

Edit `docker-compose.yml`:

```yaml
services:
  venom-backend:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 4G
```

### Kubernetes Scaling

```bash
# Manual scaling
kubectl scale deployment venom-backend --replicas=5 -n venom-system

# Auto-scaling (HPA already configured)
kubectl get hpa -n venom-system
```

## 🗑️ Cleanup Commands

### Docker
```powershell
docker-compose down -v  # Stop and remove volumes
docker system prune -a  # Remove all unused data
```

### Kubernetes
```bash
kubectl delete namespace venom-system  # Remove everything
```

### Local
```powershell
Remove-Item storage\logs\* -Recurse -Force
Remove-Item storage\vitals\* -Recurse -Force
.\.venv\Scripts\python -c "from ai_core.core.cache import performance_cache; performance_cache.clear()"
```

## 📚 Additional Resources

- [UPGRADE_SUMMARY.md](UPGRADE_SUMMARY.md) - Complete feature list
- [PERFORMANCE_GUIDE.md](PERFORMANCE_GUIDE.md) - Optimization guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [README.md](README.md) - Project overview

## 🆘 Support

For issues or questions:
1. Check logs first (Docker/K8s commands above)
2. Review health check endpoints
3. Verify environment variables are set
4. Check GitHub Issues for similar problems

---

**Status**: Production Ready v2.0-TURBO
**Last Updated**: January 2025
