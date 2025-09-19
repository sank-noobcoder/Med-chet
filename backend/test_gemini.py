import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key: {api_key}")

if not api_key or api_key == 'your_gemini_api_key_here':
    print("ERROR: API key is missing or not configured!")
else:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hello, how are you?")
        print("SUCCESS: API key is valid!")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")