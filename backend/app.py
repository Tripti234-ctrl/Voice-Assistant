from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from routes.translate_routes import translate_bp
from routes.voice_routes import voice_bp
from utils.db_helper import db, DATABASE_SCHEMA

def create_app():
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app, origins=Config.CORS_ORIGINS)
    
    # Register blueprints
    app.register_blueprint(translate_bp, url_prefix='/api')
    app.register_blueprint(voice_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """API health check"""
        return jsonify({
            'status': 'healthy',
            'service': 'Garhwali-Kumaoni Voice Assistant API',
            'version': '1.0.0',
            'endpoints': {
                'translate': '/api/translate',
                'voice_to_text': '/api/voice-to-text',
                'text_to_speech': '/api/text-to-speech',
                'voice_translate': '/api/voice-translate'
            }
        }), 200
    
    # Database schema endpoint (for documentation)
    @app.route('/api/db-schema', methods=['GET'])
    def get_db_schema():
        """Get database schema"""
        return jsonify({
            'schema': DATABASE_SCHEMA,
            'stats': db.get_stats()
        }), 200
    
    # Supported languages endpoint
    @app.route('/api/languages', methods=['GET'])
    def get_languages():
        """Get supported languages"""
        return jsonify({
            'input_languages': Config.SUPPORTED_INPUT_LANGUAGES,
            'output_languages': Config.SUPPORTED_OUTPUT_LANGUAGES
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested endpoint does not exist'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Something went wrong on our end'
        }), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    print("🚀 Garhwali-Kumaoni Voice Assistant API Starting...")
    print(f"📍 Running on http://{Config.HOST}:{Config.PORT}")
    print(f"🔗 Health Check: http://{Config.HOST}:{Config.PORT}/api/health")
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )