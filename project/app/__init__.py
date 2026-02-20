"""
__init__.py

Flask application factory for NarrativeIQ.

Responsibilities:
    - Initialize Flask app with configuration settings
    - Load environment variables from .env file
    - Initialize database (SQLAlchemy)
    - Register blueprints (routes)
    - Return a fully configured Flask application instance

Notes:
    - Uses the application factory pattern for modularity and testing
    - Environment variables (API keys, database URI) are loaded via python-dotenv
    - SQLAlchemy is initialized but models are defined separately
    - Main routes are registered via Blueprint (main_routes)

Typical Usage:
    from app import create_app
    app = create_app()
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Initialize SQLAlchemy (database connection handler)
db = SQLAlchemy()


def create_app():
    """
    Application Factory

    Returns a fully configured Flask app instance.

    Workflow:
        1. Load environment variables from .env
        2. Instantiate Flask app
        3. Load configuration settings
        4. Initialize SQLAlchemy with the app
        5. Register application blueprints (routes)
        6. Return the app instance

    Returns:
        Flask: Configured Flask application
    """

    # Load environment variables from .env file
    load_dotenv()

    # Instantiate Flask app
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # Initialize database with app
    db.init_app(app)

    # Register main application routes
    from app.routes.main_routes import main
    app.register_blueprint(main)

    return app