#!/usr/bin/env python3
"""
Simple test script for the Talk to Jesus AI API
Usage: python test_api.py
"""
import requests
import sys

BASE_URL = "http://localhost:5000"

def test_health():
    """Test the health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_home():
    """Test the home endpoint"""
    print("\nTesting / endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_sms():
    """Test the SMS endpoint"""
    print("\nTesting /sms endpoint...")
    data = {"Body": "Hello, I need guidance"}
    response = requests.post(f"{BASE_URL}/sms", data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:200]}...")
    return response.status_code == 200

def test_voice():
    """Test the voice endpoint"""
    print("\nTesting /voice endpoint...")
    data = {"SpeechResult": "Can you help me?"}
    response = requests.post(f"{BASE_URL}/voice", data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:200]}...")
    return response.status_code == 200

def main():
    """Run all tests"""
    print("=" * 60)
    print("Talk to Jesus AI - API Tests")
    print("=" * 60)
    print(f"Testing API at: {BASE_URL}\n")
    
    tests = [
        ("Health Check", test_health),
        ("Home Endpoint", test_home),
        ("SMS Endpoint", test_sms),
        ("Voice Endpoint", test_voice)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"ERROR: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(f"\nERROR: Could not connect to {BASE_URL}")
        print("Make sure the Flask application is running:")
        print("  python app.py")
        sys.exit(1)
