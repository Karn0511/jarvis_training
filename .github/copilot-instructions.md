# Project Venom - Copilot Instructions

## Architecture Overview

**Project Venom** is an advanced AI assistant with a "consciousness architecture" built on Python. The system uses:

- **Event-driven architecture**: Central [core/synapse.py](../project_Venom/core/synapse.py) nervous system broadcasts state changes (`LISTENING`, `PROCESSING`, `THINKING`, `SPEAKING`) for real-time monitoring
- **Multi-brain routing**: [brain/router.py](../project_Venom/brain/router.py) routes requests to specialized modules (Media, Comms, Vision, Math Engine, or Neural Core)
- **Three-layer UI**: Terminal console (main.py), Streamlit HUD dashboard (venom_hud.py), and web frontend
- **Immortality daemon**: [venom_daemon.py](../project_Venom/venom_daemon.py) auto-restarts on crashes with exponential backoff

### Key Data Flows

1. **Input**: User → Terminal/Web → [core/synapse.py](../project_Venom/core/synapse.py) `push_input()` → `main.py` polls via `synapse.get_input()`
2. **Processing**: Router decides module → AI generates response (streaming or static) → Broadcasts state changes
3. **Output**: Response → [storage/venom_response.json](../project_Venom/storage) → Voice TTS + Display
4. **Monitoring**: All states broadcast to [storage/venom_state.json](../project_Venom/storage) → HUD reads at 0.5s intervals

### Directory Structure

```
project_Venom/
├── brain/          # AI routing & cognitive engines (Gemini, Phi-3, Quantum)
├── core/           # System infrastructure (synapse, kernel, event_bus, neural_viz)
├── modules/        # Capability plugins (vision, voice, actions, media, comms, cloner)
├── storage/        # Runtime state files (venom_state.json, venom_input.json, crash_report.log)
└── k8s/            # Kubernetes deployment manifests
```

## Development Workflows

### Running the System

**Primary method**: Use PowerShell control script

```powershell
cd project_Venom
.\venom_control.ps1 full     # Daemon + HUD (production mode)
.\venom_control.ps1 test     # Run Phase 2 module tests
```

**VS Code tasks** (invoke via `Ctrl+Shift+P` → "Run Task"):

- `🚀 Venom: Launch ALL` - Starts daemon, HUD, and web server (recommended)
- `🧪 Venom: Run Phase2 Tests` - Runs test_phase2.py
- `🐍 Venom: Run Main` - Direct main.py execution (single process, for debugging)

**Manual approach** (for multi-terminal setup):

```powershell
# Terminal 1: Immortal daemon (auto-restarts on crash)
python venom_daemon.py

# Terminal 2: HUD dashboard (Streamlit at localhost:8501)
streamlit run venom_hud.py

# Terminal 3: Web API (FastAPI at localhost:8000)
python web_server.py
```

**Startup order matters**: Daemon must start first so input/state files exist before main.py polls them.

### Testing

- **Phase 2 tests**: `python test_phase2.py` (validates synapse, neural_viz, daemon)
- **Startup validation**: `python startup_test.py`
- **Full suite**: Use task `🧪 Venom: Run Tests` (runs pytest in tests/)
- **Coverage report**: Task `🔬 Venom: Test with Coverage` generates HTML report

**Critical**: Always run tests from `project_Venom/` directory with `.venv` activated.

### Python Environment

**Critical**: Always activate `.venv` before running commands:

```powershell
.\.venv\Scripts\Activate.ps1
```

The workspace has a shared `.venv` at repository root (`e:\Advanced Jarvis\.venv`), but project_Venom has its own. VS Code auto-activates when opening terminals.

## Project-Specific Conventions

### State Broadcasting Pattern

All async operations MUST broadcast state changes via synapse:

```python
from core.synapse import synapse

synapse.broadcast("PROCESSING", "Analyzing visual input...", synapse.get_vitals())
# ... do work ...
synapse.broadcast("THINKING", "Generating response...", synapse.get_vitals())
```

States: `BOOTING`, `ONLINE`, `LISTENING`, `PROCESSING`, `THINKING`, `RESPONSE`, `SPEAKING`, `ERROR`

**Key principle**: Synapse is the single source of truth for system state. HUD polls `storage/venom_state.json` at 0.5s intervals.

### Neural Visualization

When activating cognitive modules, trigger neural_viz to highlight nodes:

```python
from core.neural_viz import visualizer
visualizer.generate_frame("LLM_CORE", intensity=0.9, cpu_load=synapse.get_vitals()['cpu_percent'])
```

Nodes: `EARS`, `VISION`, `QUANTUM_GATE`, `LLM_CORE`, `MEMORY`, `VOICE`

### Logging

Use the custom logger from [core/logger.py](../project_Venom/core/logger.py) instead of print():

```python
from core.logger import logger
logger.system("System message")   # Blue [VENOM]
logger.success("Success")         # Green checkmark
logger.error("Error", error=e)    # Red with traceback
```

### Async by Default

Main loop and all brain functions use `async`/`await`. Blocking I/O must use `asyncio.to_thread()`:

```python
result = await asyncio.to_thread(blocking_function, arg1, arg2)
```

**Event Bus** ([core/event_bus.py](../project_Venom/core/event_bus.py)): Use for loosely-coupled component communication:

```python
from core.event_bus import bus
await bus.emit("system.shutdown", {"reason": "user_request"})
bus.subscribe("module.loaded", async def on_module_loaded(data): ...)
```

### Configuration Management

Settings use Pydantic in [core/config.py](../project_Venom/core/config.py). Access via singleton:

```python
from core.config import config
api_key = config.GEMINI_API_KEY
turbo_mode = config.VENOM_BOOST
```

Environment variables load from `.env` at project root (not committed). Required: `GEMINI_API_KEY`, optional: `OPENAI_API_KEY`.

## Integration Points

### Cognitive Router Decision Tree

[brain/router.py](../project_Venom/brain/router.py) routes by keyword detection (order matters):

1. **Hardware controls** (`clone voice`) → [modules/cloner.py](../project_Venom/modules/cloner.py) (lazy-loaded, heavy VRAM)
2. **Vision** (`see`, `camera`, `scan room`) → [modules/vision.py](../project_Venom/modules/vision.py) (YOLOv8)
3. **Media** (`play youtube`, `play song`) → [modules/media.py](../project_Venom/modules/media.py) (pywhatkit)
4. **Comms** (`whatsapp`, `send message`) → [modules/comms.py](../project_Venom/modules/comms.py)
5. **Math** (`calculate`, `solve`, arithmetic patterns) → [brain/analytical_engine.py](../project_Venom/brain/analytical_engine.py)
6. **Fallback** → [brain/system_brain.py](../project_Venom/brain/system_brain.py) (Gemini API, with streaming support)

**Pattern**: Router returns `(result, source, is_stream)` tuple. Streaming responses handled by `ai_response_stream()` animation.

### External Dependencies

- **Google Gemini API**: Primary LLM (requires API key). Supports streaming via `generate_stream()`.
- **YOLOv8**: Object detection ([yolov8n.pt](../project_Venom/yolov8n.pt) in project root)
- **Streamlit**: HUD dashboard (localhost:8501)
- **FastAPI**: Web server (web_server.py, typically port 8000)
- **Kubernetes**: Deployment manifests in [k8s/deployment.yaml](../project_Venom/k8s/deployment.yaml)

### Storage Files (Atomic Writes)

All JSON files in [storage/](../project_Venom/storage) use atomic write pattern (write to `.tmp`, then move):

- `venom_state.json` - Current system state (read by HUD)
- `venom_input.json` - Web commands (write by web_server.py, read by main.py)
- `venom_response.json` - AI responses (write by main.py, read by frontend)
- `venom_live_log.json` - Rolling log (last 50 entries)
- `crash_report.log` - Daemon crash history

## Performance Optimizations

The system has "TURBO mode" (config.VENOM_BOOST) that enables:

- Smart caching (2000 items, 10min TTL)
- Connection pooling (max 20 connections)
- Parallel processing (32 thread workers, 8 process workers)

See [PERFORMANCE_GUIDE.md](../project_Venom/PERFORMANCE_GUIDE.md) for details.

## Docker & Deployment

```bash
docker-compose up -d          # Start all services
kubectl apply -f k8s/         # Deploy to Kubernetes
.\DEPLOY_K8S.ps1              # Automated K8s deployment (Windows)
```

Container uses [docker-entrypoint.sh](../project_Venom/docker-entrypoint.sh) which starts daemon mode automatically.

## Critical Patterns & Gotchas

### Lazy Loading Strategy

Heavy modules (cloner with voice cloning) are initialized as `None` in router `__init__`, then created on first use. This prevents memory bloat on startup. Always check `if self.cloner is None:` before using, then import and instantiate.

### Atomic File I/O

All JSON writes in `storage/` use atomic pattern: write to `.tmp` file first, then `shutil.move()` to atomically replace the target. Never write directly. See `synapse._atomic_write()` for pattern.

### Config Loading Priority

`config.py` uses Pydantic with `BaseSettings`. Required env vars: `GEMINI_API_KEY`. On import failure, the system logs `CRITICAL` and continues (graceful degradation). Check `config.DEBUG_MODE` for development vs production behavior.

### Main Loop Polling

[main.py](../project_Venom/main.py) polls `synapse.get_input()` in a tight loop during `LISTENING` state. This is blocking (not async-await) by design for terminal input. Web commands are non-blocking and processed immediately when detected.

### Module Initialization Order

1. Synapse must be created first (singleton pattern)
2. Daemon starts before main.py (creates storage files)
3. Router instantiated after synapse exists
4. Neural visualizer initialized after router (depends on synapse vitals)

## Additional References

- [ARCHITECTURE.md](../project_Venom/ARCHITECTURE.md) - Detailed system diagrams
- [PHASE2_CONSCIOUSNESS.md](../project_Venom/PHASE2_CONSCIOUSNESS.md) - Phase 2 features (synapse, neural_viz, HUD, daemon)
- [QUICKSTART.md](../project_Venom/QUICKSTART.md) - All operation modes
- [README_WORKSPACE.md](../README_WORKSPACE.md) - Multi-project workspace overview
