from typing import Dict, Optional
import time
import logging

# Import the UserSession model first
from app.models.user_session import UserSession

logger = logging.getLogger(__name__)

# Initialize gemini_service as None - we'll import it later
gemini_service = None

class ConversationManager:
    def __init__(self):
        self.sessions: Dict[str, UserSession] = {}
        self.session_timeout = 30  # minutes
        
    def get_session(self, phone_number: str) -> UserSession:
        """Get or create user session"""
        if phone_number not in self.sessions or self.sessions[phone_number].is_expired(self.session_timeout):
            self.sessions[phone_number] = UserSession(phone_number)
        else:
            self.sessions[phone_number].update_activity()
        return self.sessions[phone_number]
    
    def _get_gemini_service(self):
        """Lazy import of gemini_service to avoid circular imports"""
        global gemini_service
        if gemini_service is None:
            try:
                from app.services.gemini_service import gemini_service as gs
                gemini_service = gs
            except ImportError as e:
                logger.error(f"Failed to import gemini_service: {e}")
                return None
        return gemini_service
    
    def process_message(self, phone_number: str, message: str) -> str:
        """Process incoming message and return response"""
        session = self.get_session(phone_number)
        
        # Medical chatbot context
        medical_context = """You are an AI medical assistant. Your role is to:
        1. Greet patients professionally
        2. Collect symptoms and medical history systematically
        3. Ask relevant follow-up questions
        4. Provide general medical guidance (not diagnosis)
        5. Recommend seeking professional help when appropriate
        6. Maintain empathy and professionalism
        
        Important: Always remind users that you are an AI assistant and not a substitute for professional medical advice."""
        
        # Get gemini service (lazy load)
        gemini = self._get_gemini_service()
        if gemini is None:
            return "I'm currently experiencing technical difficulties. Please try again later."
        
        try:
            # Generate response using Gemini
            response = gemini.generate_response(
                prompt=message,
                context=medical_context + "\n\n" + session.conversation_context
            )
            
            # Update conversation context
            session.conversation_context += f"\nUser: {message}\nAssistant: {response}"
            
            # Keep context manageable (last 10 exchanges)
            lines = session.conversation_context.split('\n')
            if len(lines) > 20:  # Keep last 10 exchanges
                session.conversation_context = '\n'.join(lines[-20:])
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again in a few moments."
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        current_time = time.time()
        expired_numbers = [
            number for number, session in self.sessions.items()
            if session.is_expired(self.session_timeout)
        ]
        for number in expired_numbers:
            del self.sessions[number]

# Create the singleton instance
conversation_manager = ConversationManager()