!/bin/bash
# ============================================================
# JARVIS AI - Master Control System
# Unified startup, management, and deployment
# ============================================================

# Get absolute path to the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Source animations if available
if [ -f "$SCRIPT_DIR/animations.sh" ]; then
    source "$SCRIPT_DIR/animations.sh"
else
    # Fallback simple functions if animations.sh is missing
    echo "⚠️  animations.sh not found in $SCRIPT_DIR, using simple output"
    emoji_status() { echo "$1: $2"; }
    modern_spinner() { echo "$2..."; "$1" & wait; }
    rainbow_progress() { echo "Progress: $1/$2 - $3"; }
    glow_text() { echo "$1"; }
    cyber_box() { echo "$1"; echo "$2"; }
fi

# Configuration
BACKEND_PORT=8574
FRONTEND_PORT=5173

# Venv is located one directory up from the script (in the root jarvis_gpt folder)
VENV_DIR="$SCRIPT_DIR/../.venv"
VENV_PYTHON="$VENV_DIR/bin/python"
VENV_PIP="$VENV_DIR/bin/pip"

# ==================== CORE FUNCTIONS ====================

check_python() {
    if command -v python3.12 &> /dev/null; then
        PYTHON_CMD="python3.12"
    elif command -v python3.11 &> /dev/null; then
        PYTHON_CMD="python3.11"
    elif command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    else
        emoji_status "error" "Python 3.11+ not found!"
        exit 1
    fi
}

setup_environment() {
    glow_text "INITIALIZING JARVIS SYSTEM"
    echo ""
    
    check_python
    
    local steps=5
    local current=0
    
    # 1. Virtual Environment
    current=$((current + 1))
    if [ ! -d "$VENV_DIR" ]; then
        emoji_status "loading" "Creating neural pathways (venv)..."
        $PYTHON_CMD -m venv "$VENV_DIR"
        emoji_status "success" "Neural pathways established"
    else
        emoji_status "success" "Neural pathways active"
    fi
    rainbow_progress $current $steps "Environment Check"
    echo ""
    
    # 2. Activate & Configure Paths
    if [ -f "$VENV_DIR/bin/activate" ]; then
        source "$VENV_DIR/bin/activate"
    fi
    
    # 3. Dependencies
    current=$((current + 1))
    emoji_status "loading" "Loading knowledge base..."
    
    # Use explicit venv pip with verbose output to avoid hanging/silence
    echo -e "${DIM}"
    "$VENV_PYTHON" -m pip install --upgrade pip
    "$VENV_PYTHON" -m pip install -r requirements.txt
    echo -e "${NC}"
    
    emoji_status "success" "Knowledge base loaded"
    rainbow_progress $current $steps "Dependencies"
    echo ""
    
    # 4. Frontend Setup
    current=$((current + 1))
    emoji_status "loading" "Configuring visual interface..."
    if [ -d "frontend" ]; then
        cd frontend
        if [ ! -d "node_modules" ]; then
            echo -e "${DIM}"
            npm install
            echo -e "${NC}"
        fi
        cd ..
        emoji_status "success" "Visual interface ready"
    else
        emoji_status "warning" "Frontend directory missing"
    fi
    rainbow_progress $current $steps "Frontend"
    echo ""
    
    # 5. Configuration
    current=$((current + 1))
    if [ ! -f ".env" ]; then
        cp .env.example .env 2>/dev/null || touch .env
        emoji_status "sparkle" "Configuration generated"
    fi
    rainbow_progress $current $steps "Configuration"
    echo ""
    
    # 6. CLI Installation
    current=$((current + 1))
    echo -e "${DIM}"
    "$VENV_PYTHON" -m pip install -e .
    echo -e "${NC}"
    rainbow_progress $current $steps "System Integration"
    echo ""
    
    cyber_box "SYSTEM READY" "Setup complete. Run './jarvis.sh start' to launch."
}

start_system() {
    glow_text "INITIATING LAUNCH SEQUENCE"
    echo ""
    
    # Check environment
    if [ ! -d "$VENV_DIR" ]; then
        emoji_status "error" "System not initialized. Run './jarvis.sh setup' first."
        exit 1
    fi
    
    source "$VENV_DIR/bin/activate"
    
    # Kill existing processes
    emoji_status "loading" "Clearing ports..."
    pkill -f "uvicorn main:app" 2>/dev/null
    pkill -f "vite" 2>/dev/null
    sleep 1
    
    # Start Backend
    emoji_status "rocket" "Launching Backend Core..."
    cd backend
    # Use explicit venv python to ensure uvicorn is found
    nohup "$VENV_PYTHON" -m uvicorn main:app --reload --host 0.0.0.0 --port $BACKEND_PORT > ../backend.log 2>&1 &
    BACKEND_PID=$!
    cd ..
    
    # Wait for backend health
    echo -n "   Waiting for core alignment..."
    local max_retries=30
    local retry_count=0
    local backend_ready=false
    
    while [ $retry_count -lt $max_retries ]; do
        if curl -s "http://localhost:$BACKEND_PORT/health" &>/dev/null; then
            echo -e "\r   ${NEON_GREEN}✓ Core aligned${NC}                     "
            backend_ready=true
            break
        fi
        
        # Check if process died
        if ! kill -0 $BACKEND_PID 2>/dev/null; then
            echo -e "\n${BRED}❌ Backend process died!${NC}"
            echo -e "${BYELLOW}Last 10 lines of backend.log:${NC}"
            tail -n 10 backend.log
            exit 1
        fi
        
        echo -n "."
        sleep 1
        retry_count=$((retry_count + 1))
    done
    
    if [ "$backend_ready" = false ]; then
        echo -e "\n${BRED}❌ Backend failed to start in time.${NC}"
        echo -e "${BYELLOW}Last 10 lines of backend.log:${NC}"
        tail -n 10 backend.log
        kill $BACKEND_PID 2>/dev/null
        exit 1
    fi
    
    # Start Frontend
    emoji_status "sparkle" "Initializing Interface..."
    cd frontend
    nohup npm run dev -- --port $FRONTEND_PORT > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd ..
    
    echo ""
    cyber_box "SYSTEM ONLINE" "Backend: http://localhost:$BACKEND_PORT\nFrontend: http://localhost:$FRONTEND_PORT"
    echo ""
    
    emoji_status "info" "Logs available in backend.log and frontend.log"
    echo -e "${NEON_YELLOW}Press Ctrl+C to shutdown${NC}"
    
    # Trap cleanup
    trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; emoji_status 'error' 'System Shutdown'; exit" INT
    
    wait
}

# ==================== CLI COMMANDS ====================

case "${1:-help}" in
    setup)
        setup_environment
        ;;
    start)
        start_system
        ;;
    stop)
        pkill -f "uvicorn main:app"
        pkill -f "vite"
        emoji_status "success" "System stopped"
        ;;
    status)
        if curl -s "http://localhost:$BACKEND_PORT/health" &>/dev/null; then
            emoji_status "success" "System Operational"
        else
            emoji_status "error" "System Offline"
        fi
        ;;
    hack)
        glow_text "ACCESSING MAINFRAME"
        sleep 0.5
        modern_spinner "sleep 2" "Bypassing firewalls"
        rainbow_progress 50 100 "Downloading data"
        sleep 0.5
        rainbow_progress 100 100 "Download complete"
        cyber_box "ACCESS GRANTED" "Welcome to the system."
        ;;
    help|*)
        glow_text "JARVIS COMMAND CENTER"
        echo ""
        echo "Usage: ./jarvis.sh [command]"
        echo ""
        echo "  setup   - Initialize environment and dependencies"
        echo "  start   - Launch backend and frontend"
        echo "  stop    - Stop all services"
        echo "  status  - Check system health"
        echo "  hack    - Run animation demo"
        echo ""
        ;;
esac
