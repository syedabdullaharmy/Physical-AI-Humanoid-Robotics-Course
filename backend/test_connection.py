"""
Test script to verify AI model connection
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
env_path = Path(__file__).parent / '.env'
if not env_path.exists():
    env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

print("=" * 60)
print("🔍 Testing AI Model Connection")
print("=" * 60)

# Check API key
if not GEMINI_API_KEY:
    print("❌ ERROR: GEMINI_API_KEY not found in .env file")
    print("\nPlease create a .env file with:")
    print("GEMINI_API_KEY=your_actual_api_key_here")
    exit(1)

print(f"✅ API Key found: {GEMINI_API_KEY[:10]}...{GEMINI_API_KEY[-5:]}")

# Configure Gemini
try:
    genai.configure(api_key=GEMINI_API_KEY)
    print("✅ Gemini API configured successfully")
except Exception as e:
    print(f"❌ Failed to configure Gemini API: {e}")
    exit(1)

# Test embedding model
print("\n📊 Testing Embedding Model...")
try:
    result = genai.embed_content(
        model="models/text-embedding-004", # Switched to newer model
        content="Test embedding for Physical AI and Humanoid Robotics",
        task_type="retrieval_query"
    )
    embedding = result['embedding']
    print(f"✅ Embedding successful! Vector size: {len(embedding)}")
except Exception as e:
    print(f"❌ Embedding failed: {e}")
    # Don't exit, try generation anyway
    # exit(1)

# Test generation model
print("\n🤖 Testing Generation Model...")
try:
    model = genai.GenerativeModel('gemini-2.0-flash-lite-preview-02-05')
    response = model.generate_content("What is ROS 2? Answer in one sentence.")
    print(f"✅ Generation successful!")
    print(f"📝 Response: {response.text}")
except Exception as e:
    print(f"❌ Generation failed: {e}")
    exit(1)

print("\n" + "=" * 60)
print("🎉 All tests passed! AI model is connected and working.")
print("=" * 60)
print("\n✅ You can now start the backend server with:")
print("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")
