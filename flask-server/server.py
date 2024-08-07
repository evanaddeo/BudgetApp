from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import random
import string
import os
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

mail = Mail(app)

reset_codes = {}

def generate_reset_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    reset_code = generate_reset_code()
    reset_codes[email] = {
        'code': reset_code,
        'expires_at': datetime.utcnow() + timedelta(minutes=15)
    }

    msg = Message('Password Reset Code',
                  recipients=[email],
                  body=f'Your password reset code is: {reset_code}')
    mail.send(msg)

    return jsonify({'message': 'Reset code sent to email'}), 200

@app.route('/api/confirm-reset-code', methods=['POST'])
def confirm_reset_code():
    email = request.json.get('email')
    code = request.json.get('code')

    if not email or not code:
        return jsonify({'error': 'Email and code are required'}), 400

    stored_code = reset_codes.get(email)
    if not stored_code or stored_code['code'] != code:
        return jsonify({'error': 'Invalid reset code'}), 400

    if datetime.utcnow() > stored_code['expires_at']:
        return jsonify({'error': 'Reset code has expired'}), 400

    # Code is valid, allow password reset
    return jsonify({'message': 'Reset code confirmed'}), 200

@app.route('/api/update-password', methods=['POST'])
def update_password():
    email = request.json.get('email')
    new_password = request.json.get('newPassword')

    if not email or not new_password:
        return jsonify({'error': 'Email and new password are required'}), 400

    # Here you would update the user's password in your database
    # For this example, we'll just simulate a successful update
    
    # Clear the reset code after successful password update
    if email in reset_codes:
        del reset_codes[email]

    return jsonify({'message': 'Password updated successfully'}), 200


# Members api route
# @app.route("/members")
# def members():
#     return {"members": ["Member1", "Mmeber2", "Member3"]}


if __name__ == "__main__":
    app.run(debug=True)