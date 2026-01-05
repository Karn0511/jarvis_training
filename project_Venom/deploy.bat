@echo off
REM Self-destructing deployment script for Venom
REM Builds Docker image and optional K8s deployment

setlocal enabledelayedexpansion

echo.
echo ███████╗███████╗ █████╗ ██╗     ██████╗ ███████╗██╗   ██╗
echo ██╔════╝██╔════╝██╔══██╗██║     ██╔══██╗██╔════╝██║   ██║
echo ███████╗███████╗███████║██║     ██║  ██║███████╗██║   ██║
echo ╚════██║╚════██║██╔══██║██║     ██║  ██║╚════██║╚██╗ ██╔╝
echo ███████║███████║██║  ██║███████╗██████╔╝███████║ ╚████╔╝
echo ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚═════╝ ╚══════╝  ╚═══╝
echo.

echo [DEPLOY] Venom AI Deployment Script
echo.

:menu
echo Select deployment target:
echo 1. Docker (docker-compose up)
echo 2. Kubernetes (kubectl apply)
echo 3. Build Docker Image Only
echo 4. Exit
echo.

set /p choice="Enter choice (1-4): "

if "%choice%"=="1" goto docker
if "%choice%"=="2" goto k8s
if "%choice%"=="3" goto build
if "%choice%"=="4" goto cleanup
echo Invalid choice. Try again.
goto menu

:docker
echo [DOCKER] Checking Docker Desktop...
docker ps >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Desktop not running. Please start it first.
    goto menu
)
echo [DOCKER] Building image...
docker-compose build
echo [DOCKER] Starting services...
docker-compose up -d
echo [DOCKER] ✓ Services deployed at http://localhost:8000
goto menu

:k8s
echo [K8S] Checking kubectl...
kubectl cluster-info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Kubernetes cluster not accessible.
    goto menu
)
echo [K8S] Building Docker image first...
docker build -t venom:latest .
echo [K8S] Loading image into cluster...
docker-compose up --no-start >nul 2>&1
echo [K8S] Deploying to Kubernetes...
kubectl apply -f k8s/deployment.yaml
echo [K8S] ✓ Deployment applied
echo [K8S] Watch status: kubectl get pods -n venom-system -w
goto menu

:build
echo [BUILD] Building Docker image...
docker build -t venom:latest .
echo [BUILD] ✓ Image ready: venom:latest
goto menu

:cleanup
echo [CLEANUP] Self-destructing deployment script...
timeout /t 2 /nobreak
del /f /q "%~f0" 2>nul
exit /b 0
