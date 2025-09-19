from flask import Flask, jsonify
from config import Config
import threading
import time
import logging

logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Import blueprints inside function to avoid circular imports
    from app.routes.whatsapp import whatsapp_bp
    from app.routes.api import api_bp
    
    # Register blueprints
    app.register_blueprint(whatsapp_bp, url_prefix='/whatsapp')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Add a simple test route
    @app.route('/')
    def home():
        return jsonify({"status": "ok", "message": "Med-Chat Server is running"})
    
    # Import conversation manager inside function
    def cleanup_sessions():
        from app.services.conversation_manager import conversation_manager
        while True:
            time.sleep(300)
            try:
                conversation_manager.cleanup_expired_sessions()
            except Exception as e:
                logger.error(f"Error in cleanup: {e}")
    
    cleanup_thread = threading.Thread(target=cleanup_sessions, daemon=True)
    cleanup_thread.start()
    
    logger.info("Flask app created successfully!")
    return app