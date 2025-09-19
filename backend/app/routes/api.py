from flask import Blueprint, request, jsonify
import logging

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)

# Import inside function to avoid circular imports
def get_conversation_manager():
    from app.services.conversation_manager import conversation_manager
    return conversation_manager

@api_bp.route('/query', methods=['POST'])
def handle_query():
    """Handle API queries"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Missing query parameter'}), 400
        
        query = data['query']
        user_id = data.get('user_id', 'api_user')
        
        cm = get_conversation_manager()
        response = cm.process_message(user_id, query)
        
        return jsonify({
            'status': 'success',
            'response': response,
            'user_id': user_id
        })
    
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})