from datetime import datetime
from typing import List, Dict, Optional

class DatabaseHelper:
    """
    Database helper for storing translations and voice samples.
    For Round-2, this uses in-memory storage (mock database).
    In production, this would connect to PostgreSQL/MySQL.
    """
    
    def __init__(self):
        # Mock database (in-memory storage)
        self.translations = []
        self.voice_samples = []
        self.next_translation_id = 1
        self.next_voice_id = 1
    
    # ===== TRANSLATION TABLE OPERATIONS =====
    
    def save_translation(self, input_text: str, output_text: str, 
                        input_lang: str, output_lang: str, 
                        confidence: Optional[float] = None) -> int:
        """Save translation to database"""
        translation = {
            'id': self.next_translation_id,
            'input_text': input_text,
            'output_text': output_text,
            'input_language': input_lang,
            'output_language': output_lang,
            'confidence_score': confidence,
            'timestamp': datetime.now().isoformat()
        }
        
        self.translations.append(translation)
        self.next_translation_id += 1
        
        return translation['id']
    
    def get_translation_by_id(self, translation_id: int) -> Optional[Dict]:
        """Get translation by ID"""
        for translation in self.translations:
            if translation['id'] == translation_id:
                return translation
        return None
    
    def get_recent_translations(self, limit: int = 10) -> List[Dict]:
        """Get recent translations"""
        return sorted(self.translations, 
                     key=lambda x: x['timestamp'], 
                     reverse=True)[:limit]
    
    # ===== VOICE SAMPLE TABLE OPERATIONS =====
    
    def save_voice_sample(self, audio_path: str, language: str, 
                         transcription: str) -> int:
        """Save voice sample to database"""
        voice_sample = {
            'id': self.next_voice_id,
            'audio_file_path': audio_path,
            'language': language,
            'transcription': transcription,
            'timestamp': datetime.now().isoformat()
        }
        
        self.voice_samples.append(voice_sample)
        self.next_voice_id += 1
        
        return voice_sample['id']
    
    def get_voice_sample_by_id(self, sample_id: int) -> Optional[Dict]:
        """Get voice sample by ID"""
        for sample in self.voice_samples:
            if sample['id'] == sample_id:
                return sample
        return None
    
    # ===== STATISTICS =====
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        return {
            'total_translations': len(self.translations),
            'total_voice_samples': len(self.voice_samples),
            'languages': {
                'garhwali': len([t for t in self.translations if t['input_language'] == 'garhwali']),
                'kumaoni': len([t for t in self.translations if t['input_language'] == 'kumaoni'])
            }
        }


# Database schema design (for documentation)
DATABASE_SCHEMA = """
-- Table: translations
CREATE TABLE translations (
    id SERIAL PRIMARY KEY,
    input_text TEXT NOT NULL,
    output_text TEXT NOT NULL,
    input_language VARCHAR(20) NOT NULL,
    output_language VARCHAR(20) NOT NULL,
    confidence_score FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: voice_samples
CREATE TABLE voice_samples (
    id SERIAL PRIMARY KEY,
    audio_file_path VARCHAR(255) NOT NULL,
    language VARCHAR(20) NOT NULL,
    transcription TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: language_metadata
CREATE TABLE language_metadata (
    id SERIAL PRIMARY KEY,
    language_code VARCHAR(20) UNIQUE NOT NULL,
    language_name VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    sample_count INTEGER DEFAULT 0
);

-- Indexes
CREATE INDEX idx_translations_timestamp ON translations(timestamp);
CREATE INDEX idx_translations_language ON translations(input_language, output_language);
CREATE INDEX idx_voice_language ON voice_samples(language);
"""