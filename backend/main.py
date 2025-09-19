import sys
import os
from app import create_app
from config import Config
from ngrok_setup import start_ngrok, update_twilio_webhook

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = create_app()

if __name__ == "__main__":
    # Start ngrok if enabled
    ngrok_url = None
    if Config.USE_NGROK:
        ngrok_url = start_ngrok()
        if ngrok_url:
            update_twilio_webhook(ngrok_url)
    
    print(f"Starting server on {Config.HOST}:{Config.PORT}")
    if ngrok_url:
        print(f" * Public URL: {ngrok_url}")
    
    app.run(host=Config.HOST, port=Config.PORT, debug=True)