from flask import Flask, request, jsonify, Response, render_template
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
import random

app = Flask(__name__)


def generate_ai_response(prompt: str) -> str:
    """
    Generate a contextual AI response in the persona of Jesus.
    In a production environment, this would call an LLM API.
    """
    if not prompt or prompt.strip() == '':
        return "Peace be with you. How may I guide you today?"
    
    # Simple keyword-based responses for demonstration
    prompt_lower = prompt.lower()
    
    # Greetings
    if any(word in prompt_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        responses = [
            "Peace be with you, my child. What troubles your heart today?",
            "Blessings upon you. How may I help guide your path?",
            "Welcome, dear one. I am here to listen and offer wisdom."
        ]
        return random.choice(responses)
    
    # Questions about love
    if any(word in prompt_lower for word in ['love', 'loved', 'loving']):
        responses = [
            "Love one another as I have loved you. This is the greatest commandment.",
            "Love is patient, love is kind. It does not envy, it does not boast.",
            "Let all that you do be done in love, for love conquers all."
        ]
        return random.choice(responses)
    
    # Questions about forgiveness
    if any(word in prompt_lower for word in ['forgive', 'forgiveness', 'sorry', 'guilt']):
        responses = [
            "Forgive others, as you have been forgiven. Let go of what weighs upon your heart.",
            "If you forgive others their trespasses, your heavenly Father will also forgive you.",
            "Come to me, all who are weary and burdened, and I will give you rest."
        ]
        return random.choice(responses)
    
    # Questions about faith
    if any(word in prompt_lower for word in ['faith', 'believe', 'trust', 'doubt']):
        responses = [
            "Have faith, for all things are possible to those who believe.",
            "Trust in the Lord with all your heart, and lean not on your own understanding.",
            "Faith is the substance of things hoped for, the evidence of things not seen."
        ]
        return random.choice(responses)
    
    # Questions about help/guidance
    if any(word in prompt_lower for word in ['help', 'guide', 'lost', 'confused', 'worried']):
        responses = [
            "Fear not, for I am with you always. Cast your burdens upon me.",
            "Seek first the kingdom of God, and all these things will be added unto you.",
            "I am the way, the truth, and the life. Follow me and find peace."
        ]
        return random.choice(responses)
    
    # Default response
    return f"My child, you speak of '{prompt[:50]}...' - remember that even in trials, there is purpose. Walk in faith and peace."


@app.route('/')
def home():
    """Render the interactive demo homepage."""
    return render_template('index.html')


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


if __name__ == '__main__':
    # Run the app on all interfaces so it can be accessed externally
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
