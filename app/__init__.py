from flask import Flask
from flask_mail import Mail
from google.cloud import storage
from .utils.logger import configure_logging

mail = Mail()
gcs_client = None

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    from config.dev import DevConfig  # or dynamically select prod
    app.config.from_object(DevConfig)

    # Initialize extensions
    mail.init_app(app)
    global gcs_client
    gcs_client = storage.Client()

    # Configure logging
    configure_logging(app)

    # Register blueprints
    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    return app
