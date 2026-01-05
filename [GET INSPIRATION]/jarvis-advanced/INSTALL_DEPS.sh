!/bin/bash
# One-Time Setup - Install All Dependencies

echo "🔧 Installing JARVIS dependencies..."
echo ""

# Check if conda is available
if command -v conda &> /dev/null; then
    echo "📦 Using Conda to install..."
    conda install -y -c conda-forge fastapi uvicorn websockets python-multipart
else
    echo "📦 Using pip to install..."
    pip install fastapi uvicorn websockets python-multipart
fi

echo ""
echo "✅ All dependencies installed!"
echo ""
echo "🚀 You can now run:"
echo "   ./START_BACKEND.sh"
