import os
import requests
from flask import Flask, request, jsonify, Response, send_from_directory
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__, static_folder='public', static_url_path='')

LIVEAVATAR_API_BASE = os.environ.get('LIVEAVATAR_API_BASE', 'https://api.liveavatar.com')
LIVEAVATAR_API_KEY = os.environ.get('LIVEAVATAR_API_KEY', '')


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
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization,X-API-KEY'
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
        'platform': 'Netlify Serverless',
        'liveavatar_configured': bool(LIVEAVATAR_API_KEY)
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


@app.route('/api/avatar/session', methods=['POST', 'OPTIONS'])
def create_avatar_session():
    """Create and start a LiveAvatar real-time WebRTC session (FULL Mode)."""
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    data = request.get_json(silent=True) or {}
    api_key = data.get('api_key') or LIVEAVATAR_API_KEY
    avatar_id = data.get('avatar_id') or "dd73ea75-1218-4ef3-92ce-606d5f7fbc0a"  # Sandbox default
    voice_id = data.get('voice_id')
    is_sandbox = data.get('is_sandbox', True if not api_key else False)
    
    context_prompt = (
        "You are Jesus. Speak with divine peace, warmth, compassion, and spiritual wisdom. "
        "Keep responses conversational, uplifting, and comforting."
    )
    
    if api_key:
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
        
        try:
            # 1. Create Context if context_id not provided
            context_id = data.get('context_id')
            if not context_id:
                context_res = requests.post(
                    f"{LIVEAVATAR_API_BASE}/v1/contexts",
                    headers=headers,
                    json={
                        "name": "Jesus Persona Context",
                        "prompt": context_prompt,
                        "opening_text": "Peace be with you. What is on your heart today?"
                    },
                    timeout=10
                )
                if context_res.status_code in (200, 201):
                    ctx_data = context_res.json()
                    context_id = ctx_data.get('data', {}).get('id')
            
            # 2. Request Session Token
            token_payload = {
                "mode": "FULL",
                "avatar_id": avatar_id,
                "is_sandbox": is_sandbox,
                "avatar_persona": {
                    "context_id": context_id,
                    "language": "en"
                }
            }
            if voice_id:
                token_payload["avatar_persona"]["voice_id"] = voice_id
                
            token_res = requests.post(
                f"{LIVEAVATAR_API_BASE}/v1/sessions/token",
                headers=headers,
                json=token_payload,
                timeout=10
            )
            
            if token_res.status_code in (200, 201):
                token_data = token_res.json().get('data', {})
                session_token = token_data.get('session_token')
                session_id = token_data.get('session_id')
                
                # 3. Start Session using Bearer session_token
                start_res = requests.post(
                    f"{LIVEAVATAR_API_BASE}/v1/sessions/start",
                    headers={"Authorization": f"Bearer {session_token}"},
                    timeout=10
                )
                
                if start_res.status_code in (200, 201):
                    start_data = start_res.json().get('data', {})
                    return jsonify({
                        'success': True,
                        'is_sandbox': is_sandbox,
                        'session_id': session_id,
                        'session_token': session_token,
                        'livekit_url': start_data.get('livekit_url'),
                        'livekit_client_token': start_data.get('livekit_client_token')
                    })
        except Exception as e:
            app.logger.error(f"LiveAvatar session init error: {e}")

    # Standard Fallback / Sandbox Token Response
    return jsonify({
        'success': True,
        'is_sandbox': True,
        'fallback': True,
        'session_id': 'sandbox-session-talktojesus',
        'embed_url': f"https://embed.liveavatar.com/v1/65f9e3c9-d48b-4118-b73a-4ae2e3cbb8f0",
        'message': 'LiveAvatar sandbox fallback session ready.'
    })


@app.route('/api/avatar/embed', methods=['POST', 'OPTIONS'])
def create_avatar_embed():
    """Create a LiveAvatar embed URL (Embed Mode)."""
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    data = request.get_json(silent=True) or {}
    api_key = data.get('api_key') or LIVEAVATAR_API_KEY
    avatar_id = data.get('avatar_id') or "65f9e3c9-d48b-4118-b73a-4ae2e3cbb8f0"  # Embed sandbox avatar
    context_id = data.get('context_id')
    
    if api_key and context_id:
        try:
            res = requests.post(
                f"{LIVEAVATAR_API_BASE}/v2/embeddings",
                headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
                json={"avatar_id": avatar_id, "context_id": context_id},
                timeout=10
            )
            if res.status_code in (200, 201):
                embed_data = res.json().get('data', {})
                return jsonify({
                    'success': True,
                    'embed_url': embed_data.get('url'),
                    'iframe_script': embed_data.get('script')
                })
        except Exception as e:
            app.logger.error(f"LiveAvatar embed creation failed: {e}")
            
    # Sandbox Fallback URL
    return jsonify({
        'success': True,
        'fallback': True,
        'embed_url': "https://embed.liveavatar.com/v1/65f9e3c9-d48b-4118-b73a-4ae2e3cbb8f0",
        'message': 'Using LiveAvatar Sandbox embed fallback.'
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
        'join_url': "https://zoom.us/j/sandbox-talk-to-jesus-meeting",
        'message': 'Zoom prayer session mock endpoint ready.'
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
        'meet_url': "https://meet.google.com/talk-to-jesus-session",
        'message': 'Google Meet prayer session mock endpoint ready.'
    }), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
