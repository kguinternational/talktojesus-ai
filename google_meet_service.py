"""Google Meet service integration."""
import os
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional
from logger import setup_logger

logger = setup_logger(__name__)


class GoogleMeetService:
    """Service for creating Google Meet meetings via Google Calendar API."""
    
    def __init__(self):
        """Initialize Google Meet service."""
        self.client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        self.redirect_uri = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:5000/oauth2callback')
        self.calendar_id = os.getenv('GOOGLE_CALENDAR_ID', 'primary')
        self._access_token = None
        self._refresh_token = None
    
    def is_configured(self) -> bool:
        """Check if Google Meet service is properly configured."""
        return bool(self.client_id and self.client_secret)
    
    def get_oauth_url(self) -> str:
        """
        Get OAuth authorization URL for user to grant access.
        
        Returns:
            OAuth authorization URL
        """
        scopes = [
            'https://www.googleapis.com/auth/calendar.events',
            'https://www.googleapis.com/auth/calendar'
        ]
        scope_str = ' '.join(scopes)
        
        auth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={self.client_id}&"
            f"redirect_uri={self.redirect_uri}&"
            f"response_type=code&"
            f"scope={scope_str}&"
            f"access_type=offline&"
            f"prompt=consent"
        )
        
        return auth_url
    
    def exchange_code_for_token(self, code: str) -> Dict:
        """
        Exchange authorization code for access and refresh tokens.
        
        Args:
            code: Authorization code from OAuth callback
            
        Returns:
            Dictionary with token information
        """
        url = "https://oauth2.googleapis.com/token"
        data = {
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code'
        }
        
        response = requests.post(url, data=data, timeout=30)
        response.raise_for_status()
        
        token_data = response.json()
        self._access_token = token_data.get('access_token')
        self._refresh_token = token_data.get('refresh_token')
        
        logger.info("Successfully exchanged code for Google OAuth tokens")
        return token_data
    
    def set_access_token(self, access_token: str):
        """Set access token manually (e.g., from session storage)."""
        self._access_token = access_token
    
    def create_meeting(
        self,
        summary: str = "Talk to Jesus Meeting",
        duration: int = 30,
        start_time: Optional[datetime] = None,
        timezone: str = "UTC",
        description: str = ""
    ) -> Dict:
        """
        Create a Google Meet meeting by creating a Calendar event.
        
        Args:
            summary: Meeting title/summary
            duration: Meeting duration in minutes
            start_time: Meeting start time (defaults to now)
            timezone: Meeting timezone
            description: Meeting description
            
        Returns:
            Dictionary with meeting details including Meet link
            
        Raises:
            ValueError: If service is not configured or no access token
            requests.HTTPError: If API request fails
        """
        if not self.is_configured():
            raise ValueError("Google Meet service is not configured. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET")
        
        if not self._access_token:
            raise ValueError("No access token available. User must authenticate first.")
        
        # Calculate start and end times
        if start_time is None:
            start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration)
        
        # Format times for Google Calendar API
        start_time_str = start_time.isoformat()
        end_time_str = end_time.isoformat()
        
        # Create calendar event with Google Meet
        url = f"https://www.googleapis.com/calendar/v3/calendars/{self.calendar_id}/events"
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "summary": summary,
            "description": description or "A spiritual conversation with Jesus through AI",
            "start": {
                "dateTime": start_time_str,
                "timeZone": timezone
            },
            "end": {
                "dateTime": end_time_str,
                "timeZone": timezone
            },
            "conferenceData": {
                "createRequest": {
                    "requestId": f"meet-{int(datetime.now().timestamp())}",
                    "conferenceSolutionKey": {
                        "type": "hangoutsMeet"
                    }
                }
            },
            "attendees": [],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "popup", "minutes": 10}
                ]
            }
        }
        
        # Need to use conferenceDataVersion=1 to create Meet
        params = {"conferenceDataVersion": 1}
        
        response = requests.post(url, json=data, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        event_data = response.json()
        logger.info(f"Created Google Meet meeting: {event_data.get('id')}")
        
        # Extract Meet link
        meet_link = None
        if 'conferenceData' in event_data:
            entry_points = event_data['conferenceData'].get('entryPoints', [])
            for entry in entry_points:
                if entry.get('entryPointType') == 'video':
                    meet_link = entry.get('uri')
                    break
        
        return {
            "id": event_data.get("id"),
            "summary": event_data.get("summary"),
            "meet_link": meet_link,
            "html_link": event_data.get("htmlLink"),
            "start_time": event_data.get("start", {}).get("dateTime"),
            "end_time": event_data.get("end", {}).get("dateTime"),
            "status": event_data.get("status")
        }


# Global instance
google_meet_service = GoogleMeetService()
