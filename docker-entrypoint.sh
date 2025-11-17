#!/bin/bash

# Docker entrypoint script for Talk to Jesus AI
# Starts Flask app and optionally ngrok tunnel

echo "Starting Talk to Jesus AI..."

# Configure ngrok if authtoken is provided
if [ ! -z "$NGROK_AUTHTOKEN" ]; then
    echo "Configuring ngrok with provided authtoken..."
    ngrok config add-authtoken $NGROK_AUTHTOKEN
    
    # Start ngrok in background
    echo "Starting ngrok tunnel on port 5000..."
    ngrok http 5000 --log=stdout > /var/log/ngrok.log 2>&1 &
    
    # Wait a moment for ngrok to start
    sleep 3
    
    # Try to get the public URL
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*' | grep -o 'https://[^"]*' | head -1)
    
    if [ ! -z "$NGROK_URL" ]; then
        echo "=========================================="
        echo "✓ ngrok tunnel started successfully!"
        echo "Public URL: $NGROK_URL"
        echo "ngrok Web Interface: http://localhost:4040"
        echo "=========================================="
    else
        echo "⚠ ngrok started but URL not yet available"
        echo "Check http://localhost:4040 for tunnel details"
    fi
else
    echo "⚠ NGROK_AUTHTOKEN not set. Skipping ngrok setup."
    echo "To enable ngrok, set NGROK_AUTHTOKEN environment variable."
    echo "Get your token from: https://dashboard.ngrok.com/get-started/your-authtoken"
fi

# Start Flask application
echo "Starting Flask application on 0.0.0.0:5000..."
echo "=========================================="
python app.py
