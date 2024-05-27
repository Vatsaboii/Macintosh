from config import db_connection
from functools import wraps
from flask import request, jsonify
import hashlib
import jwt
import time

SECRET = 'macintoshftw'

db = db_connection()


def gen_token(username):
    payload = {
        'username': username,
        'timestamp': int(time.time())
    }
    token = jwt.encode(payload, SECRET, algorithm='HS256')
    return token


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('token')
        decoded = validate_token(token)
        if decoded['valid']:
            return f(*args, **kwargs)
        else:
            return jsonify({
                'message': 'token is invalid or missing',
                'isSuccessful': False
            }), 403
    return decorated_function


def is_empty(username, password):
    if not username or not password:
        if not username:
            message = 'username cannot be empty'
        else:
            message = 'password cannot be empty'
        return jsonify({
            'message': message,
            'isSuccessful': False
        }), 400


def check_user(username):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    return user


def salty_pass(username, password):
    salt = 'scriptscribeftw'
    salted_pass = username + salt + password

    hashed_pass = hashlib.md5(salted_pass.encode())
    return hashed_pass.hexdigest()


def validate_user(username, password):
    user = check_user(username)
    if user:
        hashed_password = salty_pass(username, password)
        if hashed_password == user['password']:
            return True
    return False


def validate_token(token):
    try:
        payload = jwt.decode(token, SECRET, algorithms='HS256')
        return {'valid': True, 'payload': payload}
    except jwt.ExpiredSignatureError:
        return {'valid': False, 'error': 'Token has expired'}
    except jwt.InvalidTokenError:
        return {'valid': False, 'error': 'Invalid token'}
