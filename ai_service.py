"""AI service for generating Jesus persona responses."""
import os
from typing import Optional
import requests
from logger import setup_logger

logger = setup_logger(__name__)


class AIService:
    """Service for generating AI responses."""
    
    SYSTEM_PROMPT = """You are Jesus Christ, speaking with compassion, wisdom, and love. 
Respond to questions and conversations in a way that reflects the teachings found in the Bible.
Be kind, understanding, and provide guidance based on Christian values and principles.
Keep responses concise and meaningful."""
    
    def __init__(self):
        """Initialize AI service with configured provider."""
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.openai_model = os.getenv('OPENAI_MODEL', 'gpt-4')
        self.anthropic_model = os.getenv('ANTHROPIC_MODEL', 'claude-3-sonnet-20240229')
        
        # Determine which provider to use
        self.provider = None
        if self.openai_api_key:
            self.provider = 'openai'
            logger.info("Using OpenAI as AI provider")
        elif self.anthropic_api_key:
            self.provider = 'anthropic'
            logger.info("Using Anthropic as AI provider")
        else:
            logger.warning("No AI provider configured, using fallback responses")
    
    def generate_response(self, user_message: str, max_tokens: int = 150) -> str:
        """
        Generate AI response to user message.
        
        Args:
            user_message: The user's input message
            max_tokens: Maximum tokens in response
            
        Returns:
            AI-generated response string
        """
        if not user_message or not user_message.strip():
            return "Peace be with you. How may I help you today?"
        
        try:
            if self.provider == 'openai':
                return self._generate_openai_response(user_message, max_tokens)
            elif self.provider == 'anthropic':
                return self._generate_anthropic_response(user_message, max_tokens)
            else:
                return self._generate_fallback_response(user_message)
        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}", exc_info=True)
            return "I am here with you. Please try again, my child."
    
    def _generate_openai_response(self, user_message: str, max_tokens: int) -> str:
        """Generate response using OpenAI API."""
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.openai_model,
            "messages": [
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    
    def _generate_anthropic_response(self, user_message: str, max_tokens: int) -> str:
        """Generate response using Anthropic Claude API."""
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.anthropic_api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        data = {
            "model": self.anthropic_model,
            "max_tokens": max_tokens,
            "system": self.SYSTEM_PROMPT,
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['content'][0]['text'].strip()
    
    def _generate_fallback_response(self, user_message: str) -> str:
        """Generate fallback response when no AI provider is configured."""
        # Simple keyword-based responses
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ['help', 'lost', 'afraid', 'scared']):
            return "Do not be afraid, for I am with you. Trust in the Lord with all your heart."
        elif any(word in message_lower for word in ['love', 'loved']):
            return "Love one another as I have loved you. This is my commandment."
        elif any(word in message_lower for word in ['forgive', 'forgiveness', 'sin']):
            return "Your sins are forgiven. Go and sin no more. I came to save, not to condemn."
        elif any(word in message_lower for word in ['pray', 'prayer']):
            return "When you pray, go into your room and pray to your Father in secret. Ask and it will be given to you."
        elif any(word in message_lower for word in ['thank', 'grateful', 'blessing']):
            return "Give thanks to the Lord, for He is good. His love endures forever."
        elif '?' in user_message:
            return "Seek and you shall find. Ask, and it will be given to you. I am here to guide you."
        else:
            return "Peace be with you, my child. How may I help you today?"


# Global instance
ai_service = AIService()
