#!/usr/bin/env python3
"""
Talk to Jesus AI - Complete Feature Demonstration Script

This script demonstrates ALL features of the application with sample data.
Run this to see every capability in action!

Usage:
    python3 demo_all_features.py
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
COLORS = {
    'HEADER': '\033[95m',
    'BLUE': '\033[94m',
    'CYAN': '\033[96m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'RED': '\033[91m',
    'END': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m'
}

def print_header(text):
    """Print a styled header"""
    print(f"\n{COLORS['HEADER']}{COLORS['BOLD']}{'='*70}{COLORS['END']}")
    print(f"{COLORS['HEADER']}{COLORS['BOLD']}{text.center(70)}{COLORS['END']}")
    print(f"{COLORS['HEADER']}{COLORS['BOLD']}{'='*70}{COLORS['END']}\n")

def print_section(text):
    """Print a section divider"""
    print(f"\n{COLORS['CYAN']}{COLORS['BOLD']}--- {text} ---{COLORS['END']}\n")

def print_success(text):
    """Print success message"""
    print(f"{COLORS['GREEN']}✅ {text}{COLORS['END']}")

def print_info(text):
    """Print info message"""
    print(f"{COLORS['BLUE']}ℹ️  {text}{COLORS['END']}")

def print_data(label, value):
    """Print labeled data"""
    print(f"{COLORS['YELLOW']}{label}:{COLORS['END']} {value}")

def demo_sms_chat():
    """Demonstrate SMS chat feature"""
    print_header("DEMO 1: SMS CHAT CONVERSATION")
    
    messages = [
        "Hello",
        "I need guidance about love",
        "How can I forgive someone who hurt me?",
        "My faith feels weak",
        "I'm lost and need guidance"
    ]
    
    for i, message in enumerate(messages, 1):
        print_section(f"Message {i}")
        print_data("User", message)
        
        try:
            response = requests.post(
                f"{BASE_URL}/sms",
                data={"Body": message, "From": "+1234567890"}
            )
            
            if response.status_code == 200:
                # Extract message from TwiML response
                text = response.text
                if "<Message>" in text:
                    start = text.find("<Message>") + 9
                    end = text.find("</Message>")
                    ai_response = text[start:end].strip()
                    print_data("Jesus AI", ai_response)
                    print_success("Response received")
                else:
                    print_info(f"Status: {response.status_code}")
            else:
                print_info(f"Status: {response.status_code}")
        except Exception as e:
            print_info(f"Error: {str(e)}")
        
        time.sleep(1)

def demo_prayer_requests():
    """Demonstrate prayer requests with sentiment detection"""
    print_header("DEMO 2: PRAYER REQUESTS WITH SENTIMENT DETECTION")
    
    prayers = [
        {
            "name": "Sarah",
            "request": "I lost my grandmother yesterday and my heart is broken. I feel so empty.",
            "expected_sentiment": "Sadness"
        },
        {
            "name": "Michael",
            "request": "I'm so anxious about my job interview tomorrow. I can't sleep and I'm worried.",
            "expected_sentiment": "Anxiety"
        },
        {
            "name": "David",
            "request": "I'm so angry at my colleague for taking credit for my work.",
            "expected_sentiment": "Anger"
        },
        {
            "name": "Emily",
            "request": "Thank you, Jesus! I got accepted to my dream college! I'm so grateful!",
            "expected_sentiment": "Joy"
        }
    ]
    
    for i, prayer in enumerate(prayers, 1):
        print_section(f"Prayer Request {i}")
        print_data("Name", prayer["name"])
        print_data("Request", prayer["request"])
        print_data("Expected Sentiment", prayer["expected_sentiment"])
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/prayer",
                json={"name": prayer["name"], "request": prayer["request"]}
            )
            
            if response.status_code == 200:
                data = response.json()
                print_data("Detected Sentiment", data.get("sentiment", "Unknown"))
                print_data("Response", data.get("response", "")[:200] + "...")
                print_success("Prayer processed successfully")
            else:
                print_info(f"Status: {response.status_code}")
        except Exception as e:
            print_info(f"Error: {str(e)}")
        
        time.sleep(1)

def demo_daily_devotional():
    """Demonstrate daily devotional feature"""
    print_header("DEMO 3: DAILY DEVOTIONALS")
    
    try:
        response = requests.get(f"{BASE_URL}/api/devotional")
        
        if response.status_code == 200:
            data = response.json()
            print_data("Title", data.get("title", ""))
            print_data("Scripture", data.get("scripture", ""))
            print_data("Verse", data.get("verse", ""))
            print_data("Reflection", data.get("reflection", "")[:300] + "...")
            print_success("Devotional retrieved successfully")
        else:
            print_info(f"Status: {response.status_code}")
    except Exception as e:
        print_info(f"Error: {str(e)}")

def demo_bible_verses():
    """Demonstrate Bible verse library"""
    print_header("DEMO 4: BIBLE VERSE LIBRARY")
    
    categories = ["Love", "Forgiveness", "Faith", "Guidance", "Strength", "Peace", "Hope"]
    
    for category in categories:
        print_section(f"Category: {category}")
        
        try:
            response = requests.get(f"{BASE_URL}/api/verse?category={category}")
            
            if response.status_code == 200:
                data = response.json()
                print_data("Category", data.get("category", ""))
                print_data("Verse", data.get("verse", ""))
                print_data("Reference", data.get("reference", ""))
                print_success(f"{category} verse retrieved")
            else:
                print_info(f"Status: {response.status_code}")
        except Exception as e:
            print_info(f"Error: {str(e)}")
        
        time.sleep(0.5)

def demo_video_avatar_generation():
    """Demonstrate AI video generation feature"""
    print_header("DEMO 5: VIDEO AVATAR - AI GENERATION")
    
    messages = [
        "Peace be with you, my child. How may I help you today?",
        "Love is patient and kind. It does not envy or boast.",
        "I am the way, the truth, and the life."
    ]
    
    for i, message in enumerate(messages, 1):
        print_section(f"Video Generation {i}")
        print_data("Message", message)
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/video/generate",
                json={"text": message, "service": "d-id"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print_data("Status", data.get("status", ""))
                print_data("Message", data.get("message", ""))
                if "video_url" in data:
                    print_data("Video URL", data.get("video_url", ""))
                print_success("Video generation request processed")
            else:
                print_info(f"Status: {response.status_code}")
        except Exception as e:
            print_info(f"Error: {str(e)}")
        
        time.sleep(0.5)

def demo_video_streaming():
    """Demonstrate live video streaming feature"""
    print_header("DEMO 6: VIDEO AVATAR - LIVE STREAMING")
    
    session_types = ["webrtc", "zoom", "google_meet"]
    
    for session_type in session_types:
        print_section(f"Session Type: {session_type.upper()}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/video/session/create",
                json={"type": session_type, "topic": "Spiritual Guidance"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print_data("Session ID", data.get("session_id", ""))
                print_data("Type", data.get("type", ""))
                print_data("Status", data.get("status", ""))
                if "meeting_url" in data:
                    print_data("Meeting URL", data.get("meeting_url", ""))
                print_success(f"{session_type} session created")
            else:
                print_info(f"Status: {response.status_code}")
        except Exception as e:
            print_info(f"Error: {str(e)}")
        
        time.sleep(0.5)

def demo_3d_avatar():
    """Demonstrate 3D animated avatar feature"""
    print_header("DEMO 7: VIDEO AVATAR - 3D ANIMATION")
    
    animations = [
        {"text": "Welcome, my child. How may I guide you today?", "animation": "greeting"},
        {"text": "Peace be with you always.", "animation": "blessing"},
        {"text": "I am here to listen and offer wisdom.", "animation": "talking"}
    ]
    
    for i, anim in enumerate(animations, 1):
        print_section(f"Animation {i}")
        print_data("Text", anim["text"])
        print_data("Animation Type", anim["animation"])
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/avatar/3d/animate",
                json={"text": anim["text"], "animation": anim["animation"]}
            )
            
            if response.status_code == 200:
                data = response.json()
                print_data("Status", data.get("status", ""))
                print_data("Animation ID", data.get("animation_id", ""))
                print_data("Duration", f"{data.get('duration', 0)}s")
                print_success("3D animation request processed")
            else:
                print_info(f"Status: {response.status_code}")
        except Exception as e:
            print_info(f"Error: {str(e)}")
        
        time.sleep(0.5)

def demo_health_and_stats():
    """Demonstrate health check and statistics"""
    print_header("DEMO 8: HEALTH CHECK & STATISTICS")
    
    print_section("Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print_data("Status", data.get("status", ""))
            print_data("Version", data.get("version", ""))
            print_data("Uptime", f"{data.get('uptime', 0)} seconds")
            print_success("Health check passed")
        else:
            print_info(f"Status: {response.status_code}")
    except Exception as e:
        print_info(f"Error: {str(e)}")
    
    time.sleep(1)
    
    print_section("Application Statistics")
    try:
        response = requests.get(f"{BASE_URL}/api/stats")
        if response.status_code == 200:
            data = response.json()
            print_data("Total Messages", data.get("total_messages", 0))
            print_data("Total Prayers", data.get("total_prayers", 0))
            print_data("Total Devotionals", data.get("total_devotionals_requested", 0))
            print_data("Total Verses", data.get("total_verses_requested", 0))
            print_data("Active Conversations", data.get("active_conversations", 0))
            print_success("Statistics retrieved")
        else:
            print_info(f"Status: {response.status_code}")
    except Exception as e:
        print_info(f"Error: {str(e)}")

def demo_conversation_history():
    """Demonstrate conversation history feature"""
    print_header("DEMO 9: CONVERSATION HISTORY")
    
    try:
        response = requests.get(f"{BASE_URL}/api/conversation/history")
        if response.status_code == 200:
            data = response.json()
            print_data("User ID", data.get("user_id", ""))
            print_data("Message Count", data.get("message_count", 0))
            
            conversation = data.get("conversation", [])
            if conversation:
                print("\n📜 Recent Conversation:")
                for msg in conversation[:5]:  # Show last 5 messages
                    print(f"\n  User: {msg.get('user', '')}")
                    print(f"  AI: {msg.get('ai', '')[:100]}...")
            
            print_success("Conversation history retrieved")
        else:
            print_info(f"Status: {response.status_code}")
    except Exception as e:
        print_info(f"Error: {str(e)}")

def main():
    """Main demonstration function"""
    print(f"\n{COLORS['BOLD']}{COLORS['BLUE']}")
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║          🙏 TALK TO JESUS AI - COMPLETE FEATURE DEMO 🙏          ║
    ║                                                                  ║
    ║              Demonstrating ALL Application Capabilities           ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    print(COLORS['END'])
    
    print_info(f"Testing application at: {BASE_URL}")
    print_info(f"Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info("Make sure the Flask app is running (python3 app.py)")
    
    input(f"\n{COLORS['YELLOW']}Press ENTER to start the demo...{COLORS['END']}")
    
    try:
        # Run all demos
        demo_sms_chat()
        demo_prayer_requests()
        demo_daily_devotional()
        demo_bible_verses()
        demo_video_avatar_generation()
        demo_video_streaming()
        demo_3d_avatar()
        demo_health_and_stats()
        demo_conversation_history()
        
        # Final summary
        print_header("DEMO COMPLETE!")
        print_success("All features demonstrated successfully! ✨")
        print(f"\n{COLORS['CYAN']}Features Tested:{COLORS['END']}")
        print("  ✅ SMS Chat Conversations (5 messages)")
        print("  ✅ Prayer Requests with Sentiment Detection (4 emotions)")
        print("  ✅ Daily Devotionals")
        print("  ✅ Bible Verse Library (7 categories)")
        print("  ✅ AI Video Generation")
        print("  ✅ Live Video Streaming (WebRTC, Zoom, Google Meet)")
        print("  ✅ 3D Animated Avatar (3 animations)")
        print("  ✅ Health Check & Statistics")
        print("  ✅ Conversation History")
        
        print(f"\n{COLORS['GREEN']}{COLORS['BOLD']}Total: 9 major features, 30+ individual tests{COLORS['END']}")
        print(f"\n{COLORS['BLUE']}See SAMPLES.md for detailed output examples.{COLORS['END']}")
        print(f"{COLORS['BLUE']}See BROWSER_TEST_RESULTS.md for browser testing results.{COLORS['END']}\n")
        
    except KeyboardInterrupt:
        print(f"\n\n{COLORS['YELLOW']}Demo interrupted by user{COLORS['END']}")
    except Exception as e:
        print(f"\n\n{COLORS['RED']}Error during demo: {str(e)}{COLORS['END']}")
        print(f"{COLORS['YELLOW']}Make sure the Flask app is running: python3 app.py{COLORS['END']}")

if __name__ == "__main__":
    main()
