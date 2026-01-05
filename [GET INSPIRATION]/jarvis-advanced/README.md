# 🤖 JARVIS AI - Advanced Coding Assistant

**Your intelligent AI coding assistant with stunning terminal animations and web interface.**

---

## 🚀 Quick Start

```bash
# Setup (one time)
chmod +x jarvis.sh
./jarvis.sh setup

# Start backend
./jarvis.sh start

# In another terminal, use CLI
source .venv/bin/activate
jarvis status
jarvis ask "What is Python?"
jarvis chat
```

---

## 📚 Full Documentation

**See [COMPREHENSIVE_README.md](COMPREHENSIVE_README.md) for:**
- Complete installation guide
- All CLI commands and examples
- API documentation
- Troubleshooting
- Advanced usage
- Configuration options

---

## 🎯 Key Features

✨ 30+ Beautiful Terminal Animations  
🚀 Ultra-Fast FastAPI Backend  
🧠 Multi-AI Routing (GPT-4, Claude, Local)  
💬 Interactive Chat Mode  
🔍 Advanced Code Analysis  
🌐 Web Interface with Matrix UI  
📊 Beautiful Terminal Output  

---

## 📖 Quick Reference

### Start Services
```bash
# Backend (Terminal 1)
./jarvis.sh start

# Frontend (Terminal 2 - Optional)
cd frontend && npm run dev

# CLI (Terminal 3)
source .venv/bin/activate
jarvis
```

### Common Commands
```bash
jarvis status                    # Check backend
jarvis ask "question"            # Ask AI
jarvis chat                      # Interactive chat
jarvis analyze file.py           # Analyze code
jarvis init --template python    # Init project
```

---

## 🔧 Configuration

Create `.env` file:
```env
OPENAI_API_KEY=sk-your-key
ANTHROPIC_API_KEY=sk-ant-your-key
BACKEND_PORT=8574
```

---

## 📞 Need Help?

- **Full Guide**: [COMPREHENSIVE_README.md](COMPREHENSIVE_README.md)
- **Quick Start**: [START_HERE.md](START_HERE.md)
- **API Docs**: http://localhost:8574/docs (when running)

---

Created by **KARN** with ❤️
