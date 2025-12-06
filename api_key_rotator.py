# Placeholder for api_key_rotator module
# Replace this with your actual implementation

import os

def get_api_key() -> str:
    """
    Get OpenAI API key (with rotation logic if needed).
    
    Returns:
        str: OpenAI API key
    """
    return os.getenv('OPENAI_API_KEY', '')
