from flask import Flask
from flask_mail import Mail
from google.cloud import storage
from google.oauth2 import service_account
import os
import json

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

    # Initialize GCS client using JSON from environment
    global gcs_client
    credentials_info = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    gcs_client = storage.Client(credentials=credentials, project=credentials.project_id)

    # Configure logging
    configure_logging(app)

    # Register blueprints
    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    return app
