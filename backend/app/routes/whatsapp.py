from flask import Blueprint, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import logging

logger = logging.getLogger(__name__)

whatsapp_bp = Blueprint('whatsapp', __name__)

# Import conversation_manager inside the function to avoid circular imports
def get_conversation_manager():
    from app.services.conversation_manager import conversation_manager
    return conversation_manager

@whatsapp_bp.route('/webhook', methods=['POST', 'GET'])
def whatsapp_webhook():
    """Handle incoming WhatsApp messages via Twilio webhook"""
    try:
        # For GET requests (Twilio verification)
        if request.method == 'GET':
            return "Webhook is working!"
        
        # Get the incoming message from the request
        incoming_msg = request.values.get('Body', '').strip()
        sender = request.values.get('From', '')
        
        print(f"Received message from {sender}: {incoming_msg}")
        
        # Initialize Twilio response
        resp = MessagingResponse()
        msg = resp.message()
        
        # Get conversation manager
        cm = get_conversation_manager()
        
        # Process message using conversation manager
        response_text = cm.process_message(sender, incoming_msg)
        
        # Send the response
        msg.body(response_text)
        
        return Response(str(resp), mimetype="text/xml")
    
    except Exception as e:
        logger.error(f"Error processing WhatsApp message: {e}")
        resp = MessagingResponse()
        msg = resp.message()
        msg.body("Sorry, I encountered an error. Please try again.")
        return Response(str(resp), mimetype="text/xml")

@whatsapp_bp.route('/test')
def test_whatsapp():
    return {"status": "whatsapp route working"}