# 🎯 Jarvis AI - Complete Usage Guide

## Table of Contents
1. [Installation](#installation)
2. [First Steps](#first-steps)
3. [CLI Commands](#cli-commands)
4. [Animation Features](#animation-features)
5. [Advanced Usage](#advanced-usage)
6. [Troubleshooting](#troubleshooting)

---

## Installation

### Quick Install (Recommended)

**Windows:**
```cmd
quickstart.bat
```

**Linux/Mac:**
```bash
chmod +x quickstart.sh
./quickstart.sh
```

### Manual Install

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate (Windows)
.venv\Scripts\activate

# 2. Activate (Linux/Mac)
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Jarvis
pip install -e .

# 5. Setup environment
cp .env.example .env
# Edit .env with your API keys
```

---

## First Steps

### 1. Start the Backend

```bash
cd backend
uvicorn main:app --reload
```

You should see:
```
🚀 Starting Jarvis AI v2.0.0
✅ All services initialized
INFO:     Uvicorn running on http://127.0.0.1:8574
```

### 2. Test the CLI

```bash
# Check status
jarvis status

# See available commands
jarvis --help

# Ask your first question
jarvis ask "What is Python?"
```

---

## CLI Commands

### `jarvis status`
**Check backend health with beautiful animations**

```bash
jarvis status
```

Shows:
- ✅ Connection status
- 📊 System statistics
- ⚡ Response time
- 🔧 Active features

---

### `jarvis ask`
**Ask AI questions with optional streaming**

```bash
# Basic question
jarvis ask "How do I reverse a list in Python?"

# With streaming (word-by-word)
jarvis ask "Explain decorators" --stream

# Complex question
jarvis ask "What's the difference between async and threading?"
```

**Features:**
- 🧠 Thinking animation
- 💬 Markdown-formatted responses
- ⚡ Caching for instant repeat queries
- 📝 Model information display

---

### `jarvis analyze`
**Analyze code files with AI**

```bash
# Basic analysis
jarvis analyze myfile.py

# Detailed analysis
jarvis analyze myfile.py --detailed
```

**What it shows:**
- 📊 Quality score (0-10)
- 🔢 Complexity rating
- ⚠️ Issues found
- 💡 Improvement suggestions
- 🎨 Code preview with syntax highlighting

**Supported languages:**
- Python (.py)
- JavaScript (.js)
- TypeScript (.ts)
- Java (.java)
- C/C++ (.c, .cpp)
- Go (.go)
- Rust (.rs)

---

### `jarvis chat`
**Interactive chat mode**

```bash
# Start chat
jarvis chat

# With specific model
jarvis chat --model gpt4
jarvis chat --model claude
jarvis chat --model local
```

**Chat Commands:**
- Type your message and press Enter
- `exit` or `quit` - Leave chat mode
- `clear` - Clear conversation history

**Features:**
- 💬 Multi-turn conversations
- 🧠 Context awareness
- ⚡ Streaming responses
- 📝 History tracking

---

### `jarvis execute`
**Execute shell commands safely**

```bash
# With confirmation (default)
jarvis execute "ls -la"

# Without confirmation
jarvis execute "git status" --no-confirm
```

**Safety Features:**
- ✅ Confirmation prompt
- 📊 Output formatting
- ⚠️ Error handling
- 🔒 Disabled by default (enable in .env)

**Note:** Enable with `ENABLE_SHELL_EXECUTION=true` in `.env`

---

### `jarvis init`
**Initialize Jarvis in your project**

```bash
# Default (Python)
jarvis init

# With template
jarvis init --template python
jarvis init --template javascript
jarvis init --template react
jarvis init --template api
```

**Creates:**
- 📁 `.jarvis/` directory
- ⚙️ `config.yaml` configuration
- 🎨 Project-specific settings

---

## Animation Features

### 1. Banner Animation
Beautiful ASCII art with gradient colors on startup

### 2. Thinking Animation
Brain emoji with pulsing dots while AI processes

### 3. Progress Bars
Multi-stage progress with:
- 🔄 Spinners
- 📊 Progress bars
- ⏱️ Time elapsed
- 📈 Percentage complete

### 4. Code Analysis Stages
```
🔍 Scanning code structure...   ━━━━━━━━━━ 100%
🧬 Analyzing complexity...      ━━━━━━━━━━ 100%
🔬 Detecting patterns...        ━━━━━━━━━━ 100%
⚡ Running quantum analysis...  ━━━━━━━━━━ 100%
✨ Generating insights...       ━━━━━━━━━━ 100%
```

### 5. Success/Error Effects
- ✨ Flash animation for success
- ⚠️ Shake effect for errors

### 6. AI Response Streaming
Real-time word-by-word display in beautiful panels

---

## Advanced Usage

### Using Different AI Models

The backend automatically selects the best model, but you can force specific ones:

**In `.env`:**
```env
# Use local model only
USE_LOCAL_LLM=true

# Prefer OpenAI
OPENAI_API_KEY=your_key

# Prefer Anthropic
ANTHROPIC_API_KEY=your_key
```

### Caching

Responses are cached automatically for speed:

```bash
# First query - hits AI API
jarvis ask "What is Python?"  # 2-3 seconds

# Second query - from cache
jarvis ask "What is Python?"  # <100ms ⚡
```

**Configure in `.env`:**
```env
REDIS_URL=redis://localhost:6379
CACHE_TTL=300  # 5 minutes
```

### API Integration

Use Jarvis backend in your own apps:

```python
import requests

# Ask question
response = requests.post('http://localhost:8574/api/chat', json={
    'message': 'Your question',
    'stream': False
})
print(response.json()['answer'])

# Analyze code
response = requests.post('http://localhost:8574/api/analyze', json={
    'code': 'def hello(): print("Hi")',
    'language': 'python',
    'filename': 'test.py'
})
print(response.json())
```

### WebSocket Real-time

```javascript
const ws = new WebSocket('ws://localhost:8574/ws');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'chat',
    message: 'Hello!'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data.message);
};
```

---

## Troubleshooting

### Backend won't start

**Problem:** `ModuleNotFoundError`

**Solution:**
```bash
pip install -r requirements.txt
```

---

### "Backend is offline"

**Problem:** CLI can't connect

**Solutions:**
1. Check if backend is running:
   ```bash
   cd backend
   uvicorn main:app
   ```

2. Verify URL in `.env`:
   ```env
   JARVIS_BACKEND_URL=http://127.0.0.1:8574
   ```

3. Check firewall/antivirus

---

### No AI responses (local model errors)

**Problem:** API keys not set

**Solution:**
Add to `.env`:
```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

Or use local model:
```env
USE_LOCAL_LLM=true
```

---

### Slow responses

**Solutions:**
1. Enable caching:
   ```env
   REDIS_URL=redis://localhost:6379
   ```

2. Use faster model:
   ```env
   USE_LOCAL_LLM=false
   OPENAI_API_KEY=your_key
   ```

3. Check network connection

---

### Animations not showing

**Problem:** Terminal doesn't support rich formatting

**Solutions:**
1. Use modern terminal:
   - Windows Terminal
   - iTerm2 (Mac)
   - Alacritty

2. Update terminal settings for UTF-8

3. Disable animations in config:
   ```yaml
   # .jarvis/config.yaml
   preferences:
     animations: false
   ```

---

## Tips & Tricks

1. **Use `--help` everywhere**
   ```bash
   jarvis --help
   jarvis ask --help
   jarvis analyze --help
   ```

2. **Stream long responses**
   ```bash
   jarvis ask "Long explanation" --stream
   ```

3. **Analyze before committing**
   ```bash
   jarvis analyze $(git diff --name-only)
   ```

4. **Chat for complex questions**
   ```bash
   jarvis chat  # Better for back-and-forth
   ```

5. **Check status regularly**
   ```bash
   jarvis status  # Beautiful system overview
   ```

---

## Keyboard Shortcuts

**In Chat Mode:**
- `Ctrl+C` - Exit chat
- `Ctrl+D` - Exit chat (Unix)
- Type `exit` - Exit chat
- Type `clear` - Clear history

---

## Environment Variables Reference

```env
# Backend
JARVIS_BACKEND_URL=http://127.0.0.1:8574
HOST=0.0.0.0
PORT=8574
DEBUG=true
WORKERS=4

# AI Keys
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=

# Features
ENABLE_SHELL_EXECUTION=false
ENABLE_QUANTUM=false
USE_LOCAL_LLM=true

# Caching
REDIS_URL=redis://localhost:6379
CACHE_TTL=300

# Limits
MAX_FILE_SIZE=10000000
MAX_CONTEXT_LENGTH=8000

# CORS
ALLOWED_ORIGINS=["http://localhost:3000"]
```

---

**Need more help? Check the README or open an issue!**
