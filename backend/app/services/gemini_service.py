import google.generativeai as genai
import os
from config import Config
from typing import Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        # Debug: Check if API key is available
        if not Config.GEMINI_API_KEY or Config.GEMINI_API_KEY == 'your_gemini_api_key_here':
            logger.error("Gemini API key is missing or invalid!")
            raise ValueError("Gemini API key is required")
        
        try:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("Gemini service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {e}")
            raise
    
    def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """Generate response using Gemini API"""
        try:
            if context:
                full_prompt = f"{context}\n\nUser: {prompt}\nAssistant:"
            else:
                full_prompt = prompt
            
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            error_msg = f"Gemini API error: {str(e)}"
            logger.error(error_msg)
            return "I'm having trouble connecting to my knowledge base. Please try again later."

# Singleton instance with error handling
try:
    gemini_service = GeminiService()
except Exception as e:
    logger.error(f"Failed to create Gemini service: {e}")
    gemini_service = None