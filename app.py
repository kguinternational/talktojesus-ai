from flask import Flask, request, jsonify, Response
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# System prompt for Jesus AI persona
JESUS_SYSTEM_PROMPT = """You are an AI representation of Jesus Christ, designed to provide spiritual guidance, 
wisdom, and compassionate responses based on Christian teachings and biblical principles. 
Your responses should be:
- Compassionate and loving
- Grounded in biblical teachings
- Encouraging and uplifting
- Non-judgmental yet truthful
- Simple yet profound

Speak in a warm, accessible manner that reflects Jesus's teachings of love, forgiveness, and grace.
Keep responses concise and meaningful, appropriate for text/voice communication."""


def generate_ai_response(prompt: str) -> str:
    """Generate AI response using OpenAI with Jesus persona."""
    try:
        if not os.getenv('OPENAI_API_KEY'):
            return "I am here with you, but I need proper configuration to speak. Please set up the OpenAI API key."
        
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": JESUS_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        app.logger.error(f"Error generating AI response: {e}")
        return "Peace be with you. I'm having difficulty responding right now. Please try again."


@app.route('/sms', methods=['POST'])
def sms_reply():
    incoming_msg = request.form.get('Body', '')
    response_msg = generate_ai_response(incoming_msg)
    resp = MessagingResponse()
    resp.message(response_msg)
    return str(resp)


@app.route('/voice', methods=['POST'])
def voice_reply():
    # Twilio sends transcribed speech as SpeechResult when using Twilio Voice with speech recognition
    incoming_msg = request.values.get('SpeechResult', '')
    response_text = generate_ai_response(incoming_msg)
    vr = VoiceResponse()
    vr.say(response_text)
    return str(vr)


@app.route('/create_zoom_meeting', methods=['POST'])
def create_zoom_meeting():
    """Create a Zoom meeting via Zoom API (placeholder)."""
    topic = request.json.get('topic', 'Talk to Jesus Meeting')
    # TODO: Implement Zoom API call to create a meeting using JWT or OAuth credentials
    return jsonify({'message': 'Zoom meeting creation not implemented in this skeleton.'}), 501


@app.route('/create_google_meet', methods=['POST'])
def create_google_meet():
    """Create a Google Meet via Google Meet REST API (placeholder)."""
    # TODO: Implement Google Meet API call to create a meeting via Google Workspace
    return jsonify({'message': 'Google Meet creation not implemented in this skeleton.'}), 501


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the service is running."""
    return jsonify({
        'status': 'healthy',
        'service': 'Talk to Jesus AI',
        'openai_configured': bool(os.getenv('OPENAI_API_KEY'))
    })


@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API information."""
    return jsonify({
        'service': 'Talk to Jesus AI',
        'version': '1.0.0',
        'endpoints': {
            '/sms': 'POST - Handle SMS messages via Twilio',
            '/voice': 'POST - Handle voice calls via Twilio',
            '/create_zoom_meeting': 'POST - Create Zoom meeting (not yet implemented)',
            '/create_google_meet': 'POST - Create Google Meet (not yet implemented)',
            '/health': 'GET - Health check'
        }
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
