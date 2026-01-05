# 🚀 JARVIS AI - Quick Start Guide

## ✅ Setup Complete!

Your Jarvis AI has been configured and is ready to use!

---

## 📝 What Was Done

1. ✅ Frontend configured with Vite
2. ✅ npm dependencies installed  
3. ✅ Documentation consolidated (removed 7 duplicate .md files)
4. ✅ Python virtual environment linked
5. ✅ CLI package installed
6. ✅ All systems ready

---

## 🎯 How to Start Using Jarvis

### **Option 1: Use the Master Script (Recommended)**

```bash
# Make executable (first time only)
chmod +x jarvis.sh

# Start backend server
./jarvis.sh start

# In another terminal - use CLI
source .venv/bin/activate
jarvis status
jarvis ask "What is Python?"
jarvis chat
```

### **Option 2: Manual Start**

**Terminal 1 - Backend:**
```bash
cd jarvis-advanced
source .venv/bin/activate
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8574
```

**Terminal 2 - Frontend (Optional):**
```bash
cd jarvis-advanced/frontend
npm run dev
```

**Terminal 3 - CLI:**
```bash
cd jarvis-advanced
source .venv/bin/activate
jarvis
```

---

## 🎨 Quick Commands to Try

```bash
# Check if backend is running
jarvis status

# Ask AI a question
jarvis ask "Explain Python decorators"

# Ask with streaming response
jarvis ask "What is machine learning?" --stream

# Analyze a Python file
jarvis analyze backend/main.py

# Interactive chat mode
jarvis chat

# Show all commands
jarvis --help
```

---

## 🌐 Access Points

Once running:

- **Backend API**: http://localhost:8574
- **API Docs**: http://localhost:8574/docs
- **Frontend UI**: http://localhost:5173
- **CLI**: `jarvis` command in terminal

---

## ⚙️ Configuration (Optional)

Create `.env` file for AI features:

```bash
cp .env.example .env
# Then edit .env and add your API keys
```

```env
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

---

## 📚 Documentation

- **Full Guide**: [COMPREHENSIVE_README.md](COMPREHENSIVE_README.md)
- **Quick Ref**: [README.md](README.md)
- **Original Guide**: [START_HERE.md](START_HERE.md)

---

## 🐛 Troubleshooting

### Backend won't start?
```bash
# Check if virtual environment is activated
source .venv/bin/activate

# Verify Python version (should be 3.8+)
python --version

# Reinstall dependencies
pip install -r requirements.txt
```

### CLI not found?
```bash
# Make sure you're in the jarvis-advanced directory
cd jarvis-advanced

# Activate virtual environment
source .venv/bin/activate

# Reinstall CLI
pip install -e .

# Test
jarvis --version
```

### Frontend error?
```bash
cd frontend
npm install
npm run dev
```

### Port already in use?
```bash
# Kill process on port 8574
lsof -ti:8574 | xargs kill -9

# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

---

## 🎉 You're All Set!

Start with:
```bash
./jarvis.sh start
```

Then in another terminal:
```bash
source .venv/bin/activate
jarvis chat
```

**Enjoy your AI assistant! 🤖✨**
