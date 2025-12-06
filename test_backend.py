import requests
import json

print("Testing chatbot connection...")
print("=" * 60)

# Test 1: Health check
print("\n1. Testing health endpoint...")
try:
    response = requests.get("http://localhost:8000/health", timeout=5)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print("   [OK] Health check passed!")
except Exception as e:
    print(f"   [ERROR] Health check failed: {e}")
    exit(1)

# Test 2: Chat endpoint
print("\n2. Testing chat endpoint...")
try:
    data = {
        "message": "What is ROS 2?",
        "context": ""
    }
    response = requests.post(
        "http://localhost:8000/chat",
        json=data,
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        resp_text = result.get('response', '')
        print(f"   Response length: {len(resp_text)} characters")
        print(f"   Response preview: {resp_text[:150]}...")
        print("   [OK] Chat endpoint working!")
    else:
        print(f"   [ERROR] Status {response.status_code}")
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"   [ERROR] Chat request failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Test complete!")
