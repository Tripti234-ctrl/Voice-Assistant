from flask import Blueprint
from .users import users_bp
from .voice import voice_bp

# Import your route modules

# Export blueprints
__all__ = ['users_bp', 'voice_bp']