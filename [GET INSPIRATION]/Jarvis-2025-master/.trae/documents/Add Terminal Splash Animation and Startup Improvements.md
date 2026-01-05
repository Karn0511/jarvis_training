## Overview
- Stack: Python backend with Eel-powered local web UI; no existing CLI/TUI libs.
- Terminal launch: `python run.py` spawns two processes — Jarvis UI (`main.start`) and hotword listener (`backend.feature.hotword`).
- Web served from `frontend/index.html`; Edge opens app window via `os.system('start msedge.exe --app=...')`.

## Goals
- Show a polished terminal splash with lightweight animation when launching from the terminal.
- Provide clear, progressive startup status (init → web server → browser → hotword).
- Keep changes minimal, pure-Python (no new deps), and fully optional via an env toggle.

## Key Injection Points
- `run.py:14–26` — prelude around process start to render splash and status.
- `main.py:10–35` — short spinner/banners around `eel.init(...)` and before Edge app launch.
- Path portability fix: `backend/feature.py:39` absolute path → repo-relative.

## Implementation Plan
1) Terminal Splash (pure Python, no deps)
- Add `splash()` in `run.py` that:
  - Prints an ASCII logo and title using standard `print`.
  - Renders a 1–2s spinner using `sys.stdout.write`, `flush`, `time.sleep`.
  - Detects TTY via `sys.stdout.isatty()` to disable animation if piped.
- Call `splash()` at program start (`run.py:15`) before spawning processes.

2) Startup Status Banners
- In `run.py`, add concise banners before/after each process start:
  - "Starting Jarvis UI…" → PID shown
  - "Starting Hotword Listener…" → PID shown
  - On exit, print final "Goodbye" banner.
- In `main.py`, add `print_status(msg)` helper and short spinner around:
  - Before `eel.init("frontend")` (lines ~10–14)
  - Before Edge launch (lines ~31–33)
  - Immediately before `eel.start(...)` to show "Serving at http://127.0.0.1:8000".

3) Optional Toggle and Robustness
- Respect env var `JARVIS_TUI=1` (default on for TTY), `JARVIS_TUI=0` to disable.
- Guard animations under `if os.getenv("JARVIS_TUI", "1") == "1" and sys.stdout.isatty()`.
- Ensure no blocking: spinners run for fixed short windows; no background threads.

4) Portability Improvements
- Fix hardcoded audio path at `backend/feature.py:39` to use:
  - `BASE = Path(__file__).resolve().parents[1]` and `BASE / "assets" / "assistant.wav"` (or existing asset location).
- Replace `os.system('start msedge.exe --app=...')` in `main.py:31` with `subprocess.Popen(["msedge.exe", f"--app=http://127.0.0.1:8000/index.html"])` and add `try/except` for clearer terminal errors.

5) Logging Consistency (minimal)
- Add a tiny `log(msg)` utility (pure print) to prefix timestamps in terminal for startup steps.
- Keep existing Eel UI logs intact; terminal logs are additive.

## File-Level Changes
- `run.py`
  - New `splash()` function near top.
  - Call `splash()` before `startJarvis`/`listenHotword` process creation (`run.py:15–18`).
  - Add status prints around process lifecycle (`run.py:14–26`).
- `main.py`
  - Add `print_status()` helper near imports (`main.py:8–12`).
  - Short spinner + status before `eel.init("frontend")` and Edge app launch (`main.py:10–33`).
  - Print serving URL just before `eel.start(...)` (`main.py:31–35`).
- `backend/feature.py`
  - Replace absolute sound path at line 39 with repo-relative construction via `pathlib.Path`.

## Validation
- Windows PowerShell: activate venv `./envJarvis/Scripts/Activate.ps1` and run `python ./run.py`.
- Observe: splash appears; status banners print; UI opens; hotword process starts.
- Disable check: set `JARVIS_TUI=0` to confirm silent startup.
- Verify no delays added (animation capped at ~2s) and no blocking of Eel.

## Risks & Mitigations
- ANSI color support varies; keep splash monochrome by default; add color later if approved.
- Edge not found: show clear terminal error and continue serving web UI.
- Piped/non-TTY execution: auto-disables animation to avoid noisy logs.

## Future Enhancements (Optional)
- If approved, adopt `rich` for richer banners/spinners while keeping changes isolated.
- Add a `--no-browser` CLI flag to skip Edge app launch for headless runs.

## Deliverables
- Updated `run.py`, `main.py`, and `backend/feature.py` with pure-Python splash + status and portability fixes.
- No new dependencies or files; minimal, reversible changes guarded by env toggle.