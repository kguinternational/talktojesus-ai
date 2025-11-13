"""Tests for AI service."""
import pytest
from ai_service import AIService


def test_ai_service_initialization():
    """Test AI service initializes correctly."""
    service = AIService()
    assert service is not None
    assert service.SYSTEM_PROMPT is not None


def test_generate_response_empty_message():
    """Test AI service handles empty messages."""
    service = AIService()
    response = service.generate_response('')
    assert response is not None
    assert len(response) > 0
    assert 'Peace' in response or 'peace' in response


def test_generate_response_with_message():
    """Test AI service generates response for valid message."""
    service = AIService()
    response = service.generate_response('help me')
    assert response is not None
    assert len(response) > 0


def test_fallback_response_help():
    """Test fallback responses for help keywords."""
    service = AIService()
    response = service._generate_fallback_response('I need help')
    assert 'afraid' in response.lower() or 'with you' in response.lower()


def test_fallback_response_love():
    """Test fallback responses for love keywords."""
    service = AIService()
    response = service._generate_fallback_response('Tell me about love')
    assert 'love' in response.lower()


def test_fallback_response_forgiveness():
    """Test fallback responses for forgiveness keywords."""
    service = AIService()
    response = service._generate_fallback_response('I need forgiveness')
    assert 'forgive' in response.lower() or 'sin' in response.lower()


def test_fallback_response_prayer():
    """Test fallback responses for prayer keywords."""
    service = AIService()
    response = service._generate_fallback_response('How do I pray?')
    assert 'pray' in response.lower()


def test_fallback_response_generic():
    """Test fallback responses for generic messages."""
    service = AIService()
    response = service._generate_fallback_response('Hello there')
    assert response is not None
    assert len(response) > 0
