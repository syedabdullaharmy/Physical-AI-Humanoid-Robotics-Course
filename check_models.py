
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Try to load .env from typical locations
load_dotenv()
# Also try parent dir just in case
load_dotenv(dotenv_path="../.env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # also try to read from backend/.env directly if running from root
    load_dotenv(dotenv_path="backend/.env")
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("NO API KEY FOUND")
else:
    genai.configure(api_key=api_key)
    print("Listing available models with generateContent support:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model: {m.name}")
