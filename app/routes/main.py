from flask import Blueprint, render_template, request, redirect, session
from app.auth.email import send_verification_email
from app.auth.validator import validate_email_domain, verify_code
from app.upload.uploader import handle_upload

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        if validate_email_domain(email):
            send_verification_email(email)
            return redirect('/verify')
        return "Unauthorized domain", 403
    return render_template('register.html')

@main_bp.route('/verify', methods=['POST'])
def verify():
    email = request.form['email']
    code = request.form['code']
    if verify_code(email, code):
        session['user'] = email
        return redirect('/upload')
    return "Verification failed", 401

@main_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user' not in session:
        return redirect('/register')
    if request.method == 'POST':
        return handle_upload(request)
    return render_template('upload.html')
