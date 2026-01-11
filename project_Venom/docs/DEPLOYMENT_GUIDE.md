# 🚀 Deployment & Setup Guide - Project Venom

Complete guide for setting up, configuring, and deploying Project Venom across different environments.

## 📋 Table of Contents

1. [Local Development](#local-development)
2. [Environment Configuration](#environment-configuration)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Production Setup](#production-setup)
6. [Troubleshooting](#troubleshooting)

---

## Local Development

### System Requirements

**Minimum:**
- Python 3.10+
- 4GB RAM
- 2GB disk space

**Recommended:**
- Python 3.11+
- 8GB+ RAM
- NVIDIA GPU with CUDA 11.8+
- 10GB disk space

### Windows Setup

```powershell
# 1. Clone repository
git clone https://github.com/Karn0511/jarvis_training.git
cd project_Venom

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
.venv\Scripts\activate

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt

# 6. Create .env file
cp .env.example .env

# 7. Edit .env with your API keys
notepad .env

# 8. Run system
python main.py
```

### Linux/macOS Setup

```bash
# 1. Clone repository
git clone https://github.com/Karn0511/jarvis_training.git
cd project_Venom

# 2. Create virtual environment
python3 -m venv .venv

# 3. Activate virtual environment
source .venv/bin/activate

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt

# 6. Create .env file
cp .env.example .env

# 7. Edit .env with your API keys
nano .env  # or use your preferred editor

# 8. Run system
python main.py
```

---

## Environment Configuration

### Required Environment Variables

```env
# REQUIRED - Get from https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# OPTIONAL - Get from https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Performance
VENOM_BOOST=true        # Enable turbo mode
DEBUG_MODE=false        # Disable debug logging in production
POLL_RATE=0.03         # Async polling interval (seconds)
```

### Optional Configuration

```env
# Server
PORT=8000
HOST=0.0.0.0
STREAMLIT_SERVER_PORT=8501

# Cache
CACHE_ENABLED=true
CACHE_SIZE=2000
CACHE_TTL=600

# Threading
MAX_WORKERS_THREADS=32
MAX_WORKERS_PROCESSES=8
MAX_CONCURRENT_TASKS=15

# Logging
LOG_LEVEL=INFO
LOG_FILE=storage/logs/venom.log

# Voice
TTS_ENGINE=edge
TTS_VOICE=en-US-AriaNeural

# Vision
YOLO_MODEL_SIZE=n

# Environment
ENVIRONMENT=development  # or 'production'
KUBERNETES_ENABLED=false
DOCKER_BUILD=false
```

### Setting Up API Keys

#### Google Gemini API

1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API key"
3. Copy the key
4. Add to `.env`: `GEMINI_API_KEY=your_key`

#### OpenAI API (Optional)

1. Visit: https://platform.openai.com/api-keys
2. Create new secret key
3. Copy the key
4. Add to `.env`: `OPENAI_API_KEY=your_key`

---

## Docker Deployment

### Building Docker Image

```bash
# Build image
docker build -t venom:latest .

# Verify build
docker images | grep venom
```

### Running with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f venom

# Stop services
docker-compose down
```

### Docker Environment

Create `.env.docker`:
```env
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
VENOM_BOOST=true
DEBUG_MODE=false
ENVIRONMENT=production
DOCKER_BUILD=true
```

### Docker Commands

```bash
# Build and run
docker build -t venom:latest .
docker run -d \
  --name venom \
  --env-file .env \
  -p 8000:8000 \
  -p 8501:8501 \
  -v $(pwd)/storage:/app/storage \
  venom:latest

# Access logs
docker logs -f venom

# Stop container
docker stop venom

# Remove container
docker rm venom
```

---

## Kubernetes Deployment

### Prerequisites

- kubectl installed
- Kubernetes cluster (local/cloud)
- Docker registry access

### Deploy to Kubernetes

```bash
# 1. Create namespace
kubectl create namespace venom-system

# 2. Create secrets (replace with your actual keys)
kubectl create secret generic venom-secrets \
  --from-literal=GEMINI_API_KEY=your_key_here \
  --from-literal=OPENAI_API_KEY=your_key_here \
  -n venom-system

# 3. Apply deployment
kubectl apply -f k8s/deployment.yaml

# 4. Verify deployment
kubectl get pods -n venom-system
kubectl get svc -n venom-system

# 5. Get service IP
kubectl get svc venom-backend-service -n venom-system

# 6. Port forward to local machine
kubectl port-forward -n venom-system svc/venom-backend-service 8000:8000
```

### Kubernetes Scaling

```bash
# Scale replicas
kubectl scale deployment venom-backend --replicas=5 -n venom-system

# Check HPA status
kubectl get hpa -n venom-system

# Monitor pods
kubectl top pods -n venom-system
```

### Monitoring Kubernetes Deployment

```bash
# View logs
kubectl logs -f deployment/venom-backend -n venom-system

# Describe deployment
kubectl describe deployment venom-backend -n venom-system

# Check resource usage
kubectl top nodes
kubectl top pods -n venom-system
```

---

## Production Setup

### Security Checklist

- [ ] Use strong API keys
- [ ] Enable HTTPS/TLS
- [ ] Set `DEBUG_MODE=false`
- [ ] Use environment secrets (not files)
- [ ] Enable authentication on API endpoints
- [ ] Set up firewall rules
- [ ] Enable logging and monitoring
- [ ] Regular backups of storage
- [ ] Use separate DB for production
- [ ] Monitor resource usage

### Production Environment Variables

```env
ENVIRONMENT=production
DEBUG_MODE=false
VENOM_BOOST=true
LOG_LEVEL=WARNING
CACHE_ENABLED=true
CACHE_SIZE=5000
CACHE_TTL=3600
```

### Monitoring & Logging

```bash
# View system logs
tail -f storage/logs/venom.log

# Monitor CPU/Memory
python -m modules.analytics

# Stream HUD dashboard
streamlit run frontend/app.py
```

### Backup Strategy

```bash
# Daily backup
tar -czf storage_backup_$(date +%Y%m%d).tar.gz storage/

# Backup to cloud (AWS S3)
aws s3 sync storage/ s3://my-bucket/venom-backups/

# Restore from backup
tar -xzf storage_backup_20240115.tar.gz
```

---

## Troubleshooting

### Common Issues

#### 1. API Key Errors

```
Error: GEMINI_API_KEY not found
```

**Solution:**
```bash
# Verify .env file exists
ls -la .env

# Check key is set
echo $GEMINI_API_KEY

# Update .env and reload
source .venv/bin/activate
python main.py
```

#### 2. CUDA Not Found

```
Error: CUDA not available, using CPU
```

**Solution:**
```bash
# Install CUDA version of PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify CUDA
python -c "import torch; print(torch.cuda.is_available())"
```

#### 3. Port Already in Use

```
Error: Address already in use on port 8000
```

**Solution:**
```bash
# Find process using port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Use different port
PORT=8001 python main.py
```

#### 4. Memory Issues

```
Error: Out of memory
```

**Solution:**
```bash
# Reduce model size
YOLO_MODEL_SIZE=n python main.py

# Reduce cache size
CACHE_SIZE=500 python main.py

# Monitor memory
python -m modules.analytics
```

#### 5. Import Errors

```
ModuleNotFoundError: No module named 'xyz'
```

**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Clear cache
rm -rf __pycache__ .pytest_cache .mypy_cache

# Reinstall venv (nuclear option)
rm -rf .venv
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Debug Mode

```bash
# Enable debug logging
DEBUG_MODE=true python main.py

# Check configuration
python -c "from ai_core.core.config import *; print(locals())"

# Test components
python -c "from modules.vision import VisionSystem; v = VisionSystem(); print(v.active)"
python -c "from modules.voice import VenomVoice; print('Voice OK')"
```

---

## Performance Tuning

### CPU Optimization

```env
VENOM_BOOST=true
MAX_WORKERS_THREADS=16
MAX_CONCURRENT_TASKS=10
POLL_RATE=0.05
```

### GPU Acceleration

```env
VENOM_BOOST=true
YOLO_MODEL_SIZE=m  # Use medium model
# PyTorch will auto-detect CUDA
```

### Memory Optimization

```env
CACHE_SIZE=1000
CACHE_TTL=300
MAX_WORKERS_PROCESSES=4
```

---

## Support & Documentation

- **GitHub Issues**: https://github.com/Karn0511/jarvis_training/issues
- **Documentation**: See `README.md` and docs/
- **Configuration**: See `.env.example`

---

**Last Updated**: January 2026  
**Maintained by**: Karn
