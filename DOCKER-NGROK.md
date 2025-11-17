# Docker + ngrok Integration Guide

## Overview

ngrok is now fully integrated into the Docker container. When you start the container, both Flask and ngrok start automatically if you provide an authtoken.

## Quick Setup

### Step 1: Get Your ngrok Authtoken

1. Visit [ngrok.com](https://dashboard.ngrok.com/signup) and create a free account
2. Go to [Your Authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
3. Copy your authtoken

### Step 2: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your ngrok authtoken
nano .env
```

Add this line to your `.env` file:
```
NGROK_AUTHTOKEN=your_actual_authtoken_here
```

### Step 3: Start Everything

```bash
# Build and start (Flask + ngrok)
docker-compose up -d

# View logs to see your public URL
docker-compose logs -f
```

You'll see output like:
```
==========================================
✓ ngrok tunnel started successfully!
Public URL: https://abc123.ngrok.io
ngrok Web Interface: http://localhost:4040
==========================================
Starting Flask application on 0.0.0.0:5000...
```

## Access Points

After starting the container:

| Service | URL | Description |
|---------|-----|-------------|
| Flask App (Local) | http://localhost:5000 | Your local Flask application |
| Flask App (Public) | https://abc123.ngrok.io | Public URL via ngrok (shown in logs) |
| ngrok Inspector | http://localhost:4040 | Real-time request inspection |

## Usage Examples

### Share with Others

Send them your ngrok URL:
```
https://abc123.ngrok.io
```

They can access:
- `https://abc123.ngrok.io/` - API status
- `https://abc123.ngrok.io/sms` - SMS endpoint
- `https://abc123.ngrok.io/voice` - Voice endpoint

### Configure Twilio Webhooks

Use your ngrok URL in Twilio Console:
- **SMS Webhook**: `https://abc123.ngrok.io/sms`
- **Voice Webhook**: `https://abc123.ngrok.io/voice`

### Inspect Requests

Open http://localhost:4040 to see:
- All HTTP requests in real-time
- Request/response details
- Ability to replay requests
- Request history

## Running Without ngrok

If you don't need a public URL, simply don't set `NGROK_AUTHTOKEN`:

```bash
# Start without ngrok (local only)
docker-compose up -d
```

The container will start Flask on http://localhost:5000 without ngrok.

## Troubleshooting

### ngrok Not Starting

**Check logs:**
```bash
docker-compose logs -f
```

**Common issues:**
- Invalid or missing authtoken
- Port 5000 already in use
- Network connectivity issues

### Can't Access Public URL

1. Ensure ngrok started successfully (check logs)
2. Visit http://localhost:4040 to see tunnel status
3. Verify your authtoken is valid
4. Check firewall settings

### Get Container Shell

```bash
docker exec -it talktojesus-ai /bin/bash

# Inside container, check ngrok status
curl http://localhost:4040/api/tunnels
```

## Advanced Configuration

### Custom ngrok Configuration

You can mount a custom ngrok config:

```yaml
# docker-compose.yml
volumes:
  - .:/app
  - ./ngrok.yml:/root/.config/ngrok/ngrok.yml
```

### Environment Variables

Available environment variables:

- `NGROK_AUTHTOKEN` - Your ngrok authtoken (required for ngrok)
- `FLASK_ENV` - Flask environment (default: development)
- `FLASK_DEBUG` - Flask debug mode (default: True)

### Stop and Restart

```bash
# Stop
docker-compose down

# Rebuild and restart
docker-compose up -d --build

# View logs
docker-compose logs -f
```

## Benefits

✅ **No Installation Required** - Everything in Docker
✅ **Automatic Startup** - ngrok starts with Flask
✅ **Environment-Based Config** - Use .env file
✅ **Optional** - Works with or without ngrok
✅ **Portable** - Same setup on any machine with Docker
✅ **Integrated Logging** - See everything in one place
