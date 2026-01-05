## Goals
- Ensure the app launches reliably from the terminal with a polished splash/animation.
- Fix missing dependencies, hardcoded/invalid paths, and brittle audio/mic handling.
- Make the browser launch and Eel server startup robust and portable on Windows.

## Environment & Dependencies
- Create `requirements.txt` with: `eel`, `opencv-contrib-python`, `numpy`, `Pillow`, `speechrecognition`, `pyttsx3`, `pygame`, `pywhatkit`, `pyautogui`, `pvporcupine`, `pyaudio`, `hugchat`.
- Recommend Windows install flow:
  - PowerShell: `./envJarvis/Scripts/Activate.ps1`
  - Install: `pip install -r requirements.txt`
  - If `pyaudio` fails: `pip install pipwin && pipwin install pyaudio`.

## Path Normalization
- Replace all hardcoded backslash/relative strings with `pathlib.Path`:
  - `backend/auth/recoganize.py`, `backend/auth/sample.py`, `backend/auth/trainer.py`: cascade/model/samples → `BASE / "backend" / "auth" / ...` and wrap with `str(...)` for `cv2` calls.
  - `backend/feature.py` chatbot cookie: `cookie_path = str(BASE / "backend" / "cookie.json")`.
- Keep `jarvis.db` and assets repo-relative (already done for assistant sound).

## Eel Server & Browser Launch
- Use explicit port and consistent host:
  - `eel.start("index.html", mode="edge", host="127.0.0.1", port=8000, block=True)`.
- Browser fallback:
  - If Edge not found, call `webbrowser.open("http://127.0.0.1:8000/index.html", new=2)`.
- Ensure server readiness before opening browser (short poll or small delay).

## Audio/Mic Robustness
- `backend/feature.py`:
  - Lazy `pygame.mixer.init()` with error handling.
  - Porcupine loop: specify input device index, use `try/finally` to delete/close/terminate reliably.
- `backend/command.py`:
  - Initialize `pyttsx3` engine once at module load; guard voice selection.
  - Improve mic capture with exception handling and timeouts.

## Terminal UI Enhancements
- Keep splash and spinners guarded by `JARVIS_TUI` + `isatty`.
- Add concise status banners for processes and server URL.
- Optional: colorize banners later using `rich` (not required to function).

## Clean Shutdown
- On UI process exit, ensure hotword process is terminated cleanly.
- Consider signaling rather than `terminate()` for graceful cleanup.

## File-Level Changes
- `requirements.txt` — add listed packages.
- `run.py` — verify splash order and banners.
- `main.py` — set explicit port/host, use Edge mode or fallback to `webbrowser`.
- `backend/feature.py` — cookie path via `Path`; robust `pygame` init; porcupine cleanup.
- `backend/auth/*.py` — normalize all file paths via `Path`.
- `backend/command.py` — reuse `pyttsx3` engine; improve SR handling.

## Validation
- Activate venv and install requirements.
- Launch: `python ./run.py`.
- Observe: terminal splash → PIDs → Edge/app opens → Eel serves → hotword listener running.
- Smoke tests: play assistant sound, face auth prompt, send a command from UI, wake-word triggers.

## Risks & Mitigations
- `pyaudio` install issues: use `pipwin` wheel; document device index.
- Edge missing: rely on default browser via `webbrowser.open`.
- Mic permissions: add helpful terminal messages and fallbacks.

## Deliverables
- Updated Python files with path fixes, server/browser robustness, audio/mic reliability, and terminal UI.
- `requirements.txt` for consistent installs.
- Verified launch and core flows working on Windows.