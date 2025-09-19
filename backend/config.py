import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Twilio Configuration
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')
    
    # Gemini Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    PORT = int(os.getenv('PORT', 8080))
    HOST = os.getenv('HOST', '0.0.0.0')
    
    # ngrok Configuration
    USE_NGROK = os.getenv('USE_NGROK', 'False').lower() == 'true'
    NGROK_AUTHTOKEN = os.getenv('NGROK_AUTHTOKEN', '')
    
    # Path Configuration
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    COOKIE_DIR = os.path.join(BASE_DIR, 'usercookies')
    EMAIL = "uwuwuwu@proxiedmail.com"