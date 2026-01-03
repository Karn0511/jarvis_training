# 🚀 Project Venom CI/CD Guide

## 📋 Overview

This document describes the CI/CD pipeline for Project Venom, designed for the GitHub repository: `https://github.com/Karn0511/jarvis_training`

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Code Push/PR                            │
└────────────────────────┬────────────────────────────────────┘
                         │
           ┌─────────────┴──────────────┐
           │                            │
           ▼                            ▼
    ┌──────────────┐           ┌───────────────┐
    │  CI Pipeline │           │  Security     │
    │  (Test/Lint) │           │  Scanning     │
    └──────┬───────┘           └───────┬───────┘
           │                           │
           └───────────┬───────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Docker Build   │
              │  & Push to      │
              │  GitHub Registry│
              └────────┬────────┘
                       │
           ┌───────────┴────────────┐
           │                        │
           ▼                        ▼
    ┌─────────────┐         ┌──────────────┐
    │   Staging   │         │  Production  │
    │ Deployment  │────────▶│  Deployment  │
    └─────────────┘         └──────────────┘
```

## 📦 Workflows

### 1. **CI - Test & Lint** (`ci.yml`)

**Trigger**: Push to `main`/`develop`, Pull Requests

**Jobs**:
- ✅ **Test Matrix**: Runs tests on Python 3.10, 3.11, 3.12
- 🧹 **Code Quality**: Black formatting, Pylint, MyPy type checking
- 📊 **Coverage**: Generates code coverage reports and uploads to Codecov
- 🔒 **Security**: Bandit security scanner, Safety dependency check
- 🏗️ **Build**: Verifies package can be built
- 🐳 **Docker**: Tests Docker image build

### 2. **CD - Deploy** (`cd.yml`)

**Trigger**:
- Push to `main` branch
- Version tags (`v*.*.*`)
- Manual workflow dispatch

**Jobs**:
- 🐳 **Docker Publish**: Builds and pushes multi-arch images (amd64, arm64)
- 🧪 **Staging Deploy**: Deploys to staging environment with smoke tests
- 🌟 **Production Deploy**: Deploys to production (requires approval)
- 📦 **Release**: Creates GitHub release with changelog

### 3. **Performance Testing** (`performance.yml`)

**Trigger**: Daily at 2 AM UTC, Manual dispatch

**Jobs**:
- ⚡ **Benchmarks**: Runs performance benchmarks with pytest-benchmark
- 🔥 **Load Testing**: Uses Locust for load testing
- 🧠 **Memory Profiling**: Profiles memory usage

### 4. **Dependency Updates** (`dependency-update.yml`)

**Trigger**: Weekly on Monday, Manual dispatch

**Jobs**:
- 📦 **Update Dependencies**: Auto-updates and creates PR
- 🤖 **Dependabot Auto-merge**: Auto-merges patch updates

### 5. **Security Scanning** (`docker-scan.yml`, `codeql.yml`)

**Trigger**: Push, PR, Daily/Weekly schedules

**Jobs**:
- 🔒 **Trivy**: Scans Docker images for vulnerabilities
- 🔍 **Snyk**: Container security scanning
- 🐳 **Hadolint**: Dockerfile linting
- 🔒 **CodeQL**: Advanced security analysis

### 6. **Cleanup** (`cleanup.yml`)

**Trigger**: Weekly on Sunday, Manual dispatch

**Jobs**:
- 🗑️ **Artifacts**: Removes old workflow artifacts
- 🐳 **Docker Images**: Cleans old container images
- 🧹 **Caches**: Clears outdated build caches

### 7. **Auto Label** (`auto-label.yml`)

**Trigger**: PR/Issue opened

**Jobs**:
- 🏷️ **File-based Labels**: Labels based on changed files
- 📏 **Size Labels**: Labels PRs by size (XS/S/M/L/XL)

## 🔐 Required Secrets

Add these secrets in GitHub repository settings:

### GitHub Packages (Auto-configured)
- `GITHUB_TOKEN` ✅ (Automatic)

### Kubernetes Deployment
- `KUBE_CONFIG_STAGING` - Base64 encoded kubeconfig for staging
- `KUBE_CONFIG_PRODUCTION` - Base64 encoded kubeconfig for production

### Optional Services
- `SNYK_TOKEN` - Snyk security scanning token
- `CODECOV_TOKEN` - Codecov upload token (optional, works without)

## 🚀 Setup Instructions

### 1. Repository Setup

```bash
# Clone the repository
git clone https://github.com/Karn0511/jarvis_training.git
cd jarvis_training

# Copy CI/CD files to repository
cp -r project_Venom/.github .
cp project_Venom/.pylintrc .
cp project_Venom/CI_CD_GUIDE.md .

# Commit and push
git add .github/ .pylintrc CI_CD_GUIDE.md
git commit -m "🚀 Add CI/CD pipeline"
git push origin main
```

### 2. Enable GitHub Actions

1. Go to repository **Settings** → **Actions** → **General**
2. Enable **Allow all actions and reusable workflows**
3. Set **Workflow permissions** to **Read and write permissions**
4. Check **Allow GitHub Actions to create and approve pull requests**

### 3. Configure Secrets

```bash
# Generate base64 kubeconfig for staging
cat ~/.kube/config-staging | base64 -w 0

# Generate base64 kubeconfig for production
cat ~/.kube/config-production | base64 -w 0
```

Add in **Settings** → **Secrets and variables** → **Actions**:
- `KUBE_CONFIG_STAGING`: [paste base64 staging kubeconfig]
- `KUBE_CONFIG_PRODUCTION`: [paste base64 production kubeconfig]

### 4. Create Environments

1. Go to **Settings** → **Environments**
2. Create **staging** environment
3. Create **production** environment with protection rules:
   - ✅ Required reviewers (add yourself)
   - ✅ Wait timer: 5 minutes

### 5. Enable Dependabot

1. Go to **Settings** → **Code security and analysis**
2. Enable **Dependabot alerts**
3. Enable **Dependabot security updates**
4. The `.github/dependabot.yml` file will configure weekly updates

## 📝 Usage

### Running Tests Locally

```bash
# Activate virtual environment
.venv/Scripts/Activate.ps1

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Format code
black .

# Lint code
pylint **/*.py
```

### Manual Deployment

```bash
# Trigger staging deployment
gh workflow run cd.yml -f environment=staging

# Trigger production deployment (after testing)
gh workflow run cd.yml -f environment=production
```

### Creating a Release

```bash
# Tag a new version
git tag -a v2.1.0 -m "Release v2.1.0"
git push origin v2.1.0

# This automatically:
# 1. Builds Docker image with version tag
# 2. Deploys to staging
# 3. Awaits approval for production
# 4. Creates GitHub release with changelog
```

### Monitoring Workflows

```bash
# List workflow runs
gh run list

# Watch a workflow
gh run watch

# View logs
gh run view --log
```

## 🎯 Best Practices

### Branch Strategy
- `main` - Production-ready code
- `develop` - Development branch
- `feature/*` - Feature branches
- `hotfix/*` - Urgent fixes

### Commit Conventions
```
✨ feat: Add new feature
🐛 fix: Fix bug
📚 docs: Update documentation
🎨 style: Code formatting
♻️ refactor: Code refactoring
⚡ perf: Performance improvement
✅ test: Add tests
🔧 ci: CI/CD changes
```

### Pull Request Workflow
1. Create feature branch
2. Make changes and commit
3. Push and create PR
4. CI runs automatically
5. Review and merge
6. CD deploys to staging
7. Test on staging
8. Tag for production release

## 🔍 Monitoring & Alerts

### GitHub Actions Dashboard
- View all workflows: `https://github.com/Karn0511/jarvis_training/actions`
- Monitor failures and re-run if needed

### Deployment Status
- Staging: Check Kubernetes dashboard
- Production: Monitor health endpoint

### Security Alerts
- GitHub Security tab shows vulnerabilities
- Dependabot creates PRs for updates
- CodeQL alerts appear in Security tab

## 🐳 Docker Registry

Images are pushed to GitHub Container Registry:
```
ghcr.io/karn0511/jarvis_training:latest
ghcr.io/karn0511/jarvis_training:v2.1.0
ghcr.io/karn0511/jarvis_training:main-abc1234
```

### Pull Image
```bash
docker pull ghcr.io/karn0511/jarvis_training:latest
```

## 🆘 Troubleshooting

### Workflow Fails
1. Check workflow logs in Actions tab
2. Review error messages
3. Fix locally and push
4. Re-run workflow if needed

### Docker Build Fails
1. Test locally: `docker build -t venom:test .`
2. Check Dockerfile syntax
3. Ensure all dependencies are in requirements.txt

### Deployment Fails
1. Verify kubeconfig secrets are correct
2. Check Kubernetes cluster is accessible
3. Review k8s/deployment.yaml for errors

### Tests Fail
1. Run locally: `pytest tests/ -v`
2. Fix failing tests
3. Ensure all dependencies installed

## 📚 Additional Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Project Venom Docs](README.md)

## ✅ Checklist

- [x] CI/CD workflows created
- [x] GitHub Actions enabled
- [x] Secrets configured
- [x] Environments created
- [x] Dependabot enabled
- [x] Pull request template added
- [x] Issue templates added
- [x] Auto-labeling configured
- [x] Security scanning enabled

## 🎉 You're All Set!

Your CI/CD pipeline is now fully configured and ready to use! Every push will trigger automated tests, builds, and deployments.

**Happy Shipping! 🚀**
