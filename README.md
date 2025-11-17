# talktojesus-ai

Interactive AI that allows users to communicate with a Jesus persona via text, phone calls, Zoom &amp; Google Meet meetings. Uses Twilio for SMS/voice and Zoom/Google Meet APIs.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Local Setup and Installation

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

The application will start on `http://127.0.0.1:5000` by default.

## API Endpoints

The application provides the following endpoints:

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

You can test the SMS endpoint using curl:

```bash
curl -X POST http://127.0.0.1:5000/sms \
  -d "Body=Hello Jesus"
```

You can test the voice endpoint:

```bash
curl -X POST http://127.0.0.1:5000/voice \
  -d "SpeechResult=Hello Jesus"
```

## Configuration

### Twilio Setup (Optional for Local Testing)

To use Twilio features, you'll need:
1. A Twilio account (sign up at https://www.twilio.com)
2. Twilio phone numbers configured for SMS and Voice
3. Webhook URLs pointing to your endpoints

For local development with Twilio, you can use tools like [ngrok](https://ngrok.com/) to expose your local server:

```bash
ngrok http 5000
```

Then configure your Twilio phone numbers to use the ngrok URLs.

## Project Structure

```
talktojesus-ai/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Development

The application runs in debug mode by default when using `python app.py`. Any changes to the code will automatically reload the server.

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
