# Talk to Jesus AI

Interactive AI that allows users to communicate with a Jesus persona via text, phone calls, Zoom &amp; Google Meet meetings. Uses OpenAI for intelligent responses, Twilio for SMS/voice, and Zoom/Google Meet APIs.

## Features

- 🤖 AI-powered Jesus persona using OpenAI GPT models
- 📱 SMS messaging via Twilio
- 📞 Voice calls via Twilio
- 🎥 Zoom meeting integration (planned)
- 💬 Google Meet integration (planned)

## Setup

### Prerequisites

- Python 3.8+
- OpenAI API key
- Twilio account (for SMS/voice features)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/kguinternational/talktojesus-ai.git
cd talktojesus-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

4. Run the application:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

- `GET /` - Service information
- `GET /health` - Health check
- `POST /sms` - Handle incoming SMS messages
- `POST /voice` - Handle incoming voice calls
- `POST /create_zoom_meeting` - Create Zoom meeting (not yet implemented)
- `POST /create_google_meet` - Create Google Meet (not yet implemented)

## Configuration

Set the following environment variables in your `.env` file:

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `FLASK_ENV` - Flask environment (development/production)
- `FLASK_DEBUG` - Enable Flask debug mode (True/False)
- `PORT` - Server port (default: 5000)

## Usage

### Testing SMS Endpoint

```bash
curl -X POST http://localhost:5000/sms \
  -d "Body=Hello, Jesus. Can you help me?"
```

### Testing Voice Endpoint

```bash
curl -X POST http://localhost:5000/voice \
  -d "SpeechResult=I need guidance"
```

## Docker Deployment

### Using Docker

Build and run with Docker:
```bash
docker build -t talktojesus-ai .
docker run -p 5000:5000 -e OPENAI_API_KEY=your_key_here talktojesus-ai
```

### Using Docker Compose

```bash
# Make sure .env file exists with your API keys
docker-compose up -d
```

## Deployment

This application can be deployed to any platform that supports Python Flask applications:
- **Docker** - Use the provided Dockerfile and docker-compose.yml
- **Heroku** - Deploy directly from Git
- **AWS Elastic Beanstalk** - Python platform
- **Google Cloud Platform** - App Engine or Cloud Run
- **Railway** - Auto-detect Python application

### Environment Variables for Production

Ensure these environment variables are set in your production environment:
- `OPENAI_API_KEY` (required)
- `FLASK_ENV=production`
- `FLASK_DEBUG=False`
- `PORT` (if required by platform)

## License

MIT License
