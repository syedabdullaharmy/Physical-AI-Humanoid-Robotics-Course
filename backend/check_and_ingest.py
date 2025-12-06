"""
Auto-check Gemini API quota and run ingestion when available
This script will test if the API quota has reset and automatically run ingestion
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
import subprocess
import sys

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def check_quota():
    """Test if we can make an embedding request"""
    print("Checking Gemini API quota status...")
    
    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY not set in .env file")
        return False
    
    genai.configure(api_key=GEMINI_API_KEY)
    
    try:
        # Try a simple embedding request
        result = genai.embed_content(
            model="models/text-embedding-004",
            content="test",
            task_type="retrieval_query"
        )
        print("SUCCESS: API quota is available!")
        return True
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            print("QUOTA EXCEEDED: API quota limit still reached")
            print("Please wait for the quota to reset (resets daily)")
            print("Check your usage at: https://ai.dev/usage?tab=rate-limit")
        else:
            print(f"ERROR: {error_msg}")
        return False

def run_ingestion():
    """Run the quick ingestion script"""
    print("\nRunning quick ingestion...")
    print("This will populate the database with 5 sample documents")
    print("Expected time: ~30 seconds\n")
    
    try:
        result = subprocess.run(
            [sys.executable, "quick_ingest.py"],
            cwd=os.path.dirname(__file__),
            capture_output=True,
            text=True
        )
        
        # Print output (avoiding unicode issues)
        if result.stdout:
            print(result.stdout.encode('ascii', 'ignore').decode('ascii'))
        if result.stderr:
            print("Errors:", result.stderr.encode('ascii', 'ignore').decode('ascii'))
        
        if result.returncode == 0:
            print("\nSUCCESS: Ingestion completed!")
            print("\nYour chatbot is now ready to use!")
            print("Try asking questions like:")
            print("  - What is ROS 2?")
            print("  - How do nodes communicate?")
            print("  - What are VLA models?")
            return True
        else:
            print("\nERROR: Ingestion failed")
            return False
            
    except Exception as e:
        print(f"ERROR running ingestion: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Gemini API Quota Checker & Auto-Ingestion")
    print("=" * 60)
    print()
    
    if check_quota():
        print("\nQuota is available! Starting ingestion...")
        run_ingestion()
    else:
        print("\nCannot proceed with ingestion due to quota limits.")
        print("\nOptions:")
        print("1. Wait for quota reset (resets daily)")
        print("2. Upgrade your Gemini API plan")
        print("3. Use a different API key")
        print("\nRun this script again later to check if quota has reset.")
