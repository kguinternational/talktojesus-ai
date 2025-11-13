from flask import Flask, request, jsonify, Response, render_template, session
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
import random
import logging
from datetime import datetime, timedelta
from collections import defaultdict
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Simple in-memory storage for conversation history and rate limiting
conversation_history = defaultdict(list)
rate_limit_storage = defaultdict(list)


# Bible verses database
BIBLE_VERSES = {
    'love': [
        "Love one another as I have loved you. This is the greatest commandment. (John 13:34)",
        "Love is patient, love is kind. It does not envy, it does not boast. (1 Corinthians 13:4)",
        "Let all that you do be done in love, for love conquers all. (1 Corinthians 16:14)"
    ],
    'forgiveness': [
        "If you forgive others their trespasses, your heavenly Father will also forgive you. (Matthew 6:14)",
        "Come to me, all who are weary and burdened, and I will give you rest. (Matthew 11:28)",
        "As far as the east is from the west, so far has He removed our transgressions from us. (Psalm 103:12)"
    ],
    'faith': [
        "Have faith, for all things are possible to those who believe. (Mark 9:23)",
        "Trust in the Lord with all your heart, and lean not on your own understanding. (Proverbs 3:5)",
        "Faith is the substance of things hoped for, the evidence of things not seen. (Hebrews 11:1)"
    ],
    'guidance': [
        "Fear not, for I am with you always, even to the end of the age. (Matthew 28:20)",
        "Seek first the kingdom of God, and all these things will be added unto you. (Matthew 6:33)",
        "I am the way, the truth, and the life. Follow me and find peace. (John 14:6)"
    ],
    'strength': [
        "I can do all things through Christ who strengthens me. (Philippians 4:13)",
        "The Lord is my strength and my shield; my heart trusts in Him. (Psalm 28:7)",
        "Be strong and courageous. Do not be afraid; the Lord your God goes with you. (Deuteronomy 31:6)"
    ],
    'peace': [
        "Peace I leave with you; my peace I give you. Not as the world gives do I give to you. (John 14:27)",
        "Do not be anxious about anything, but in everything by prayer present your requests to God. (Philippians 4:6)",
        "Cast all your anxiety on Him because He cares for you. (1 Peter 5:7)"
    ],
    'hope': [
        "For I know the plans I have for you, plans to prosper you and not to harm you, plans to give you hope and a future. (Jeremiah 29:11)",
        "May the God of hope fill you with all joy and peace as you trust in Him. (Romans 15:13)",
        "Be joyful in hope, patient in affliction, faithful in prayer. (Romans 12:12)"
    ]
}

# Daily devotionals
DAILY_DEVOTIONALS = [
    {
        "title": "Walk in Love",
        "verse": "John 13:34",
        "content": "A new command I give you: Love one another. As I have loved you, so you must love one another.",
        "reflection": "Today, let love be your guide in all interactions. Show kindness to everyone you meet, for in doing so, you reflect my love to the world."
    },
    {
        "title": "Trust in Me",
        "verse": "Proverbs 3:5-6",
        "content": "Trust in the Lord with all your heart and lean not on your own understanding; in all your ways submit to Him, and He will make your paths straight.",
        "reflection": "Release your worries and trust in my plan. Even when the path is unclear, I am guiding your steps."
    },
    {
        "title": "Peace Beyond Understanding",
        "verse": "Philippians 4:7",
        "content": "And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus.",
        "reflection": "In the midst of chaos, seek my peace. It is a peace that the world cannot give, and no circumstance can take away."
    }
]


def rate_limit(max_requests=10, window_seconds=60):
    """Simple rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            identifier = request.remote_addr
            now = datetime.now()
            
            # Clean old requests
            rate_limit_storage[identifier] = [
                req_time for req_time in rate_limit_storage[identifier]
                if now - req_time < timedelta(seconds=window_seconds)
            ]
            
            if len(rate_limit_storage[identifier]) >= max_requests:
                return jsonify({
                    'error': 'Rate limit exceeded. Please try again later.',
                    'message': 'Too many requests. Peace, my child, there is time for all things.'
                }), 429
            
            rate_limit_storage[identifier].append(now)
            return f(*args, **kwargs)
        return wrapped
    return decorator


def detect_sentiment(text: str) -> str:
    """Detect basic sentiment from text"""
    text_lower = text.lower()
    
    # Negative emotions
    if any(word in text_lower for word in ['sad', 'depressed', 'hopeless', 'despair', 'grief', 'sorrow', 'crying']):
        return 'sadness'
    if any(word in text_lower for word in ['angry', 'mad', 'furious', 'rage', 'hate', 'frustrated']):
        return 'anger'
    if any(word in text_lower for word in ['anxious', 'worried', 'scared', 'afraid', 'fear', 'nervous', 'panic']):
        return 'anxiety'
    
    # Positive emotions
    if any(word in text_lower for word in ['happy', 'joy', 'grateful', 'blessed', 'thankful', 'praise']):
        return 'joy'
    
    return 'neutral'


def generate_ai_response(prompt: str, user_id: str = None) -> str:
    """
    Generate a contextual AI response in the persona of Jesus.
    Now includes sentiment detection and Bible verse references.
    """
    if not prompt or prompt.strip() == '':
        return "Peace be with you. How may I guide you today?"
    
    logger.info(f"Generating response for prompt: {prompt[:50]}...")
    
    # Store conversation history if user_id provided
    if user_id:
        conversation_history[user_id].append({
            'timestamp': datetime.now(),
            'user_message': prompt,
        })
        # Keep only last 10 messages
        conversation_history[user_id] = conversation_history[user_id][-10:]
    
    prompt_lower = prompt.lower()
    sentiment = detect_sentiment(prompt)
    
    # Respond to sentiment first
    if sentiment == 'sadness':
        responses = [
            "I see the sorrow in your heart, my child. Remember, blessed are those who mourn, for they shall be comforted. (Matthew 5:4)",
            "Your tears are not unseen. I am close to the brokenhearted and save those who are crushed in spirit. (Psalm 34:18)",
            "Come to me, all who are weary and burdened, and I will give you rest. (Matthew 11:28)"
        ]
        return random.choice(responses)
    
    if sentiment == 'anxiety':
        responses = [
            "Do not be anxious about anything. Cast all your anxiety on me because I care for you. (1 Peter 5:7)",
            "Peace I leave with you; my peace I give you. Let not your heart be troubled. (John 14:27)",
            "Fear not, for I am with you; be not dismayed, for I am your God. (Isaiah 41:10)"
        ]
        return random.choice(responses)
    
    if sentiment == 'anger':
        responses = [
            "Be slow to anger, for anger does not produce the righteousness of God. (James 1:19-20)",
            "Love your enemies and pray for those who persecute you. (Matthew 5:44)",
            "Forgive others as I have forgiven you. Let go of the anger that weighs on your heart. (Ephesians 4:32)"
        ]
        return random.choice(responses)
    
    if sentiment == 'joy':
        responses = [
            "Rejoice! This is the day the Lord has made. Be glad and celebrate! (Psalm 118:24)",
            "I rejoice with you! May your joy be full and your heart overflow with gratitude. (John 15:11)",
            "The joy of the Lord is your strength. Continue to walk in this blessing! (Nehemiah 8:10)"
        ]
        return random.choice(responses)
    
    # Topic-based responses with Bible verses
    if any(word in prompt_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        responses = [
            "Peace be with you, my child. What troubles your heart today?",
            "Blessings upon you. How may I help guide your path? (Matthew 5:9)",
            "Welcome, dear one. I am here to listen and offer wisdom. (Proverbs 2:6)"
        ]
        return random.choice(responses)
    
    if any(word in prompt_lower for word in ['love', 'loved', 'loving']):
        return random.choice(BIBLE_VERSES['love'])
    
    if any(word in prompt_lower for word in ['forgive', 'forgiveness', 'sorry', 'guilt']):
        return random.choice(BIBLE_VERSES['forgiveness'])
    
    if any(word in prompt_lower for word in ['faith', 'believe', 'trust', 'doubt']):
        return random.choice(BIBLE_VERSES['faith'])
    
    if any(word in prompt_lower for word in ['help', 'guide', 'lost', 'confused']):
        return random.choice(BIBLE_VERSES['guidance'])
    
    if any(word in prompt_lower for word in ['strength', 'strong', 'weak', 'tired']):
        return random.choice(BIBLE_VERSES['strength'])
    
    if any(word in prompt_lower for word in ['peace', 'calm', 'rest', 'quiet']):
        return random.choice(BIBLE_VERSES['peace'])
    
    if any(word in prompt_lower for word in ['hope', 'future', 'plans', 'tomorrow']):
        return random.choice(BIBLE_VERSES['hope'])
    
    if any(word in prompt_lower for word in ['pray', 'prayer']):
        return "When you pray, go into your room, close the door and pray to your Father. And your Father, who sees what is done in secret, will reward you. (Matthew 6:6)"
    
    # Default response
    return f"My child, you speak of important matters. Remember: 'In all your ways acknowledge Him, and He shall direct your paths.' (Proverbs 3:6) Walk in faith and peace."


@app.route('/')
def home():
    """Render the interactive demo homepage."""
    return render_template('index.html')


@app.route('/sms', methods=['POST'])
@rate_limit(max_requests=20, window_seconds=60)
def sms_reply():
    incoming_msg = request.form.get('Body', '')
    phone_number = request.form.get('From', 'unknown')
    
    logger.info(f"SMS from {phone_number}: {incoming_msg[:50]}...")
    
    response_msg = generate_ai_response(incoming_msg, user_id=phone_number)
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
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'Talk to Jesus AI',
        'timestamp': datetime.now().isoformat(),
        'version': '1.1.0'
    }), 200


@app.route('/api/devotional', methods=['GET'])
def get_daily_devotional():
    """Get a daily devotional message"""
    # Use day of year to select devotional
    day_index = datetime.now().timetuple().tm_yday % len(DAILY_DEVOTIONALS)
    devotional = DAILY_DEVOTIONALS[day_index]
    
    logger.info(f"Serving daily devotional: {devotional['title']}")
    
    return jsonify({
        'success': True,
        'devotional': devotional,
        'date': datetime.now().strftime('%Y-%m-%d')
    }), 200


@app.route('/api/prayer', methods=['POST'])
@rate_limit(max_requests=10, window_seconds=60)
def submit_prayer_request():
    """Submit a prayer request"""
    data = request.get_json()
    
    if not data or 'prayer' not in data:
        return jsonify({
            'error': 'Prayer request text is required',
            'message': 'Please share what is on your heart.'
        }), 400
    
    prayer_text = data.get('prayer', '')
    name = data.get('name', 'Anonymous')
    
    logger.info(f"Prayer request from {name}: {prayer_text[:50]}...")
    
    # In production, this would be saved to a database
    response_message = generate_ai_response(prayer_text, user_id=request.remote_addr)
    
    return jsonify({
        'success': True,
        'message': 'Your prayer has been received, my child.',
        'response': response_message,
        'encouragement': 'Continue to pray without ceasing, for the prayer of a righteous person is powerful and effective. (James 5:16)'
    }), 200


@app.route('/api/verse', methods=['GET'])
def get_random_verse():
    """Get a random Bible verse"""
    category = request.args.get('category', None)
    
    if category and category in BIBLE_VERSES:
        verse = random.choice(BIBLE_VERSES[category])
        return jsonify({
            'success': True,
            'verse': verse,
            'category': category
        }), 200
    else:
        # Random verse from any category
        all_verses = [verse for verses in BIBLE_VERSES.values() for verse in verses]
        verse = random.choice(all_verses)
        return jsonify({
            'success': True,
            'verse': verse,
            'categories': list(BIBLE_VERSES.keys())
        }), 200


@app.route('/api/conversation/history', methods=['GET'])
def get_conversation_history():
    """Get conversation history for a user"""
    user_id = request.args.get('user_id', request.remote_addr)
    
    history = conversation_history.get(user_id, [])
    
    return jsonify({
        'success': True,
        'user_id': user_id,
        'message_count': len(history),
        'history': [
            {
                'timestamp': msg['timestamp'].isoformat(),
                'message': msg['user_message']
            }
            for msg in history[-10:]  # Last 10 messages
        ]
    }), 200


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get application statistics"""
    total_conversations = sum(len(hist) for hist in conversation_history.values())
    active_users = len(conversation_history)
    
    return jsonify({
        'success': True,
        'statistics': {
            'total_conversations': total_conversations,
            'active_users': active_users,
            'available_categories': list(BIBLE_VERSES.keys()),
            'devotionals_available': len(DAILY_DEVOTIONALS)
        }
    }), 200


if __name__ == '__main__':
    # Run the app on all interfaces so it can be accessed externally
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
    app.run(host='0.0.0.0', port=port, debug=debug)
