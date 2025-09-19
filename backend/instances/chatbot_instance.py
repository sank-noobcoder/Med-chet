from chatbot import setup_auth, Inference
from config import Config

# Initialize the chatbot instance
setup_auth("Gemini Integration")
chatbot_instance = Inference()

def get_chatbot_response(query: str) -> str:
    """Get response from the original chatbot if needed"""
    try:
        # This would need to be async or run in a thread
        return "Please use the Gemini API for responses."
    except Exception as e:
        return f"Error: {str(e)}"