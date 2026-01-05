#!/bin/bash
# Self-destructing deployment script for Venom (Linux/macOS)
# Builds Docker image and optional K8s deployment

set -e

cat << 'EOF'
███████╗███████╗ █████╗ ██╗     ██████╗ ███████╗██╗   ██╗
██╔════╝██╔════╝██╔══██╗██║     ██╔══██╗██╔════╝██║   ██║
███████╗███████╗███████║██║     ██║  ██║███████╗██║   ██║
╚════██║╚════██║██╔══██║██║     ██║  ██║╚════██║╚██╗ ██╔╝
███████║███████║██║  ██║███████╗██████╔╝███████║ ╚████╔╝
╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚═════╝ ╚══════╝  ╚═══╝
EOF

echo "[DEPLOY] Venom AI Deployment Script"
echo ""

menu() {
    echo "Select deployment target:"
    echo "1. Docker (docker-compose up)"
    echo "2. Kubernetes (kubectl apply)"
    echo "3. Build Docker Image Only"
    echo "4. Exit"
    echo ""
    read -p "Enter choice (1-4): " choice

    case $choice in
        1) docker_deploy ;;
        2) k8s_deploy ;;
        3) build_image ;;
        4) cleanup ;;
        *) echo "Invalid choice"; menu ;;
    esac
}

docker_deploy() {
    echo "[DOCKER] Checking Docker..."
    if ! docker ps > /dev/null 2>&1; then
        echo "[ERROR] Docker not running"
        menu
        return
    fi
    echo "[DOCKER] Building image..."
    docker-compose build
    echo "[DOCKER] Starting services..."
    docker-compose up -d
    echo "[DOCKER] ✓ Services deployed at http://localhost:8000"
    menu
}

k8s_deploy() {
    echo "[K8S] Checking kubectl..."
    if ! kubectl cluster-info > /dev/null 2>&1; then
        echo "[ERROR] Kubernetes cluster not accessible"
        menu
        return
    fi
    echo "[K8S] Building Docker image..."
    docker build -t venom:latest .
    echo "[K8S] Deploying to Kubernetes..."
    kubectl apply -f k8s/deployment.yaml
    echo "[K8S] ✓ Deployment applied"
    echo "[K8S] Watch status: kubectl get pods -n venom-system -w"
    menu
}

build_image() {
    echo "[BUILD] Building Docker image..."
    docker build -t venom:latest .
    echo "[BUILD] ✓ Image ready: venom:latest"
    menu
}

cleanup() {
    echo "[CLEANUP] Self-destructing..."
    sleep 2
    rm -f "$0"
    exit 0
}

menu
