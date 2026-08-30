import os
import requests
from flask import Flask, request, jsonify, Response, send_from_directory
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__, static_folder='public', static_url_path='')


def generate_ai_response(prompt: str) -> str:
    """Generate compassionate, scripture-inspired responses for the Jesus persona."""
    if not prompt or not prompt.strip():
        return "Peace be with you. What is on your heart today?"
    
    clean_prompt = prompt.strip().lower()
    
    if any(w in clean_prompt for w in ['hello', 'hi', 'greetings', 'hey']):
        return "Peace be with you. I am here to listen. What troubles or questions rest upon your mind today?"
    
    if any(w in clean_prompt for w in ['fear', 'afraid', 'scared', 'worry', 'anxious', 'anxiety']):
        return "Do not be anxious about tomorrow, for tomorrow will care for itself. Peace I leave with you; my peace I give to you. Trust, and cast your burdens upon me."
    
    if any(w in clean_prompt for w in ['love', 'lonely', 'alone', 'heartbreak']):
        return "You are never truly alone. Love one another as I have loved you. Greater love has no one than this, and my presence remains with you always."
    
    if any(w in clean_prompt for w in ['hope', 'help', 'guidance', 'pray', 'prayer']):
        return "Ask and it will be given to you; seek and you will find; knock and the door will be opened to you. Keep faith in your heart."
    
    return f"I hear your words: '{prompt}'. Walk in love, faith, and grace, knowing that every step in humility brings light to your path."


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return response


@app.route('/')
def serve_index():
    return send_from_directory('public', 'index.html')


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'online',
        'service': 'Talk-to-Jesus.ai',
        'platform': 'Netlify Serverless'
    })


@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    data = request.get_json(silent=True) or {}
    message = data.get('message', request.form.get('message', ''))
    
    reply = generate_ai_response(message)
    return jsonify({
        'success': True,
        'message': message,
        'response': reply
    })


@app.route('/sms', methods=['POST'])
def sms_reply():
    incoming_msg = request.form.get('Body', '')
    response_msg = generate_ai_response(incoming_msg)
    resp = MessagingResponse()
    resp.message(response_msg)
    return Response(str(resp), mimetype='application/xml')


@app.route('/voice', methods=['POST'])
def voice_reply():
    incoming_msg = request.values.get('SpeechResult', '')
    response_text = generate_ai_response(incoming_msg)
    vr = VoiceResponse()
    vr.say(response_text)
    return Response(str(vr), mimetype='application/xml')


@app.route('/create_zoom_meeting', methods=['POST', 'OPTIONS'])
def create_zoom_meeting():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    data = request.get_json(silent=True) or {}
    topic = data.get('topic', 'Talk to Jesus Meeting')
    email = data.get('email', 'user@example.com')
    
    return jsonify({
        'success': True,
        'status': 'scheduled',
        'provider': 'Zoom',
        'topic': topic,
        'email': email,
        'join_url': f"https://zoom.us/j/sandbox-talk-to-jesus-meeting",
        'message': 'Zoom prayer session mock endpoint ready. Configure ZOOM_JWT / OAuth credentials in Netlify env vars.'
    }), 200


@app.route('/create_google_meet', methods=['POST', 'OPTIONS'])
def create_google_meet():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    data = request.get_json(silent=True) or {}
    topic = data.get('topic', 'Talk to Jesus Session')
    email = data.get('email', 'user@example.com')
    
    return jsonify({
        'success': True,
        'status': 'scheduled',
        'provider': 'Google Meet',
        'topic': topic,
        'email': email,
        'meet_url': f"https://meet.google.com/talk-to-jesus-session",
        'message': 'Google Meet prayer session mock endpoint ready. Configure Google Workspace credentials in Netlify env vars.'
    }), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
