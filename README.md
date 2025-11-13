# talktojesus-ai 🙏

Interactive AI that allows users to communicate with a Jesus persona via text, phone calls, Zoom & Google Meet meetings. Uses Twilio for SMS/voice and Zoom/Google Meet APIs.

## Features

- **💬 SMS Messaging**: Send text messages and receive spiritual guidance through SMS powered by Twilio integration
- **📞 Voice Calls**: Have spoken conversations with voice transcription and text-to-speech responses via Twilio Voice
- **🎥 Video Meetings**: Schedule Zoom or Google Meet sessions (placeholder implementation - requires API credentials)
- **🌐 Interactive Web Interface**: Test all endpoints directly from your browser

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

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

### Running the Application

Start the Flask development server:

```bash
python3 app.py
```

The application will start on `http://localhost:5000`

You can also specify a custom port:
```bash
PORT=8080 python3 app.py
```

### Using the Application

1. **Web Interface**: Open your browser and navigate to `http://localhost:5000`
   - Test the SMS endpoint with the interactive chat
   - Try the voice endpoint simulation
   - Explore the video meeting placeholders

2. **SMS Endpoint** (`POST /sms`):
   ```bash
   curl -X POST http://localhost:5000/sms -d "Body=Hello"
   ```

3. **Voice Endpoint** (`POST /voice`):
   ```bash
   curl -X POST http://localhost:5000/voice -d "SpeechResult=I need guidance"
   ```

4. **Zoom Meeting** (`POST /create_zoom_meeting`):
   ```bash
   curl -X POST http://localhost:5000/create_zoom_meeting \
     -H "Content-Type: application/json" \
     -d '{"topic":"Spiritual Guidance Session"}'
   ```

5. **Google Meet** (`POST /create_google_meet`):
   ```bash
   curl -X POST http://localhost:5000/create_google_meet \
     -H "Content-Type: application/json" \
     -d '{}'
   ```

## API Endpoints

### `GET /`
Renders the interactive web interface for testing all endpoints.

### `POST /sms`
Handles incoming SMS messages from Twilio.

**Parameters:**
- `Body` (form data): The text message content

**Response:** TwiML XML with message response

### `POST /voice`
Handles incoming voice calls with speech recognition from Twilio.

**Parameters:**
- `SpeechResult` (form data): The transcribed speech text

**Response:** TwiML XML with spoken response

### `POST /create_zoom_meeting`
Creates a Zoom meeting (placeholder - requires Zoom API credentials).

**Request Body:**
```json
{
  "topic": "Meeting topic"
}
```

**Response:**
```json
{
  "message": "Status message"
}
```

### `POST /create_google_meet`
Creates a Google Meet (placeholder - requires Google Workspace API credentials).

**Response:**
```json
{
  "message": "Status message"
}
```

## Development

### Project Structure

```
talktojesus-ai/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   └── index.html     # Interactive web interface
├── static/            # Static assets (CSS, JS, images)
└── README.md          # This file
```

### AI Response Generation

The `generate_ai_response()` function in `app.py` provides keyword-based responses in the persona of Jesus. In a production environment, this would be replaced with calls to a language model API (OpenAI, Anthropic, etc.).

Current response categories:
- Greetings
- Questions about love
- Questions about forgiveness
- Questions about faith
- Questions about help/guidance
- General spiritual wisdom

## Production Deployment

For production deployment, consider:

1. **Use a production WSGI server** (e.g., Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Set up Twilio webhooks** pointing to your deployed endpoints:
   - SMS webhook: `https://yourdomain.com/sms`
   - Voice webhook: `https://yourdomain.com/voice`

3. **Configure API credentials** for Zoom and Google Meet integrations

4. **Integrate with a real LLM** for better AI responses (OpenAI GPT, Anthropic Claude, etc.)

5. **Add authentication** and rate limiting for API endpoints

6. **Use environment variables** for sensitive configuration

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
