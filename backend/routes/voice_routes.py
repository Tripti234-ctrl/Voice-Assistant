from flask import Blueprint, request, jsonify
import base64
import os
from models.schemas import VoiceRequest
from utils.ml_integration import MLIntegration
from utils.db_helper import DatabaseHelper

voice_bp = Blueprint('voice', __name__)

# Initialize services
ml_integration = MLIntegration()
db = DatabaseHelper()


@voice_bp.route('/voice-to-text', methods=['POST'])
def voice_to_text():
    """
    Convert voice audio to text using ASR
    
    Request JSON:
    {
        "audio_data": "base64_encoded_audio",
        "input_language": "garhwali"
    }
    
    OR send as multipart/form-data with audio file
    """
    try:
        # Check if audio sent as file or base64
        if 'audio_file' in request.files:
            # Audio sent as file
            audio_file = request.files['audio_file']
            input_lang = request.form.get('input_language', 'garhwali').lower()
            
            # Save temporarily
            temp_path = f'/tmp/{audio_file.filename}'
            audio_file.save(temp_path)
            
            # Process with ASR
            asr_result = ml_integration.speech_to_text(temp_path, input_lang)
            
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
        else:
            # Audio sent as base64
            data = request.get_json()
            audio_base64 = data.get('audio_data')
            input_lang = data.get('input_language', 'garhwali').lower()
            
            if not audio_base64:
                return jsonify({
                    'error': 'No audio data provided'
                }), 400
            
            # Decode base64
            audio_bytes = base64.b64decode(audio_base64)
            
            # Save temporarily
            temp_path = '/tmp/temp_audio.wav'
            with open(temp_path, 'wb') as f:
                f.write(audio_bytes)
            
            # Process with ASR
            asr_result = ml_integration.speech_to_text(temp_path, input_lang)
            
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
        # Save to database
        db.save_voice_sample(
            audio_path='temp_audio.wav',
            language=input_lang,
            transcription=asr_result.get('text', '')
        )
        
        return jsonify({
            'success': True,
            'data': {
                'text': asr_result.get('text'),
                'confidence': asr_result.get('confidence'),
                'language': input_lang
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@voice_bp.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    """
    Convert text to speech audio
    
    Request JSON:
    {
        "text": "मुझे पेट दर्द है",
        "language": "hindi"
    }
    """
    try:
        data = request.get_json()
        
        text = data.get('text', '')
        language = data.get('language', 'hindi').lower()
        
        if not text:
            return jsonify({
                'error': 'No text provided'
            }), 400
        
        # Generate speech using TTS
        audio_bytes = ml_integration.text_to_speech(text, language)
        
        # Convert to base64 for response
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        return jsonify({
            'success': True,
            'data': {
                'audio_data': audio_base64,
                'text': text,
                'language': language
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@voice_bp.route('/voice-translate', methods=['POST'])
def voice_translate():
    """
    Complete voice translation pipeline:
    Voice → ASR → Translation → TTS
    
    Request: audio file
    Response: translated text + audio
    """
    try:
        if 'audio_file' not in request.files:
            return jsonify({
                'error': 'No audio file provided'
            }), 400
        
        audio_file = request.files['audio_file']
        input_lang = request.form.get('input_language', 'garhwali').lower()
        output_lang = request.form.get('output_language', 'hindi').lower()
        
        # Save audio temporarily
        temp_audio_path = f'/tmp/{audio_file.filename}'
        audio_file.save(temp_audio_path)
        
        # Step 1: ASR (Voice → Text)
        asr_result = ml_integration.speech_to_text(temp_audio_path, input_lang)
        input_text = asr_result.get('text', '')
        
        # Step 2: Translation
        translation = ml_integration.translate_text(input_text, input_lang, output_lang)
        output_text = translation.get('translated_text', '')
        
        # Step 3: TTS (Text → Voice)
        output_audio = ml_integration.text_to_speech(output_text, output_lang)
        output_audio_base64 = base64.b64encode(output_audio).decode('utf-8')
        
        # Save to database
        db.save_translation(
            input_text=input_text,
            output_text=output_text,
            input_lang=input_lang,
            output_lang=output_lang,
            confidence=translation.get('confidence')
        )
        
        # Clean up
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
        
        return jsonify({
            'success': True,
            'data': {
                'input_text': input_text,
                'output_text': output_text,
                'input_language': input_lang,
                'output_language': output_lang,
                'output_audio': output_audio_base64,
                'asr_confidence': asr_result.get('confidence'),
                'translation_confidence': translation.get('confidence')
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500