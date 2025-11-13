#!/bin/bash

# Talk to Jesus AI - Launch Script

echo "=================================================="
echo "  🙏 Talk to Jesus AI - Starting Application 🙏  "
echo "=================================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if dependencies are installed
if ! python3 -c "import flask" &> /dev/null; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
    echo ""
fi

echo "✅ Dependencies installed"
echo ""

# Set default port if not specified
if [ -z "$PORT" ]; then
    export PORT=5000
fi

echo "🚀 Starting Flask application on port $PORT..."
echo ""
echo "📱 Access the web interface at: http://localhost:$PORT"
echo "📖 API Documentation available in README.md"
echo ""
echo "Press CTRL+C to stop the server"
echo "=================================================="
echo ""

# Run the Flask app
python3 app.py
