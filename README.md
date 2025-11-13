# Talk to Jesus AI

Interactive AI application that allows users to have spiritual conversations with a Jesus persona via multiple channels:
- 📱 SMS text messages (Twilio)
- 📞 Voice calls (Twilio Voice)
- 🎥 Video meetings (Zoom)
- 💬 Google Meet conferences

## Features

- **Multi-channel Communication**: SMS, voice calls, video meetings
- **AI-Powered Responses**: Integrates with OpenAI GPT or Anthropic Claude
- **RESTful API**: Well-documented endpoints for all functionality
- **Security**: Rate limiting, input validation, webhook verification
- **Production Ready**: Docker support, proper logging, health checks
- **Comprehensive Tests**: Full test suite with pytest

## Quick Start

### Prerequisites

- Python 3.11+
- Twilio account (for SMS/voice)
- OpenAI or Anthropic API key (for AI responses)
- Zoom account (optional, for video meetings)
- Google Cloud account (optional, for Google Meet)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/kguinternational/talktojesus-ai.git
cd talktojesus-ai
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys and credentials
```

5. **Run the application**
```bash
python app.py
```

The server will start on `http://localhost:5000`

## Configuration

Copy `.env.example` to `.env` and configure the following:

### Required Settings
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` - AI provider API key
- `TWILIO_ACCOUNT_SID` - Your Twilio account SID
- `TWILIO_AUTH_TOKEN` - Your Twilio auth token
- `TWILIO_PHONE_NUMBER` - Your Twilio phone number

### Optional Settings
- `ZOOM_CLIENT_ID`, `ZOOM_CLIENT_SECRET`, `ZOOM_ACCOUNT_ID` - For Zoom integration
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` - For Google Meet integration
- `FLASK_ENV` - Environment (development/production)
- `LOG_LEVEL` - Logging level (DEBUG/INFO/WARNING/ERROR)

## API Endpoints

### Health Check
```bash
GET /health
```
Returns service health status and configuration info.

### SMS Messaging
```bash
POST /sms
Body: Body=Your message here
```
Twilio webhook for handling incoming SMS messages.

### Voice Calls
```bash
POST /voice
```
Twilio webhook for handling incoming voice calls with speech recognition.

### Create Zoom Meeting
```bash
POST /create_zoom_meeting
Content-Type: application/json

{
  "topic": "Talk to Jesus Meeting",
  "duration": 30,
  "timezone": "UTC"
}
```

### Create Google Meet
```bash
POST /create_google_meet
Content-Type: application/json

{
  "summary": "Talk to Jesus Meeting",
  "duration": 30,
  "timezone": "UTC"
}
```

### Google Authentication
```bash
GET /google_auth
```
Initiates OAuth flow for Google Calendar/Meet access.

## Docker Deployment

### Using Docker
```bash
docker build -t talktojesus-ai .
docker run -p 5000:5000 --env-file .env talktojesus-ai
```

### Using Docker Compose
```bash
docker-compose up -d
```

## Heroku Deployment

1. **Create Heroku app**
```bash
heroku create your-app-name
```

2. **Set environment variables**
```bash
heroku config:set OPENAI_API_KEY=your_key
heroku config:set TWILIO_ACCOUNT_SID=your_sid
# ... set other variables
```

3. **Deploy**
```bash
git push heroku main
```

## Testing

### Run all tests
```bash
pytest
```

### Run with coverage
```bash
pytest --cov=. --cov-report=html
```

### Run specific test file
```bash
pytest tests/test_app.py
```

## Code Quality

### Format code with Black
```bash
black .
```

### Run linter
```bash
pylint *.py
```

### Type checking
```bash
mypy *.py
```

## Development

### Project Structure
```
talktojesus-ai/
├── app.py                  # Main Flask application
├── config.py               # Configuration management
├── logger.py               # Logging setup
├── ai_service.py           # AI response generation
├── zoom_service.py         # Zoom integration
├── google_meet_service.py  # Google Meet integration
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── Procfile              # Heroku configuration
├── pytest.ini            # Pytest configuration
├── .pylintrc             # Pylint configuration
├── pyproject.toml        # Tool configuration
├── .env.example          # Environment template
└── tests/                # Test suite
    ├── conftest.py
    ├── test_app.py
    └── test_ai_service.py
```

## Twilio Configuration

### SMS Setup
1. Purchase a Twilio phone number
2. Configure webhook URL: `https://your-domain.com/sms`
3. Set HTTP POST method

### Voice Setup
1. Configure voice webhook URL: `https://your-domain.com/voice`
2. Enable speech recognition in Twilio console
3. Set HTTP POST method

## Security Considerations

- All Twilio webhooks are validated with signature verification
- Rate limiting is enabled on all endpoints
- Input sanitization prevents injection attacks
- CORS is configured for API access
- Environment variables for sensitive data
- HTTPS recommended for production

## Troubleshooting

### AI responses not working
- Verify your API key is correct in `.env`
- Check the logs for API errors
- Ensure you have sufficient API credits

### Twilio webhooks failing
- Verify webhook URLs are publicly accessible
- Check Twilio signature validation
- Review Twilio debugger logs

### Zoom/Google Meet not working
- Ensure OAuth credentials are configured
- Complete authentication flow for Google
- Verify account permissions

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Open a GitHub issue
- Check existing documentation
- Review Twilio/Zoom/Google API docs

## Acknowledgments

- Built with Flask and Python
- Powered by OpenAI GPT / Anthropic Claude
- SMS/Voice via Twilio
- Video meetings via Zoom and Google Meet
