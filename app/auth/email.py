import random, string
from flask_mail import Message
from app import mail

codes = {}  # In-memory storage

def generate_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

def send_verification_email(email):
    code = generate_code()
    codes[email] = code
    msg = Message("Your Verification Code", recipients=[email])
    msg.body = f"Your code is: {code}"
    mail.send(msg)

def get_stored_code(email):
    return codes.get(email)
