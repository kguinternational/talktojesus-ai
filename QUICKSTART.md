# Quick Start Guide - Talk to Jesus AI

## 🚀 Fastest Way to Get Started

### Option 1: Docker + ngrok (Recommended for Sharing)

```bash
# 1. Clone and navigate to the repository
git clone https://github.com/kguinternational/talktojesus-ai.git
cd talktojesus-ai

# 2. Start with Docker
docker-compose up -d

# 3. Install and setup ngrok
./setup_ngrok.sh
ngrok config add-authtoken YOUR_AUTHTOKEN

# 4. Expose your server
ngrok http 5000

# Your app is now accessible via the ngrok URL!
```

### Option 2: Local Python

```bash
# 1. Clone and navigate
git clone https://github.com/kguinternational/talktojesus-ai.git
cd talktojesus-ai

# 2. Setup Python environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py

# 5. In another terminal, expose with ngrok
ngrok http 5000
```

## 📱 Testing the API

Once running, test your endpoints:

```bash
# Test root endpoint
curl http://localhost:5000/

# Test SMS endpoint
curl -X POST http://localhost:5000/sms -d "Body=Hello Jesus"

# Test voice endpoint
curl -X POST http://localhost:5000/voice -d "SpeechResult=Bless me"
```

## 🌐 Share Your App

After starting ngrok, you'll get a public URL like:
```
https://abc123.ngrok.io
```

Share this URL with others, or use it as your Twilio webhook URL!

## 🔗 ngrok Web Interface

View all requests in real-time at: `http://localhost:4040`

## 🛑 Stop Everything

**Docker:**
```bash
docker-compose down
```

**ngrok:**
Press `Ctrl+C` in the ngrok terminal

**Python:**
Press `Ctrl+C` in the Flask terminal

## 📚 Next Steps

- Configure Twilio webhooks with your ngrok URL
- Integrate AI models for better responses
- Check the full README.md for advanced configuration
