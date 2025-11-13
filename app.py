"""Talk to Jesus AI - Main Flask application."""
from flask import Flask, request, jsonify, Response, redirect, session, url_for
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import os
from datetime import datetime

from config import get_config
from logger import setup_logger
from ai_service import ai_service
from zoom_service import zoom_service
from google_meet_service import google_meet_service

# Initialize Flask app
app = Flask(__name__)
config = get_config()
app.config.from_object(config)

# Setup logging
logger = setup_logger(__name__, level=config.LOG_LEVEL)

# Setup CORS
CORS(app)

# Setup rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[config.RATE_LIMIT]
)

# Twilio validator for webhook security
twilio_validator = RequestValidator(config.TWILIO_AUTH_TOKEN) if config.TWILIO_AUTH_TOKEN else None


def validate_twilio_request():
    """Validate that request is from Twilio."""
    if not twilio_validator or app.config.get('TESTING'):
        return True
    
    url = request.url
    signature = request.headers.get('X-Twilio-Signature', '')
    params = request.form.to_dict()
    
    return twilio_validator.validate(url, params, signature)


def sanitize_input(text: str, max_length: int = None) -> str:
    """Sanitize and validate user input."""
    if not text:
        return ""
    
    # Strip whitespace
    text = text.strip()
    
    # Limit length
    max_len = max_length or config.MAX_MESSAGE_LENGTH
    if len(text) > max_len:
        text = text[:max_len]
    
    return text


@app.route('/')
def index():
    """Root endpoint with API information."""
    return jsonify({
        'service': 'Talk to Jesus AI',
        'version': '1.0.0',
        'description': 'Interactive AI for spiritual conversations',
        'endpoints': {
            'health': '/health',
            'sms': '/sms (POST)',
            'voice': '/voice (POST)',
            'zoom': '/create_zoom_meeting (POST)',
            'google_meet': '/create_google_meet (POST)',
            'google_auth': '/google_auth (GET)',
            'oauth_callback': '/oauth2callback (GET)'
        }
    })


@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'services': {
            'ai_provider': ai_service.provider or 'fallback',
            'zoom_configured': zoom_service.is_configured(),
            'google_meet_configured': google_meet_service.is_configured()
        }
    })


@app.route('/sms', methods=['POST'])
@limiter.limit("20 per minute")
def sms_reply():
    """Handle incoming SMS messages via Twilio."""
    try:
        # Validate Twilio request
        if not validate_twilio_request():
            logger.warning("Invalid Twilio signature")
            return jsonify({'error': 'Unauthorized'}), 401
        
        # Get and sanitize incoming message
        incoming_msg = request.form.get('Body', '')
        incoming_msg = sanitize_input(incoming_msg)
        
        logger.info(f"Received SMS: {incoming_msg[:50]}...")
        
        # Generate AI response
        response_msg = ai_service.generate_response(incoming_msg)
        
        # Create Twilio response
        resp = MessagingResponse()
        resp.message(response_msg)
        
        logger.info(f"Sent SMS response: {response_msg[:50]}...")
        return str(resp), 200, {'Content-Type': 'text/xml'}
    
    except Exception as e:
        logger.error(f"Error in SMS handler: {str(e)}", exc_info=True)
        resp = MessagingResponse()
        resp.message("I am having trouble responding right now. Please try again in a moment.")
        return str(resp), 200, {'Content-Type': 'text/xml'}


@app.route('/voice', methods=['POST'])
@limiter.limit("20 per minute")
def voice_reply():
    """Handle incoming voice calls via Twilio."""
    try:
        # Validate Twilio request
        if not validate_twilio_request():
            logger.warning("Invalid Twilio signature")
            return jsonify({'error': 'Unauthorized'}), 401
        
        # Get speech result or setup speech recognition
        incoming_msg = request.values.get('SpeechResult', '')
        
        vr = VoiceResponse()
        
        if incoming_msg:
            # We have speech input, generate response
            incoming_msg = sanitize_input(incoming_msg)
            logger.info(f"Received voice input: {incoming_msg[:50]}...")
            
            response_text = ai_service.generate_response(incoming_msg)
            vr.say(response_text, voice='alice')
            
            # Ask if they want to continue
            vr.say("Would you like to say something else?")
            gather = Gather(input='speech', action='/voice', timeout=3, speech_timeout='auto')
            vr.append(gather)
            
            logger.info(f"Sent voice response: {response_text[:50]}...")
        else:
            # Initial call, prompt for input
            vr.say("Peace be with you. I am here to listen. Please speak your heart.", voice='alice')
            gather = Gather(input='speech', action='/voice', timeout=5, speech_timeout='auto')
            vr.append(gather)
            vr.say("I did not hear anything. God bless you.")
        
        return str(vr), 200, {'Content-Type': 'text/xml'}
    
    except Exception as e:
        logger.error(f"Error in voice handler: {str(e)}", exc_info=True)
        vr = VoiceResponse()
        vr.say("I am having trouble responding right now. Please try calling again.", voice='alice')
        return str(vr), 200, {'Content-Type': 'text/xml'}


@app.route('/create_zoom_meeting', methods=['POST'])
@limiter.limit("5 per minute")
def create_zoom_meeting():
    """Create a Zoom meeting."""
    try:
        if not zoom_service.is_configured():
            return jsonify({
                'error': 'Zoom service not configured',
                'message': 'Please configure ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET, and ZOOM_ACCOUNT_ID'
            }), 503
        
        # Get parameters from request
        data = request.get_json() or {}
        topic = data.get('topic', 'Talk to Jesus Meeting')
        duration = int(data.get('duration', 30))
        timezone = data.get('timezone', 'UTC')
        
        # Create meeting
        meeting = zoom_service.create_meeting(
            topic=topic,
            duration=duration,
            timezone=timezone
        )
        
        logger.info(f"Created Zoom meeting: {meeting['id']}")
        return jsonify({
            'success': True,
            'meeting': meeting
        }), 201
    
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating Zoom meeting: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Failed to create Zoom meeting',
            'message': str(e)
        }), 500


@app.route('/google_auth')
def google_auth():
    """Redirect user to Google OAuth consent screen."""
    try:
        if not google_meet_service.is_configured():
            return jsonify({
                'error': 'Google Meet service not configured',
                'message': 'Please configure GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET'
            }), 503
        
        auth_url = google_meet_service.get_oauth_url()
        return redirect(auth_url)
    
    except Exception as e:
        logger.error(f"Error initiating Google auth: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/oauth2callback')
def oauth2callback():
    """Handle OAuth callback from Google."""
    try:
        code = request.args.get('code')
        if not code:
            return jsonify({'error': 'No authorization code received'}), 400
        
        # Exchange code for tokens
        tokens = google_meet_service.exchange_code_for_token(code)
        
        # In production, store tokens securely (database, session, etc.)
        session['google_access_token'] = tokens.get('access_token')
        session['google_refresh_token'] = tokens.get('refresh_token')
        
        return jsonify({
            'success': True,
            'message': 'Successfully authenticated with Google',
            'next_step': 'You can now create Google Meet meetings via /create_google_meet'
        })
    
    except Exception as e:
        logger.error(f"Error in OAuth callback: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/create_google_meet', methods=['POST'])
@limiter.limit("5 per minute")
def create_google_meet():
    """Create a Google Meet meeting."""
    try:
        if not google_meet_service.is_configured():
            return jsonify({
                'error': 'Google Meet service not configured',
                'message': 'Please configure GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET'
            }), 503
        
        # Check for access token
        access_token = session.get('google_access_token')
        if not access_token:
            return jsonify({
                'error': 'Not authenticated',
                'message': 'Please authenticate first via /google_auth',
                'auth_url': url_for('google_auth', _external=True)
            }), 401
        
        google_meet_service.set_access_token(access_token)
        
        # Get parameters from request
        data = request.get_json() or {}
        summary = data.get('summary', 'Talk to Jesus Meeting')
        duration = int(data.get('duration', 30))
        timezone = data.get('timezone', 'UTC')
        description = data.get('description', '')
        
        # Create meeting
        meeting = google_meet_service.create_meeting(
            summary=summary,
            duration=duration,
            timezone=timezone,
            description=description
        )
        
        logger.info(f"Created Google Meet: {meeting['id']}")
        return jsonify({
            'success': True,
            'meeting': meeting
        }), 201
    
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating Google Meet: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Failed to create Google Meet',
            'message': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}", exc_info=True)
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Validate configuration
    missing = config.validate()
    if missing:
        logger.warning(f"Configuration warnings: {', '.join(missing)}")
    
    # Run app
    logger.info(f"Starting Talk to Jesus AI on {config.HOST}:{config.PORT}")
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
