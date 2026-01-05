# 🤖 JARVIS AI - Advanced Coding Assistant

**JARVIS by KARN** - Your intelligent AI coding assistant with stunning terminal animations and web interface.

---

## 🚀 Quick Start

### **One-Command Setup**

**Linux/Mac/WSL:**
```bash
chmod +x jarvis.sh
./jarvis.sh setup
./jarvis.sh start
```

**After Setup - Use CLI:**
```bash
source .venv/bin/activate
jarvis status
jarvis ask "What is Python?"
jarvis chat
```

---

## 📋 Complete Installation Guide

### **Prerequisites**
- Python 3.8+ 
- Node.js 18+ & npm (for frontend)
- API Keys (optional but recommended):
  - OpenAI API Key
  - Anthropic API Key

### **Step 1: Clone or Download**
```bash
cd jarvis-advanced
```

### **Step 2: Setup Python Environment**
```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # Linux/Mac/WSL
# OR
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### **Step 3: Configure API Keys**
Create a `.env` file in the `jarvis-advanced` directory:
```env
# API Keys (get from respective providers)
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# Backend Settings
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8574

# Security
ENABLE_SHELL_EXECUTION=false
MAX_EXECUTION_TIME=30

# Features
USE_LOCAL_LLM=false
ENABLE_ANIMATIONS=true
```

### **Step 4: Start Backend Server**
Open a new terminal:
```bash
cd jarvis-advanced
source .venv/bin/activate
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8574
```

You should see:
```
🚀 Starting Jarvis AI v2.0.0
✅ All services initialized
INFO:     Uvicorn running on http://0.0.0.0:8574
```

### **Step 5: Start Frontend (Optional)**
Open another terminal:
```bash
cd jarvis-advanced/frontend
npm install  # First time only
npm run dev
```

Frontend will be available at: http://localhost:5173

### **Step 6: Use the CLI**
Open another terminal:
```bash
cd jarvis-advanced
source .venv/bin/activate
jarvis
```

---

## 🎨 Features

### ✨ **30+ Beautiful Terminal Animations**
- Animated ASCII banner with gradient colors
- Thinking animation with pulsing brain emojis
- Multi-stage progress bars with spinners
- Code analysis visualization (5 stages)
- AI response streaming (word-by-word)
- Success flash effects
- Error shake effects
- Matrix falling code effect
- Rainbow text effects
- Quantum circuit visualization
- Connection animations

### 💻 **Powerful CLI Commands**

#### Basic Commands
```bash
jarvis                    # Show banner and main menu
jarvis --help            # Show all available commands
jarvis --version         # Show version information
jarvis status            # Check backend connection (animated)
```

#### AI Interaction
```bash
jarvis ask "question"              # Ask AI a question
jarvis ask "question" --stream     # Ask with streaming response
jarvis chat                        # Interactive chat mode
jarvis chat --model gpt4          # Chat with specific model
```

#### Code Analysis
```bash
jarvis analyze file.py             # Analyze code file
jarvis analyze file.py --detailed  # Detailed analysis
```

#### Command Execution
```bash
jarvis execute "ls -la"            # Execute shell command
jarvis execute "python script.py"  # Run scripts
```

#### Project Initialization
```bash
jarvis init                        # Interactive project setup
jarvis init --template python      # Init with Python template
jarvis init --template react       # Init with React template
jarvis init --template node        # Init with Node.js template
```

### 🌐 **Web Interface**
- Beautiful Matrix-style UI
- Real-time backend status checking
- Direct link to API documentation
- Responsive design

### 🧠 **Multi-AI Routing**
- Automatically selects best AI model for the task
- Supports: GPT-4, GPT-3.5, Claude, Local LLMs
- Smart caching for instant repeated queries
- Fallback mechanisms

### 🔒 **Security Features**
- Safe command execution with confirmations
- Configurable execution timeout
- API key encryption
- Shell execution can be disabled

---

## 📚 Usage Examples

### Example 1: Ask a Question
```bash
$ jarvis ask "How do I reverse a list in Python?"

🧠 Thinking...

To reverse a list in Python, you have several options:

1. Using slicing:
   my_list = [1, 2, 3, 4, 5]
   reversed_list = my_list[::-1]

2. Using reverse() method:
   my_list.reverse()

3. Using reversed() function:
   reversed_list = list(reversed(my_list))
```

### Example 2: Analyze Code
```bash
$ jarvis analyze app.py

🔍 Scanning code structure...   ━━━━━━━━━━ 100%
🧬 Analyzing complexity...      ━━━━━━━━━━ 100%
🔬 Detecting patterns...        ━━━━━━━━━━ 100%
⚡ Running quantum analysis...  ━━━━━━━━━━ 100%
✨ Generating insights...       ━━━━━━━━━━ 100%

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📊 Analysis: app.py              ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Complexity     │ 4/10  │ 🟢 Low   │
│ Quality Score  │ 8/10  │ 🟢 Good  │
│ Issues Found   │ 2     │ ⚠️ 2     │
└────────────────┴───────┴──────────┘
```

### Example 3: Interactive Chat
```bash
$ jarvis chat

╔══════════════════════════════════════╗
║     💬 JARVIS CHAT MODE             ║
║     Type 'exit' to quit             ║
╚══════════════════════════════════════╝

You: Explain decorators in Python

🤖 JARVIS: Decorators are a powerful feature in Python...
[Detailed explanation follows]

You: Show me an example

🤖 JARVIS: Here's a simple decorator example...
[Code example provided]
```

### Example 4: Initialize Project
```bash
$ jarvis init --template python

✨ Initializing Python project...

📁 Creating structure:
   ├── src/
   ├── tests/
   ├── requirements.txt
   ├── README.md
   └── .gitignore

✅ Project created successfully!
```

---

## 🛠️ Configuration

### Backend Configuration (.env)
```env
# Required for AI features
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Server settings
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8574

# Feature flags
ENABLE_SHELL_EXECUTION=false  # Set to true to allow command execution
USE_LOCAL_LLM=false           # Use local LLM instead of API
ENABLE_ANIMATIONS=true        # CLI animations

# Security
MAX_EXECUTION_TIME=30         # Max seconds for command execution
ALLOWED_COMMANDS=ls,pwd,git   # Comma-separated allowed commands
```

### CLI Configuration
After first run, edit `~/.jarvis/config.yaml`:
```yaml
default_model: gpt-4
streaming: true
show_animations: true
color_scheme: matrix
auto_save_chat: true
```

---

## 🎯 Master Script Commands

### jarvis.sh (Linux/Mac/WSL)
```bash
./jarvis.sh setup      # Complete installation
./jarvis.sh start      # Start backend server
./jarvis.sh frontend   # Start frontend
./jarvis.sh demo       # Show animation showcase
./jarvis.sh status     # Check system status
./jarvis.sh test       # Run tests
./jarvis.sh clean      # Clean cache and temp files
./jarvis.sh help       # Show all commands
```

---

## 🔧 Troubleshooting

### Backend Won't Start
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check if port is in use
lsof -i :8574  # Linux/Mac
netstat -ano | findstr :8574  # Windows
```

### CLI Command Not Found
```bash
# Activate virtual environment
source .venv/bin/activate

# Reinstall CLI
pip install -e .

# Verify installation
which jarvis
```

### Frontend Won't Load
```bash
# Check Node version
node --version  # Should be 18+

# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install

# Start with different port
npm run dev -- --port 3000
```

### No AI Responses
1. Check API keys in `.env`
2. Verify backend is running: `curl http://localhost:8574/`
3. Check logs: Backend terminal shows errors
4. Try different model: `jarvis ask "test" --model gpt-3.5-turbo`

### Import Errors
```bash
# Make sure you're in the right directory
cd jarvis-advanced

# Activate virtual environment
source .venv/bin/activate

# Reinstall in editable mode
pip install -e .
```

---

## 📖 API Documentation

When backend is running, visit:
- **Swagger UI**: http://localhost:8574/docs
- **ReDoc**: http://localhost:8574/redoc

### Main Endpoints

#### GET /
Health check endpoint
```bash
curl http://localhost:8574/
```

#### POST /api/ask
Ask AI a question
```bash
curl -X POST http://localhost:8574/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Python?", "model": "gpt-4"}'
```

#### POST /api/analyze
Analyze code
```bash
curl -X POST http://localhost:8574/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "def hello(): print(\"Hi\")", "language": "python"}'
```

#### POST /api/execute
Execute command (if enabled)
```bash
curl -X POST http://localhost:8574/api/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "ls -la", "timeout": 10}'
```

---

## 🏗️ Project Structure

```
jarvis-advanced/
├── backend/               # FastAPI backend
│   ├── main.py           # Main server file
│   ├── api/              # API endpoints
│   ├── core/             # Core logic
│   ├── models/           # Data models
│   └── services/         # AI services
├── cli/                  # CLI application
│   ├── jarvis_cli.py    # Main CLI entry
│   ├── client.py        # API client
│   └── animations.py    # Animation functions
├── frontend/             # Web interface
│   ├── index.html       # Main HTML
│   ├── package.json     # NPM config
│   └── vite.config.js   # Vite config
├── config/              # Configuration files
├── docs/                # Documentation
├── shared/              # Shared utilities
├── .env                 # Environment variables
├── requirements.txt     # Python dependencies
├── setup.py            # Python package setup
└── jarvis.sh           # Master script
```

---

## 🎓 Advanced Usage

### Custom AI Models
Edit `backend/core/config.py`:
```python
AVAILABLE_MODELS = {
    "gpt-4": {"provider": "openai", "priority": 1},
    "gpt-3.5-turbo": {"provider": "openai", "priority": 2},
    "claude-3": {"provider": "anthropic", "priority": 3},
    "local": {"provider": "ollama", "priority": 4}
}
```

### Custom Templates
Add to `cli/templates/`:
```bash
jarvis-advanced/cli/templates/
├── python/
├── react/
├── node/
└── your-custom-template/
```

### Plugins
Create plugins in `backend/plugins/`:
```python
# backend/plugins/my_plugin.py
from backend.core.plugin import Plugin

class MyPlugin(Plugin):
    def execute(self, data):
        # Your logic here
        return result
```

---

## 🔄 Updating

```bash
cd jarvis-advanced
git pull  # If using git
source .venv/bin/activate
pip install -r requirements.txt --upgrade
cd frontend
npm update
```

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Credits

Created by **KARN** with ❤️

Special thanks to:
- OpenAI for GPT models
- Anthropic for Claude
- FastAPI for the amazing framework
- Vite for lightning-fast frontend
- Rich library for beautiful terminal output

---

## 📞 Support

- **Issues**: Create an issue on GitHub
- **Questions**: Use discussions tab
- **Email**: your-email@example.com

---

## 🎉 Enjoy Your JARVIS AI!

Your CLI is now:
- ✨ **Beautiful** - Stunning animations everywhere
- ⚡ **Fast** - Optimized with caching
- 🧠 **Smart** - Multi-AI routing
- 🎯 **Feature-rich** - Comprehensive commands
- 📚 **Well-documented** - Complete guides
- 🔒 **Secure** - Safety first approach
- 💪 **Production-ready** - Zero errors!

**Start using it NOW and experience the most beautiful AI assistant! 🚀✨**

---

*Made with ❤️ and lots of ☕*
