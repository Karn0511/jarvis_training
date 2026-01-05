## Goals
- Run Jarvis purely via typed terminal commands; disable voice input.
- Upgrade terminal visuals using animations and color (with safe fallbacks).
- Integrate a configurable chat provider: OpenAI or free/local options for unlimited use.

## Chat Provider Integration
- Add a provider switch (env var): `JARVIS_CHAT_PROVIDER=openai|ollama|hugchat|none`.
- `openai` (paid, reliable):
  - Read `OPENAI_API_KEY` from environment. Do NOT hardcode it.
  - Use cost-efficient model (e.g., `gpt-4o-mini`) for chat completions.
- `ollama` (free, local, unlimited):
  - If `OLLAMA_HOST` (default `http://localhost:11434`) is reachable, call `POST /api/generate` with a local model (e.g., `llama3.2` or `phi3`).
  - Provide a one-time instruction to install Ollama and pull a model.
- `hugchat` (existing): keep as fallback but no guarantee of “unlimited” use.
- Implementation:
  - Replace current `chatBot()` in `backend/feature.py:190–198` with a small adapter:
    - `get_chat_response(query)` selects provider by env var.
    - `openai`: use official Python SDK, `client.chat.completions.create`.
    - `ollama`: send HTTP request to local server.
    - `hugchat`: use current cookie-based flow.

## Text-Only Terminal Mode
- `main.py` runner:
  - Remove calls to microphone capture; always read from `input()`.
  - Keep TTS (`speak`) for responses.
  - Update prompt hints (only typed input).

## Terminal Animations & Styling
- Default (no new deps): maintain splash, spinner, typewriter.
- Rich upgrade (optional): add `rich` to requirements and guard usage via `try/except` and `JARVIS_TUI_STYLE=rich|basic`.
  - Use `rich` Panels for banners, `Spinner` for processing, colored prompts, and subtle progress bars.
- Keep `JARVIS_TUI=1` toggle; auto-disable animations when not a TTY.

## Security & Config
- Never commit or print secrets. Read `OPENAI_API_KEY` from env only.
- Env vars:
  - `OPENAI_API_KEY` (for OpenAI)
  - `JARVIS_CHAT_PROVIDER` (select provider)
  - `JARVIS_TUI_STYLE` (rich/basic)
  - `JARVIS_TUI` (enable/disable animations)

## Validation
- Install optional `rich`: `pip install rich`.
- Set provider:
  - Unlimited local: install Ollama, `ollama pull llama3.2`, set `JARVIS_CHAT_PROVIDER=ollama`.
  - OpenAI: set `OPENAI_API_KEY`, `JARVIS_CHAT_PROVIDER=openai`.
- Run: `python .\run.py`.
- Type commands; observe animated terminal output and chat responses.

## Deliverables
- Updated `backend/feature.py` with provider adapter.
- Updated `main.py` to text-only input, enhanced terminal UI, guarded rich usage.
- Requirements optionally updated to include `rich`.

## Free/Unlimited Options Summary
- Local LLM via Ollama (recommended): free, offline, unlimited.
- Future optional: offline STT (Vosk) if voice is reintroduced later.
- Current operations (open apps, YouTube, WhatsApp) are local and don’t consume API quotas.