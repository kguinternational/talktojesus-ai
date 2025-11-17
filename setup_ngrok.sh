#!/bin/bash

# Setup script for ngrok
echo "Setting up ngrok for Talk to Jesus AI..."

# Check if ngrok is already installed
if command -v ngrok &> /dev/null; then
    echo "✓ ngrok is already installed"
    ngrok version
else
    echo "Installing ngrok..."
    
    # Detect OS
    OS=$(uname -s)
    ARCH=$(uname -m)
    
    if [ "$OS" = "Linux" ]; then
        if [ "$ARCH" = "x86_64" ]; then
            curl -sL https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz -o /tmp/ngrok.tgz
        elif [ "$ARCH" = "aarch64" ]; then
            curl -sL https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz -o /tmp/ngrok.tgz
        fi
        tar -xzf /tmp/ngrok.tgz -C /tmp
        sudo mv /tmp/ngrok /usr/local/bin/
        rm /tmp/ngrok.tgz
    elif [ "$OS" = "Darwin" ]; then
        # macOS
        brew install ngrok/ngrok/ngrok
    else
        echo "Unsupported OS: $OS"
        echo "Please install ngrok manually from: https://ngrok.com/download"
        exit 1
    fi
    
    echo "✓ ngrok installed successfully"
fi

# Check if authtoken is set
echo ""
echo "To use ngrok, you need to:"
echo "1. Sign up for a free account at https://dashboard.ngrok.com/signup"
echo "2. Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken"
echo "3. Run: ngrok config add-authtoken YOUR_AUTHTOKEN"
echo ""

# Check if authtoken is configured
if ngrok config check &> /dev/null; then
    echo "✓ ngrok authtoken is configured"
else
    echo "⚠ Please configure your ngrok authtoken"
    echo "Run: ngrok config add-authtoken YOUR_AUTHTOKEN"
fi

echo ""
echo "Setup complete!"
echo ""
echo "To start sharing your local server:"
echo "1. Start the Flask app: python app.py"
echo "2. In another terminal, run: ngrok http 5000"
echo "3. Copy the public URL from ngrok output"
