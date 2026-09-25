import os
from dotenv import load_dotenv

load_dotenv()

EXPERIENTIAL_API_KEY = os.getenv('EXPERIENTIAL_API_KEY', '').strip()
EXPERIENTIAL_BASE_URL = os.getenv('EXPERIENTIAL_BASE_URL', '').strip()
MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-5.6-luna').strip()
BACKEND_HOST = os.getenv('BACKEND_HOST', '0.0.0.0').strip()
BACKEND_PORT = int(os.getenv('BACKEND_PORT', '8000'))
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000').strip()

def require_api_key() -> str:
    if not EXPERIENTIAL_API_KEY or EXPERIENTIAL_API_KEY == 'your_experientiallabs_key_here':
        raise RuntimeError(
            'EXPERIENTIAL_API_KEY is missing. Add it to your .env file.'
        )
    return EXPERIENTIAL_API_KEY