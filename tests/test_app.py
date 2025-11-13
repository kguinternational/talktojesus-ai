"""Tests for main application routes."""
import json
import pytest


def test_index_route(client):
    """Test the index route returns API information."""
    response = client.get('/')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['service'] == 'Talk to Jesus AI'
    assert 'endpoints' in data


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data
    assert 'services' in data


def test_sms_endpoint_post_required(client):
    """Test SMS endpoint requires POST method."""
    response = client.get('/sms')
    assert response.status_code == 405  # Method not allowed


def test_sms_endpoint_with_message(client):
    """Test SMS endpoint processes messages."""
    response = client.post('/sms', data={'Body': 'Hello'})
    assert response.status_code == 200
    assert b'<?xml' in response.data  # TwiML response


def test_voice_endpoint_post_required(client):
    """Test voice endpoint requires POST method."""
    response = client.get('/voice')
    assert response.status_code == 405  # Method not allowed


def test_voice_endpoint_initial_call(client):
    """Test voice endpoint handles initial call."""
    response = client.post('/voice', data={})
    assert response.status_code == 200
    assert b'<?xml' in response.data
    assert b'Peace be with you' in response.data


def test_voice_endpoint_with_speech(client):
    """Test voice endpoint processes speech input."""
    response = client.post('/voice', data={'SpeechResult': 'Help me'})
    assert response.status_code == 200
    assert b'<?xml' in response.data


def test_create_zoom_meeting_requires_post(client):
    """Test Zoom meeting endpoint requires POST."""
    response = client.get('/create_zoom_meeting')
    assert response.status_code == 405


def test_create_zoom_meeting_not_configured(client):
    """Test Zoom meeting returns error when not configured."""
    response = client.post('/create_zoom_meeting', 
                          json={'topic': 'Test Meeting'},
                          content_type='application/json')
    assert response.status_code == 503
    
    data = json.loads(response.data)
    assert 'error' in data


def test_create_google_meet_requires_post(client):
    """Test Google Meet endpoint requires POST."""
    response = client.get('/create_google_meet')
    assert response.status_code == 405


def test_create_google_meet_not_authenticated(client):
    """Test Google Meet returns error when not authenticated."""
    response = client.post('/create_google_meet',
                          json={'summary': 'Test Meeting'},
                          content_type='application/json')
    # Should return 401 or 503 depending on configuration
    assert response.status_code in [401, 503]


def test_google_auth_redirect(client):
    """Test Google auth redirects or returns error."""
    response = client.get('/google_auth')
    # Will be 302 if configured, 503 if not
    assert response.status_code in [302, 503]


def test_404_handler(client):
    """Test 404 error handler."""
    response = client.get('/nonexistent-endpoint')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert 'error' in data


def test_empty_sms_message(client):
    """Test SMS endpoint handles empty messages."""
    response = client.post('/sms', data={'Body': ''})
    assert response.status_code == 200
    assert b'<?xml' in response.data


def test_long_sms_message(client):
    """Test SMS endpoint handles long messages."""
    long_message = 'A' * 2000
    response = client.post('/sms', data={'Body': long_message})
    assert response.status_code == 200
    assert b'<?xml' in response.data
