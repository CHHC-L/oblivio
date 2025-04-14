from flask import current_app
from app.auth.email import get_stored_code

def validate_email_domain(email):
    domain = email.split('@')[-1]
    allowed_domains = current_app.config.get("WHITELIST_DOMAINS", "").split(',')
    return domain in allowed_domains

def verify_code(email, submitted_code):
    return submitted_code == get_stored_code(email)
