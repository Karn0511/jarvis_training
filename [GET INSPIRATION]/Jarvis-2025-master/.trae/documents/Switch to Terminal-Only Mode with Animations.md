## Goals
- Remove browser/Eel UI and face authentication flow; run Jarvis entirely in the terminal.
- Keep voice input/output working with clear terminal animations and status.
- Make hotword listener optional and non-blocking.

## Key Changes
- `main.py`: Add a terminal-only runner that:
  - Prints animated banners/spinners, plays assistant sound.
  - Welcomes the user and enters a voice-command loop.
  - Dispatches commands (open apps/URLs, YouTube, chatbot, WhatsApp) without any Eel calls.
  - Skips face authentication entirely.
- `backend/command.py`: Guard all `eel.*` calls so terminal mode doesn’t crash; keep pyttsx3 engine reuse.
- `run.py`: Call the terminal runner and stop launching the browser; make hotword process optional via `JARVIS_HOTWORD=1` and `PORCUPINE_ACCESS_KEY`.

## Terminal Animations
- Use the existing splash and spinners for status.
- Add typewriter-style message printing on welcome and key events.

## Validation
- Run `python .\run.py` and confirm it stays in the terminal.
- Speak a command; observe printed status and spoken response.
- Confirm hotword disabled unless keys are set.

## Deliverables
- Updated `main.py`, `run.py`, and `backend/command.py` for terminal-only operation.
- No new files or dependencies; browser/UI entirely removed from the startup path.