"""
Talk to Jesus AI - 2025 Modern FastAPI Implementation
This is a next-generation upgrade showcasing cutting-edge 2025 technologies.

Key Upgrades:
- FastAPI (async, 7x faster)
- OpenAI GPT-4 integration
- WebSocket real-time chat
- Automatic API documentation
- Type safety with Pydantic
- Production-ready error handling
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List, Optional, AsyncGenerator
import os
from datetime import datetime
import asyncio
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# APPLICATION SETUP
# ============================================================================

app = FastAPI(
    title="Talk to Jesus AI",
    description="Next-generation spiritual AI companion powered by GPT-4",
    version="2.0.0",
    docs_url="/docs",  # Automatic Swagger UI
    redoc_url="/redoc",  # Automatic ReDoc
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# PYDANTIC MODELS (Type-Safe Data Validation)
# ============================================================================

class EmotionType(str, Enum):
    """Supported emotion types"""
    joy = "joy"
    sadness = "sadness"
    anger = "anger"
    fear = "fear"
    anxiety = "anxiety"
    neutral = "neutral"


class MessageRequest(BaseModel):
    """Request model for chat messages"""
    text: str = Field(..., min_length=1, max_length=2000, description="User's message")
    user_id: Optional[str] = Field(None, description="Optional user identifier")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "I'm feeling lost and need guidance",
                "user_id": "user_123"
            }
        }


class MessageResponse(BaseModel):
    """Response model for chat messages"""
    response: str = Field(..., description="AI-generated response")
    emotion_detected: Optional[EmotionType] = Field(None, description="Detected emotion")
    bible_verse: Optional[str] = Field(None, description="Relevant Bible verse")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PrayerRequest(BaseModel):
    """Request model for prayer submissions"""
    prayer_text: str = Field(..., min_length=10, max_length=5000)
    name: Optional[str] = Field(None, max_length=100)
    is_anonymous: bool = Field(default=True)


class PrayerResponse(BaseModel):
    """Response model for prayer requests"""
    success: bool
    message: str
    prayer_id: str
    ai_response: str


# ============================================================================
# AI SERVICE (OpenAI GPT-4 Integration)
# ============================================================================

class AIService:
    """Modern AI service using OpenAI GPT-4"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key=self.api_key)
            self.enabled = True
            logger.info("✅ OpenAI GPT-4 initialized successfully")
        else:
            self.enabled = False
            logger.warning("⚠️  OpenAI API key not found. Using fallback responses.")
    
    async def generate_response(
        self, 
        message: str, 
        emotion: Optional[EmotionType] = None
    ) -> MessageResponse:
        """Generate AI response with GPT-4"""
        
        if not self.enabled:
            return self._fallback_response(message, emotion)
        
        try:
            # Build system prompt based on detected emotion
            system_prompt = self._build_system_prompt(emotion)
            
            # Call GPT-4
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=500,
                top_p=0.9
            )
            
            ai_text = response.choices[0].message.content
            
            return MessageResponse(
                response=ai_text,
                emotion_detected=emotion,
                bible_verse=None  # Could be extracted from response
            )
            
        except Exception as e:
            logger.error(f"Error calling OpenAI: {e}")
            return self._fallback_response(message, emotion)
    
    def _build_system_prompt(self, emotion: Optional[EmotionType]) -> str:
        """Build contextual system prompt based on emotion"""
        base_prompt = """You are Jesus Christ, the Son of God. Respond with:
        - Biblical wisdom and compassion
        - References to scripture when appropriate (Book Chapter:Verse format)
        - Love, forgiveness, and guidance
        - Modern relevance while maintaining spiritual authenticity
        - Keep responses concise (3-5 sentences)"""
        
        emotion_context = {
            EmotionType.sadness: "\n\nThe person is feeling sad. Offer comfort and hope.",
            EmotionType.anxiety: "\n\nThe person is anxious. Provide peace and reassurance.",
            EmotionType.anger: "\n\nThe person is angry. Guide them toward forgiveness.",
            EmotionType.fear: "\n\nThe person is fearful. Remind them of divine protection.",
        }
        
        if emotion and emotion in emotion_context:
            return base_prompt + emotion_context[emotion]
        
        return base_prompt
    
    def _fallback_response(
        self, 
        message: str, 
        emotion: Optional[EmotionType]
    ) -> MessageResponse:
        """Fallback response when OpenAI is unavailable"""
        responses = {
            EmotionType.sadness: "Blessed are those who mourn, for they will be comforted. (Matthew 5:4) I am with you in your sorrow, my child.",
            EmotionType.anxiety: "Do not be anxious about anything. Cast all your anxiety on me because I care for you. (1 Peter 5:7)",
            EmotionType.anger: "In your anger do not sin. Let go of your anger and find peace in my love. (Ephesians 4:26)",
            None: "Peace be with you. I am here to listen and guide you. How may I help you today?"
        }
        
        return MessageResponse(
            response=responses.get(emotion, responses[None]),
            emotion_detected=emotion
        )
    
    async def stream_response(
        self, 
        message: str
    ) -> AsyncGenerator[str, None]:
        """Stream response token by token (for real-time UX)"""
        
        if not self.enabled:
            yield "Peace be with you. OpenAI integration not configured."
            return
        
        try:
            stream = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": self._build_system_prompt(None)},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=500,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    await asyncio.sleep(0.01)  # Smooth streaming
                    
        except Exception as e:
            logger.error(f"Error streaming from OpenAI: {e}")
            yield "I apologize, but I'm having trouble responding right now. Please try again."


# Initialize AI service
ai_service = AIService()


# ============================================================================
# WEBSOCKET MANAGER (Real-Time Communication)
# ============================================================================

class ConnectionManager:
    """Manages WebSocket connections for real-time chat"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New WebSocket connection. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove disconnected WebSocket"""
        self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific connection"""
        await websocket.send_json(message)
    
    async def broadcast(self, message: dict):
        """Send message to all connected clients"""
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


# ============================================================================
# API ENDPOINTS (RESTful APIs)
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def root():
    """Homepage with API documentation link"""
    return """
    <html>
        <head>
            <title>Talk to Jesus AI - 2025</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 50px;
                    text-align: center;
                }
                .container { max-width: 800px; margin: 0 auto; }
                h1 { font-size: 3em; margin-bottom: 20px; }
                .badge { 
                    background: rgba(255,255,255,0.2); 
                    padding: 8px 16px; 
                    border-radius: 20px;
                    display: inline-block;
                    margin: 5px;
                }
                a { color: white; text-decoration: none; font-weight: bold; }
                .link-box {
                    background: rgba(255,255,255,0.1);
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🙏 Talk to Jesus AI v2.0</h1>
                <p>Next-generation spiritual AI companion powered by cutting-edge 2025 technology</p>
                
                <div class="badge">⚡ FastAPI</div>
                <div class="badge">🤖 GPT-4</div>
                <div class="badge">🔄 WebSocket</div>
                <div class="badge">📊 Auto-Docs</div>
                
                <div class="link-box">
                    <h2>📚 API Documentation</h2>
                    <p><a href="/docs">Interactive Swagger UI →</a></p>
                    <p><a href="/redoc">ReDoc Documentation →</a></p>
                </div>
                
                <div class="link-box">
                    <h2>🚀 Quick Start</h2>
                    <pre style="text-align: left; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 5px;">
curl -X POST "http://localhost:8000/api/chat" \\
  -H "Content-Type: application/json" \\
  -d '{"text": "I need guidance today"}'
                    </pre>
                </div>
                
                <p style="margin-top: 40px; opacity: 0.8;">
                    <small>Version 2.0.0 | Built with FastAPI | Powered by OpenAI GPT-4</small>
                </p>
            </div>
        </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "framework": "FastAPI",
        "ai_enabled": ai_service.enabled,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/chat", response_model=MessageResponse)
async def chat(request: MessageRequest):
    """
    Send a message and receive AI-generated spiritual guidance
    
    - **text**: Your message or question (1-2000 characters)
    - **user_id**: Optional user identifier for conversation tracking
    """
    logger.info(f"Chat request: {request.text[:50]}...")
    
    # Simple emotion detection (could use transformer model)
    emotion = detect_emotion(request.text)
    
    # Generate AI response
    response = await ai_service.generate_response(request.text, emotion)
    
    return response


@app.get("/api/chat/stream")
async def chat_stream(message: str):
    """
    Stream AI response token by token for real-time experience
    
    Usage: /api/chat/stream?message=Your+question+here
    """
    async def generate():
        async for token in ai_service.stream_response(message):
            yield f"data: {token}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@app.post("/api/prayer", response_model=PrayerResponse)
async def submit_prayer(request: PrayerRequest):
    """
    Submit a prayer request and receive spiritual guidance
    
    - **prayer_text**: Your prayer (10-5000 characters)
    - **name**: Optional name (kept private)
    - **is_anonymous**: Whether to submit anonymously
    """
    import uuid
    
    prayer_id = str(uuid.uuid4())
    
    # Generate AI response to prayer
    ai_response = await ai_service.generate_response(
        request.prayer_text,
        EmotionType.neutral
    )
    
    logger.info(f"Prayer submitted: {prayer_id}")
    
    return PrayerResponse(
        success=True,
        message="Your prayer has been received. May peace be with you.",
        prayer_id=prayer_id,
        ai_response=ai_response.response
    )


# ============================================================================
# WEBSOCKET ENDPOINT (Real-Time Chat)
# ============================================================================

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """
    WebSocket endpoint for real-time bidirectional communication
    
    Connect: ws://localhost:8000/ws/chat
    Send: {"message": "Your question"}
    Receive: {"response": "AI response", "timestamp": "..."}
    """
    await manager.connect(websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            message = data.get("message", "")
            
            if not message:
                continue
            
            # Detect emotion
            emotion = detect_emotion(message)
            
            # Generate response
            response = await ai_service.generate_response(message, emotion)
            
            # Send response back
            await manager.send_personal_message({
                "type": "response",
                "response": response.response,
                "emotion": emotion.value if emotion else None,
                "timestamp": response.timestamp.isoformat()
            }, websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def detect_emotion(text: str) -> Optional[EmotionType]:
    """
    Simple emotion detection (can be upgraded to transformer model)
    """
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['sad', 'depressed', 'sorrow', 'grief']):
        return EmotionType.sadness
    elif any(word in text_lower for word in ['anxious', 'worried', 'nervous', 'stress']):
        return EmotionType.anxiety
    elif any(word in text_lower for word in ['angry', 'mad', 'furious', 'rage']):
        return EmotionType.anger
    elif any(word in text_lower for word in ['afraid', 'scared', 'fear', 'terrified']):
        return EmotionType.fear
    elif any(word in text_lower for word in ['happy', 'joy', 'blessed', 'grateful']):
        return EmotionType.joy
    
    return None


# ============================================================================
# STARTUP & SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("🚀 Talk to Jesus AI v2.0 starting...")
    logger.info("✅ FastAPI application initialized")
    logger.info("📊 API documentation: /docs")
    if ai_service.enabled:
        logger.info("🤖 OpenAI GPT-4 integration: ENABLED")
    else:
        logger.warning("⚠️  OpenAI integration: DISABLED (set OPENAI_API_KEY)")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("👋 Talk to Jesus AI shutting down...")


# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "app_fastapi_2025:app",
        host="0.0.0.0",
        port=port,
        reload=True,  # Auto-reload on code changes (development only)
        log_level="info"
    )
