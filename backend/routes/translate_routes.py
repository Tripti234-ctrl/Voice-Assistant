from flask import Blueprint, request, jsonify
from datetime import datetime
from models.schemas import TranslationRequest, TranslationResponse
from utils.ml_integration import MLIntegration
from utils.db_helper import DatabaseHelper

translate_bp = Blueprint('translate', __name__)

# Initialize ML integration and database
ml_integration = MLIntegration()
db = DatabaseHelper()


@translate_bp.route('/translate', methods=['POST'])
def translate():
    """
    Translate text from Garhwali/Kumaoni to Hindi/English
    
    Request JSON:
    {
        "text": "म्यर पेट दुखाण छ",
        "input_language": "garhwali",
        "output_language": "hindi"
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'message': 'Request body must be JSON'
            }), 400
        
        # Validate request
        trans_request = TranslationRequest(
            text=data.get('text', ''),
            input_language=data.get('input_language', '').lower(),
            output_language=data.get('output_language', '').lower()
        )
        
        trans_request.validate()
        
        # Call ML translation service
        translation_result = ml_integration.translate_text(
            text=trans_request.text,
            input_lang=trans_request.input_language,
            output_lang=trans_request.output_language
        )
        
        # Save to database
        db.save_translation(
            input_text=trans_request.text,
            output_text=translation_result['translated_text'],
            input_lang=trans_request.input_language,
            output_lang=trans_request.output_language,
            confidence=translation_result.get('confidence')
        )
        
        # Prepare response
        response = TranslationResponse(
            input_text=trans_request.text,
            output_text=translation_result['translated_text'],
            input_language=trans_request.input_language,
            output_language=trans_request.output_language,
            timestamp=datetime.now().isoformat(),
            confidence_score=translation_result.get('confidence')
        )
        
        return jsonify({
            'success': True,
            'data': {
                'input': response.input_text,
                'output': response.output_text,
                'input_language': response.input_language,
                'output_language': response.output_language,
                'confidence': response.confidence_score,
                'timestamp': response.timestamp
            }
        }), 200
        
    except ValueError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@translate_bp.route('/translate/batch', methods=['POST'])
def translate_batch():
    """
    Translate multiple texts at once
    
    Request JSON:
    {
        "texts": ["text1", "text2"],
        "input_language": "garhwali",
        "output_language": "hindi"
    }
    """
    try:
        data = request.get_json()
        
        texts = data.get('texts', [])
        input_lang = data.get('input_language', '').lower()
        output_lang = data.get('output_language', '').lower()
        
        if not texts or not isinstance(texts, list):
            return jsonify({
                'error': 'Invalid input',
                'message': 'texts must be a non-empty list'
            }), 400
        
        results = []
        for text in texts:
            translation = ml_integration.translate_text(text, input_lang, output_lang)
            results.append({
                'input': text,
                'output': translation['translated_text'],
                'confidence': translation.get('confidence')
            })
        
        return jsonify({
            'success': True,
            'data': {
                'translations': results,
                'count': len(results)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@translate_bp.route('/translations/recent', methods=['GET'])
def get_recent_translations():
    """Get recent translations from database"""
    try:
        limit = request.args.get('limit', 10, type=int)
        recent = db.get_recent_translations(limit=limit)
        
        return jsonify({
            'success': True,
            'data': {
                'translations': recent,
                'count': len(recent)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500