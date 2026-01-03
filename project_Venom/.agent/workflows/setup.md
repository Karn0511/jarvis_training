---
description: Initial setup and dependency installation for Project Venom.
---

# 🛠️ Venom Setup Workflow

Follow these steps to initialize the symbiote.

1. **Environment Setup**
// turbo
Run the following to create and activate the virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

1. **Dependency Installation**
// turbo
Install all core AI and system tools:

```powershell
pip install -r requirements.txt
```

1. **GPU Check**
Verify CUDA availability for the eyes and memory:

```powershell
python check_specs.py
```

1. **Neural Link Calibration**
Start Ollama to provide the brain:

```powershell
ollama serve
```

*(In a separate terminal)*

1. **Awaken Venom**

```powershell
.\run_venom.ps1
```
