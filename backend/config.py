import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask settings
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000
    
    # CORS settings
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:8080']
    
    # ML Model paths (for ML teammate integration)
    ASR_MODEL_PATH = os.path.join('..', 'ml', 'models', 'asr_model')
    TRANSLATION_MODEL_PATH = os.path.join('..', 'ml', 'models', 'translation_model')
    
    # Supported languages
    SUPPORTED_INPUT_LANGUAGES = ['garhwali', 'kumaoni']
    SUPPORTED_OUTPUT_LANGUAGES = ['hindi', 'english']
    
    # File upload settings
    MAX_AUDIO_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_AUDIO_FORMATS = ['wav', 'mp3', 'ogg']