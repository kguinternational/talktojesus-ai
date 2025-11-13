# Talk to Jesus AI - API Documentation

Complete API reference for the Talk to Jesus AI service.

## Base URL

```
https://your-domain.com
```

For local development:
```
http://localhost:5000
```

## Authentication

### Twilio Webhooks
Twilio webhooks are automatically validated using request signatures. Ensure your `TWILIO_AUTH_TOKEN` is configured correctly.

### API Endpoints
Most API endpoints use rate limiting. Default: 10 requests per minute.

## Endpoints

### 1. Health Check

Check service status and configuration.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "services": {
    "ai_provider": "openai",
    "zoom_configured": true,
    "google_meet_configured": true
  }
}
```

### 2. Service Information

Get API information and available endpoints.

**Endpoint:** `GET /`

**Response:**
```json
{
  "service": "Talk to Jesus AI",
  "version": "1.0.0",
  "description": "Interactive AI for spiritual conversations",
  "endpoints": {
    "health": "/health",
    "sms": "/sms (POST)",
    "voice": "/voice (POST)",
    "zoom": "/create_zoom_meeting (POST)",
    "google_meet": "/create_google_meet (POST)"
  }
}
```

### 3. SMS Handler

Handle incoming SMS messages from Twilio.

**Endpoint:** `POST /sms`

**Headers:**
- `X-Twilio-Signature`: Twilio request signature

**Form Data:**
- `Body` (string): The incoming SMS message text
- `From` (string): Sender's phone number
- `To` (string): Receiver's phone number

**Response:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message>Peace be with you. How may I help you today?</Message>
</Response>
```

**Rate Limit:** 20 requests per minute

### 4. Voice Handler

Handle incoming voice calls from Twilio with speech recognition.

**Endpoint:** `POST /voice`

**Headers:**
- `X-Twilio-Signature`: Twilio request signature

**Form Data:**
- `SpeechResult` (string, optional): Transcribed speech from caller
- `CallSid` (string): Unique call identifier

**Response:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="alice">Peace be with you. I am here to listen.</Say>
  <Gather input="speech" action="/voice" timeout="5" speechTimeout="auto"/>
</Response>
```

**Rate Limit:** 20 requests per minute

### 5. Create Zoom Meeting

Create a new Zoom meeting.

**Endpoint:** `POST /create_zoom_meeting`

**Headers:**
- `Content-Type: application/json`

**Request Body:**
```json
{
  "topic": "Talk to Jesus Meeting",
  "duration": 30,
  "timezone": "UTC"
}
```

**Parameters:**
- `topic` (string, optional): Meeting title. Default: "Talk to Jesus Meeting"
- `duration` (integer, optional): Duration in minutes. Default: 30
- `timezone` (string, optional): Meeting timezone. Default: "UTC"

**Success Response (201):**
```json
{
  "success": true,
  "meeting": {
    "id": "123456789",
    "topic": "Talk to Jesus Meeting",
    "join_url": "https://zoom.us/j/123456789",
    "start_url": "https://zoom.us/s/123456789",
    "start_time": "2024-01-01T12:00:00Z",
    "duration": 30,
    "password": "abc123"
  }
}
```

**Error Response (503):**
```json
{
  "error": "Zoom service not configured",
  "message": "Please configure ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET, and ZOOM_ACCOUNT_ID"
}
```

**Rate Limit:** 5 requests per minute

### 6. Google Authentication

Initiate Google OAuth flow for Calendar/Meet access.

**Endpoint:** `GET /google_auth`

**Response:** Redirects to Google OAuth consent screen

**Success:** Redirects to `/oauth2callback` with authorization code

**Error Response (503):**
```json
{
  "error": "Google Meet service not configured",
  "message": "Please configure GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET"
}
```

### 7. OAuth Callback

Handle OAuth callback from Google (automatic).

**Endpoint:** `GET /oauth2callback`

**Query Parameters:**
- `code` (string): Authorization code from Google

**Success Response (200):**
```json
{
  "success": true,
  "message": "Successfully authenticated with Google",
  "next_step": "You can now create Google Meet meetings via /create_google_meet"
}
```

### 8. Create Google Meet

Create a new Google Meet via Calendar API.

**Endpoint:** `POST /create_google_meet`

**Headers:**
- `Content-Type: application/json`

**Prerequisites:** Must authenticate via `/google_auth` first

**Request Body:**
```json
{
  "summary": "Talk to Jesus Meeting",
  "duration": 30,
  "timezone": "UTC",
  "description": "A spiritual conversation"
}
```

**Parameters:**
- `summary` (string, optional): Meeting title. Default: "Talk to Jesus Meeting"
- `duration` (integer, optional): Duration in minutes. Default: 30
- `timezone` (string, optional): Meeting timezone. Default: "UTC"
- `description` (string, optional): Meeting description

**Success Response (201):**
```json
{
  "success": true,
  "meeting": {
    "id": "event123",
    "summary": "Talk to Jesus Meeting",
    "meet_link": "https://meet.google.com/abc-defg-hij",
    "html_link": "https://calendar.google.com/event?eid=...",
    "start_time": "2024-01-01T12:00:00Z",
    "end_time": "2024-01-01T12:30:00Z",
    "status": "confirmed"
  }
}
```

**Error Response (401):**
```json
{
  "error": "Not authenticated",
  "message": "Please authenticate first via /google_auth",
  "auth_url": "http://localhost:5000/google_auth"
}
```

**Rate Limit:** 5 requests per minute

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Invalid signature or missing authentication"
}
```

### 404 Not Found
```json
{
  "error": "Endpoint not found"
}
```

### 429 Too Many Requests
```json
{
  "error": "Rate limit exceeded"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

### 503 Service Unavailable
```json
{
  "error": "Service not configured",
  "message": "Required credentials are missing"
}
```

## Rate Limits

- Default: 10 requests per minute
- SMS/Voice endpoints: 20 requests per minute
- Meeting creation endpoints: 5 requests per minute

## Examples

### cURL Examples

**Health Check:**
```bash
curl http://localhost:5000/health
```

**Create Zoom Meeting:**
```bash
curl -X POST http://localhost:5000/create_zoom_meeting \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "My Meeting",
    "duration": 60,
    "timezone": "America/New_York"
  }'
```

**Create Google Meet:**
```bash
curl -X POST http://localhost:5000/create_google_meet \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "My Meeting",
    "duration": 45
  }'
```

### Python Examples

```python
import requests

# Health check
response = requests.get('http://localhost:5000/health')
print(response.json())

# Create Zoom meeting
response = requests.post(
    'http://localhost:5000/create_zoom_meeting',
    json={
        'topic': 'My Meeting',
        'duration': 30
    }
)
print(response.json())
```

### JavaScript Examples

```javascript
// Health check
fetch('http://localhost:5000/health')
  .then(response => response.json())
  .then(data => console.log(data));

// Create Zoom meeting
fetch('http://localhost:5000/create_zoom_meeting', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    topic: 'My Meeting',
    duration: 30
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## Webhooks

### Configuring Twilio Webhooks

1. Log into Twilio Console
2. Go to Phone Numbers → Manage → Active Numbers
3. Select your phone number
4. Under "Messaging", set:
   - Webhook URL: `https://your-domain.com/sms`
   - HTTP Method: POST
5. Under "Voice & Fax", set:
   - Webhook URL: `https://your-domain.com/voice`
   - HTTP Method: POST

## Best Practices

1. **Always use HTTPS in production** for security
2. **Store access tokens securely** (database, encrypted storage)
3. **Implement proper error handling** on client side
4. **Respect rate limits** to avoid throttling
5. **Validate webhook signatures** for security
6. **Use environment variables** for configuration
7. **Monitor logs** for errors and issues

## Support

For questions or issues with the API:
- Check the main README.md
- Review error messages and logs
- Open a GitHub issue
- Consult Twilio/Zoom/Google API documentation
