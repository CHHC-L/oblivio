import os

class DevConfig:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    WHITELIST_DOMAINS = os.environ.get('WHITELIST_DOMAINS')
