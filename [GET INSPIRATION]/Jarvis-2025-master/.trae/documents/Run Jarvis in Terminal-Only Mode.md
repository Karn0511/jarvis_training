## Prerequisites
- Python installed and accessible in your shell.
- Install dependencies: `pip install -r requirements.txt`.
- Optional visuals: `pip install rich` (already in requirements).

## Configure Provider (Optional)
- Choose a chat provider via env var `JARVIS_CHAT_PROVIDER=openai|ollama|hugchat`.
- OpenAI: set `OPENAI_API_KEY` in your environment.
- Ollama (free/local): install Ollama, pull a model (`llama3.2`), and set `JARVIS_CHAT_PROVIDER=ollama`.

## UI Settings (Optional)
- Enable terminal animations: `JARVIS_TUI=1` (default).
- Choose style: `JARVIS_TUI_STYLE=rich` for colored panels and spinners; otherwise uses basic.
- Hotword is off by default. To enable later: `JARVIS_HOTWORD=1` and set `PORCUPINE_ACCESS_KEY`.

## Run
- In your project directory: `python .\run.py`.
- Expected logs: ASCII splash → “Initializing Jarvis terminal mode…” → prompt `>`.

## Use
- Type commands at the prompt (no voice input):
  - Examples: `open notepad`, `play song on youtube`, `send message to Alice`, general questions for the chatbot.
  - Exit: `exit`, `quit`, or `stop`.

## Verification & Troubleshooting
- If chat errors: confirm provider env vars (`OPENAI_API_KEY`) or that Ollama is running and model is pulled.
- If animations don’t show: ensure you’re in a real TTY and `JARVIS_TUI=1`.
- WhatsApp automation requires desktop app installed and focus; YouTube opens via default browser.

## Next Enhancements (Optional)
- Colorized banners everywhere via `rich` components.
- Add more local/free providers if desired (e.g., LM Studio with local HTTP API).