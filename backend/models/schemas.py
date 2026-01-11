from typing import Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TranslationRequest:
    """Schema for translation request"""
    text: str
    input_language: str
    output_language: str
    
    def validate(self):
        """Validate request data"""
        if not self.text or not self.text.strip():
            raise ValueError("Text cannot be empty")
        
        if self.input_language not in ['garhwali', 'kumaoni']:
            raise ValueError(f"Unsupported input language: {self.input_language}")
        
        if self.output_language not in ['hindi', 'english']:
            raise ValueError(f"Unsupported output language: {self.output_language}")
        
        return True


@dataclass
class TranslationResponse:
    """Schema for translation response"""
    input_text: str
    output_text: str
    input_language: str
    output_language: str
    timestamp: str
    confidence_score: Optional[float] = None


@dataclass
class VoiceRequest:
    """Schema for voice input request"""
    audio_data: bytes
    input_language: str
    output_language: str
    
    def validate(self):
        """Validate voice request"""
        if not self.audio_data:
            raise ValueError("Audio data cannot be empty")
        
        if self.input_language not in ['garhwali', 'kumaoni']:
            raise ValueError(f"Unsupported input language: {self.input_language}")
        
        if self.output_language not in ['hindi', 'english']:
            raise ValueError(f"Unsupported output language: {self.output_language}")
        
        return True