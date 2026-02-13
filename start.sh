#!/bin/bash
# SafetyNomad AI - Start Script

cd "$(dirname "$0")"

echo "🛡️  Starting SafetyNomad AI..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r backend/requirements.txt

# Start the server
echo ""
echo "🚀 SafetyNomad AI is running!"
echo ""
echo "   Open in browser: http://localhost:8000"
echo "   On your phone:   http://$(ipconfig getifaddr en0):8000"
echo ""
echo "   Press Ctrl+C to stop"
echo ""

cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
