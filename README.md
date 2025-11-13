# talktojesus-ai 🙏

Interactive AI that allows users to communicate with a Jesus persona via text, phone calls, Zoom & Google Meet meetings. Uses Twilio for SMS/voice and Zoom/Google Meet APIs.

## Features

### Core Features
- **💬 SMS Messaging**: Send text messages and receive spiritual guidance through SMS powered by Twilio integration
- **📞 Voice Calls**: Have spoken conversations with voice transcription and text-to-speech responses via Twilio Voice
- **🎥 Video Meetings**: Schedule Zoom or Google Meet sessions (placeholder implementation - requires API credentials)
- **🌐 Interactive Web Interface**: Test all endpoints directly from your browser

### Enhanced AI Capabilities (NEW)
- **🎭 Sentiment Detection**: AI detects emotional tone (sadness, anxiety, anger, joy) and responds with appropriate comfort
- **📖 Bible Verse Integration**: All responses include actual Bible verse references with chapter and verse citations
- **💭 Conversation History**: Tracks conversation context for more personalized responses
- **🧠 Expanded Response Categories**: Love, forgiveness, faith, guidance, strength, peace, hope, and more

### New API Endpoints
- **📿 Prayer Requests** (`POST /api/prayer`): Submit prayer requests and receive spiritual guidance
- **📚 Daily Devotionals** (`GET /api/devotional`): Get daily devotional messages with scripture and reflections
- **✝️ Bible Verse Library** (`GET /api/verse`): Access categorized Bible verses by topic
- **📊 Conversation History** (`GET /api/conversation/history`): View past conversation history
- **📈 Statistics** (`GET /api/stats`): View application usage statistics
- **❤️ Health Check** (`GET /health`): Monitor application health status

### Security & Performance
- **🛡️ Rate Limiting**: Protects endpoints from abuse (configurable limits per endpoint)
- **📝 Logging**: Comprehensive logging for monitoring and debugging
- **🔒 Session Management**: Secure session handling for user tracking

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

### Core Endpoints

#### `GET /`
Renders the interactive web interface for testing all endpoints.

#### `POST /sms`
Handles incoming SMS messages from Twilio with sentiment detection and conversation history.

**Parameters:**
- `Body` (form data): The text message content
- `From` (form data): Phone number (automatically tracked)

**Response:** TwiML XML with message response

**Rate Limit:** 20 requests per minute per phone number

#### `POST /voice`
Handles incoming voice calls with speech recognition from Twilio.

**Parameters:**
- `SpeechResult` (form data): The transcribed speech text

**Response:** TwiML XML with spoken response

#### `POST /create_zoom_meeting`
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

#### `POST /create_google_meet`
Creates a Google Meet (placeholder - requires Google Workspace API credentials).

**Response:**
```json
{
  "message": "Status message"
}
```

### New Enhanced Endpoints

#### `GET /health`
Health check endpoint for monitoring application status.

**Response:**
```json
{
  "status": "healthy",
  "service": "Talk to Jesus AI",
  "timestamp": "2024-01-01T12:00:00",
  "version": "1.1.0"
}
```

#### `POST /api/prayer`
Submit a prayer request and receive spiritual guidance.

**Request Body:**
```json
{
  "name": "John Doe",
  "prayer": "Please pray for my family's health"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Your prayer has been received, my child.",
  "response": "AI-generated spiritual guidance with Bible verse",
  "encouragement": "Continue to pray without ceasing..."
}
```

**Rate Limit:** 10 requests per minute

#### `GET /api/devotional`
Get today's daily devotional message.

**Response:**
```json
{
  "success": true,
  "devotional": {
    "title": "Walk in Love",
    "verse": "John 13:34",
    "content": "A new command I give you...",
    "reflection": "Today, let love be your guide..."
  },
  "date": "2024-01-01"
}
```

#### `GET /api/verse?category={category}`
Get a Bible verse by category or random if no category specified.

**Parameters:**
- `category` (optional): love, forgiveness, faith, guidance, strength, peace, hope

**Response:**
```json
{
  "success": true,
  "verse": "Love one another as I have loved you. (John 13:34)",
  "category": "love"
}
```

#### `GET /api/conversation/history?user_id={user_id}`
Get conversation history for a user.

**Parameters:**
- `user_id` (optional): User identifier (defaults to IP address)

**Response:**
```json
{
  "success": true,
  "user_id": "user123",
  "message_count": 5,
  "history": [
    {
      "timestamp": "2024-01-01T12:00:00",
      "message": "Hello"
    }
  ]
}
```

#### `GET /api/stats`
Get application statistics.

**Response:**
```json
{
  "success": true,
  "statistics": {
    "total_conversations": 150,
    "active_users": 25,
    "available_categories": ["love", "faith", "hope", ...],
    "devotionals_available": 3
  }
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

The enhanced `generate_ai_response()` function now includes:

**Sentiment Detection:**
- Automatically detects emotional state (sadness, anxiety, anger, joy)
- Responds with appropriate comfort and encouragement
- Includes relevant Bible verses for each emotional state

**Response Categories with Bible Verses:**
- Love (John 13:34, 1 Corinthians 13:4, etc.)
- Forgiveness (Matthew 6:14, Psalm 103:12, etc.)
- Faith (Mark 9:23, Hebrews 11:1, etc.)
- Guidance (Matthew 28:20, John 14:6, etc.)
- Strength (Philippians 4:13, Psalm 28:7, etc.)
- Peace (John 14:27, Philippians 4:6, etc.)
- Hope (Jeremiah 29:11, Romans 15:13, etc.)
- Prayer (Matthew 6:6)

**Conversation Context:**
- Tracks conversation history per user
- Maintains context across messages
- Stores last 10 messages per user

In a production environment, this could be enhanced with:
- Integration with OpenAI GPT, Anthropic Claude, or other LLMs
- More sophisticated sentiment analysis
- Persistent database storage for conversations
- Advanced natural language understanding

## Environment Variables

- `PORT`: Server port (default: 5000)
- `FLASK_DEBUG`: Enable debug mode (default: False, set to True for development)

Example:
```bash
PORT=8080 FLASK_DEBUG=False python3 app.py
```

## Production Deployment

For production deployment, consider:

1. **Disable debug mode** by setting `FLASK_DEBUG=False` or not setting it at all

2. **Use a production WSGI server** (e.g., Gunicorn):
   ```bash
   pip install gunicorn
   FLASK_DEBUG=False gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Set up Twilio webhooks** pointing to your deployed endpoints:
   - SMS webhook: `https://yourdomain.com/sms`
   - Voice webhook: `https://yourdomain.com/voice`

4. **Configure API credentials** for Zoom and Google Meet integrations

5. **Integrate with a real LLM** for better AI responses (OpenAI GPT, Anthropic Claude, etc.)

6. **Add authentication** and rate limiting for API endpoints

7. **Use environment variables** for sensitive configuration

8. **Enable HTTPS** with SSL/TLS certificates

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
