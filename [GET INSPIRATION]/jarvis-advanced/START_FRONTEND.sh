#!/bin/bash
# Start Frontend - Auto-fix port issues

echo "🌐 Starting JARVIS Frontend..."
echo ""

# Kill any old servers
pkill -f "http.server 5173" 2>/dev/null
pkill -f "http.server 8080" 2>/dev/null
sleep 1

cd "$(dirname "$0")/frontend"

# Try port 5173 first
echo "📡 Starting server on http://localhost:5173"
echo ""
echo "✨ Open your browser to: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python3 -m http.server 5173
