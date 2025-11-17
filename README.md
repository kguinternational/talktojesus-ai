# talktojesus-ai

Interactive AI that allows users to communicate with a Jesus persona via text, phone calls, Zoom &amp; Google Meet meetings. Uses Twilio for SMS/voice and Zoom/Google Meet APIs.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

**OR**

- Docker and Docker Compose (for containerized deployment)

## Quick Start with Docker (Recommended)

The easiest way to run the application is using Docker with built-in ngrok support:

### Option 1: Docker with ngrok (Get Public URL)

```bash
# Clone the repository
git clone https://github.com/kguinternational/talktojesus-ai.git
cd talktojesus-ai

# Copy and configure environment file
cp .env.example .env
# Edit .env and add your NGROK_AUTHTOKEN (get from https://dashboard.ngrok.com)

# Build and run with Docker Compose (includes ngrok)
docker-compose up -d

# View logs to see your ngrok public URL
docker-compose logs -f

# Stop the application
docker-compose down
```

### Option 2: Docker without ngrok

```bash
# Run without ngrok authtoken
docker-compose up -d

# View logs
docker-compose logs -f
```

**Access Points:**
- Flask App: `http://localhost:5000`
- ngrok Web UI: `http://localhost:4040` (if ngrok authtoken is configured)
- Public URL: Shown in logs when ngrok is enabled

## Local Setup and Installation (Without Docker)

### 1. Clone the Repository

```bash
git clone https://github.com/kguinternational/talktojesus-ai.git
cd talktojesus-ai
```

### 2. Create a Virtual Environment (Recommended)

```bash
# On Linux/MacOS
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

The application will start on `http://0.0.0.0:5000`, making it accessible at:
- `http://localhost:5000` (from the same machine)
- `http://127.0.0.1:5000` (from the same machine)
- `http://<your-ip-address>:5000` (from other machines on your network)

Visit `http://localhost:5000` in your browser to verify the API is running.

## API Endpoints

The application provides the following endpoints:

### Root Endpoint
- **URL**: `/`
- **Method**: `GET`
- **Description**: Returns API status and available endpoints

### SMS Endpoint
- **URL**: `/sms`
- **Method**: `POST`
- **Description**: Handles incoming SMS messages via Twilio
- **Parameters**: `Body` - The incoming SMS message text

### Voice Endpoint
- **URL**: `/voice`
- **Method**: `POST`
- **Description**: Handles incoming voice calls via Twilio
- **Parameters**: `SpeechResult` - The transcribed speech from the caller

### Zoom Meeting Creation
- **URL**: `/create_zoom_meeting`
- **Method**: `POST`
- **Description**: Creates a Zoom meeting (placeholder - not yet implemented)
- **Parameters**: `topic` - Meeting topic (JSON)

### Google Meet Creation
- **URL**: `/create_google_meet`
- **Method**: `POST`
- **Description**: Creates a Google Meet (placeholder - not yet implemented)

## Testing Locally

You can test the root endpoint to verify the API is running:

```bash
curl http://localhost:5000/
```

You can test the SMS endpoint using curl:

```bash
curl -X POST http://localhost:5000/sms \
  -d "Body=Hello Jesus"
```

You can test the voice endpoint:

```bash
curl -X POST http://localhost:5000/voice \
  -d "SpeechResult=Hello Jesus"
```

## Configuration

## Exposing Your Local Server with ngrok

To share your local development server with others or to use Twilio webhooks, you need to expose it to the internet using ngrok.

### Install ngrok

**Option 1: Using the setup script (Linux/macOS)**
```bash
./setup_ngrok.sh
```

**Option 2: Manual installation**

On **Linux**:
```bash
curl -sL https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz -o ngrok.tgz
tar -xzf ngrok.tgz
sudo mv ngrok /usr/local/bin/
```

On **macOS**:
```bash
brew install ngrok/ngrok/ngrok
```

On **Windows**:
Download from [ngrok.com/download](https://ngrok.com/download) and add to PATH.

### Configure ngrok

1. **Sign up** for a free account at [ngrok.com](https://dashboard.ngrok.com/signup)
2. **Get your authtoken** from [your dashboard](https://dashboard.ngrok.com/get-started/your-authtoken)
3. **Add the authtoken**:
```bash
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```

### Start ngrok Tunnel

**Method 1: Simple command**
```bash
# Start your Flask app first
python app.py

# In another terminal, start ngrok
ngrok http 5000
```

**Method 2: Using configuration file**
```bash
# Copy the example config
cp ngrok.yml.example ~/.config/ngrok/ngrok.yml
# Edit and add your authtoken
nano ~/.config/ngrok/ngrok.yml

# Start the tunnel with config
ngrok start talktojesus
```

### Access Your Public URL

After starting ngrok, you'll see output like:
```
Session Status                online
Account                       your@email.com
Version                       3.x.x
Region                        United States (us)
Forwarding                    https://abc123.ngrok.io -> http://localhost:5000
```

Your app is now accessible at the `https://abc123.ngrok.io` URL!

### View Requests in Real-Time

Open the ngrok web interface at `http://localhost:4040` to:
- Inspect HTTP requests and responses
- Replay requests
- View request/response details

### Twilio Setup (Optional for SMS/Voice)

To use Twilio features with your ngrok URL:

1. **Create a Twilio account** at [twilio.com](https://www.twilio.com)
2. **Get a Twilio phone number** with SMS and Voice capabilities
3. **Configure webhooks** in Twilio Console:
   - **SMS Webhook**: `https://your-ngrok-url.ngrok.io/sms`
   - **Voice Webhook**: `https://your-ngrok-url.ngrok.io/voice`
4. **Add credentials** to `.env` file (copy from `.env.example`)

Now you can send SMS messages or make calls to your Twilio number, and they'll be handled by your local application!

## Docker Commands

### Build the Docker image:
```bash
docker build -t talktojesus-ai .
```

### Run the container with ngrok:
```bash
# With ngrok authtoken
docker run -d \
  -p 5000:5000 \
  -p 4040:4040 \
  -e NGROK_AUTHTOKEN=your_token_here \
  --name talktojesus-ai \
  talktojesus-ai

# Without ngrok (local only)
docker run -d -p 5000:5000 --name talktojesus-ai talktojesus-ai
```

### Using Docker Compose (Recommended):
```bash
# Start with ngrok (set NGROK_AUTHTOKEN in .env first)
docker-compose up -d

# View logs (including ngrok public URL)
docker-compose logs -f

# Stop the application
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

### Access the container:
```bash
docker exec -it talktojesus-ai /bin/bash
```

### Check ngrok status inside container:
```bash
# View ngrok web interface
curl http://localhost:4040/api/tunnels

# Or open in browser
open http://localhost:4040
```

## Project Structure

```
talktojesus-ai/
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker container configuration
├── docker-compose.yml    # Docker Compose orchestration
├── .dockerignore         # Files to exclude from Docker builds
├── .gitignore            # Git ignore rules
├── .env.example          # Environment variable template
├── setup_ngrok.sh        # ngrok installation script
├── ngrok.yml.example     # ngrok configuration template
└── README.md             # This file
```

## Development

The application runs in debug mode by default when using `python app.py`. Any changes to the code will automatically reload the server.

⚠️ **Security Warning**: Debug mode is enabled for local development convenience. **Never use debug mode in production** as it can expose sensitive information and allow arbitrary code execution. For production deployment, use a production WSGI server like Gunicorn or uWSGI with debug mode disabled.

## Future Enhancements

- Integrate with actual AI language models for Jesus persona responses
- Implement Zoom API integration for meeting creation
- Implement Google Meet API integration
- Add authentication and authorization
- Add database for conversation history
- Enhance AI response generation with context and personality

## License

[Add your license here]

## Support

For issues or questions, please open an issue on the GitHub repository.
