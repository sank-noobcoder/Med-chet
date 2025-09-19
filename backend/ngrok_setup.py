import requests
import threading
import time
from pyngrok import ngrok
from config import Config

def start_ngrok():
    """Start ngrok tunnel and return the public URL"""
    try:
        # Set ngrok authtoken if provided
        if Config.NGROK_AUTHTOKEN:
            ngrok.set_auth_token(Config.NGROK_AUTHTOKEN)
        
        # Open a ngrok tunnel to the Flask server
        public_url = ngrok.connect(Config.PORT, bind_tls=True).public_url
        print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:{Config.PORT}\"")
        
        return public_url
    except Exception as e:
        print(f" * ngrok error: {e}")
        return None

def update_twilio_webhook(ngrok_url):
    """Update Twilio webhook URL programmatically"""
    if not all([Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN]):
        print(" * Twilio credentials not found, skipping webhook update")
        return
    
    try:
        webhook_url = f"{ngrok_url}/whatsapp/webhook"
        
        # Update Twilio WhatsApp sandbox settings
        twilio_url = f"https://studio.twilio.com/v2/Flows/FWXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # You'll need to get your flow SID
        
        # Alternatively, use the Twilio API to update webhooks
        # This is a simplified example - you might need to adjust based on your Twilio setup
        print(f" * Twilio webhook should be set to: {webhook_url}")
        print(" * Please update manually in Twilio Console -> WhatsApp -> Sandbox Settings")
        
    except Exception as e:
        print(f" * Error updating Twilio webhook: {e}")