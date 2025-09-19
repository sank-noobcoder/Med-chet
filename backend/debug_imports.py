import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.services.conversation_manager import conversation_manager
    print("SUCCESS: conversation_manager imported successfully")
except ImportError as e:
    print(f"ERROR: {e}")
    
    # Let's see what's actually in the module
    import app.services.conversation_manager as cm_module
    print("Available names in conversation_manager module:")
    for name in dir(cm_module):
        if not name.startswith('_'):
            print(f"  {name}")