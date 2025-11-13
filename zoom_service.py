"""Zoom meeting service integration."""
import os
import base64
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional
from logger import setup_logger

logger = setup_logger(__name__)


class ZoomService:
    """Service for creating and managing Zoom meetings."""
    
    def __init__(self):
        """Initialize Zoom service."""
        self.client_id = os.getenv('ZOOM_CLIENT_ID')
        self.client_secret = os.getenv('ZOOM_CLIENT_SECRET')
        self.account_id = os.getenv('ZOOM_ACCOUNT_ID')
        self._access_token = None
        self._token_expires_at = None
    
    def is_configured(self) -> bool:
        """Check if Zoom service is properly configured."""
        return bool(self.client_id and self.client_secret and self.account_id)
    
    def _get_access_token(self) -> str:
        """Get or refresh OAuth access token."""
        # Check if token is still valid
        if self._access_token and self._token_expires_at:
            if datetime.now() < self._token_expires_at:
                return self._access_token
        
        # Get new token
        url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={self.account_id}"
        
        # Create basic auth header
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        response = requests.post(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        self._access_token = data['access_token']
        # Set expiration with 5 minute buffer
        expires_in = data.get('expires_in', 3600)
        self._token_expires_at = datetime.now() + timedelta(seconds=expires_in - 300)
        
        logger.info("Successfully obtained Zoom access token")
        return self._access_token
    
    def create_meeting(
        self,
        topic: str = "Talk to Jesus Meeting",
        duration: int = 30,
        start_time: Optional[datetime] = None,
        timezone: str = "UTC"
    ) -> Dict:
        """
        Create a Zoom meeting.
        
        Args:
            topic: Meeting topic/title
            duration: Meeting duration in minutes
            start_time: Meeting start time (defaults to now)
            timezone: Meeting timezone
            
        Returns:
            Dictionary with meeting details including join URL
            
        Raises:
            ValueError: If service is not configured
            requests.HTTPError: If API request fails
        """
        if not self.is_configured():
            raise ValueError("Zoom service is not configured. Please set ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET, and ZOOM_ACCOUNT_ID")
        
        access_token = self._get_access_token()
        
        # Format start time
        if start_time is None:
            start_time = datetime.now()
        start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
        
        # Create meeting
        url = "https://api.zoom.us/v2/users/me/meetings"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "topic": topic,
            "type": 2,  # Scheduled meeting
            "start_time": start_time_str,
            "duration": duration,
            "timezone": timezone,
            "settings": {
                "host_video": True,
                "participant_video": True,
                "join_before_host": True,
                "mute_upon_entry": False,
                "watermark": False,
                "audio": "both",
                "auto_recording": "none"
            }
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        
        meeting_data = response.json()
        logger.info(f"Created Zoom meeting: {meeting_data.get('id')}")
        
        return {
            "id": meeting_data.get("id"),
            "topic": meeting_data.get("topic"),
            "join_url": meeting_data.get("join_url"),
            "start_url": meeting_data.get("start_url"),
            "start_time": meeting_data.get("start_time"),
            "duration": meeting_data.get("duration"),
            "password": meeting_data.get("password")
        }


# Global instance
zoom_service = ZoomService()
