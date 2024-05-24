from config import db_connection
from flask import Blueprint, jsonify, make_response, request
from .auth import check_user, gen_token, salty_pass, validate_creds

auth_bp = Blueprint('auth', __name__)

db = db_connection()


@auth_bp.route('/api/login', methods=['POST'])
def auth():

    def user_auth(username, password):
        cursor = db.cursor()
        # todo: validate username and salty_pass(username,password)
        # cursor.execute()
        return True

    data = request.get_json()
    username = data['username']
    password = data['password']

    # validate_creds() only returns when there's an error
    not_valid = validate_creds(username, password)
    if not_valid:
        return not_valid

    if not check_user(username):
        return jsonify({
            'message': 'user does not exist',
            'isSuccessful': False
        }), 401

    if user_auth(username, password):
        token = gen_token(username)
        response = make_response(jsonify({
            'message': 'logged in',
            'isSuccessful': True
        }))
        response.set_cookie('token', token)
        return response, 200
    else:
        return jsonify({
            'message': 'incorrect password',
            'isSuccessful': False
        }), 401


@auth_bp.route('/api/signup', methods=['POST'])
def signup():

    def add_user(username, hashed_pass):
        # todo: insert username and hashed_pass in db
        return

    data = request.get_json()
    username = data['username']
    password = data['password']

    # validate_creds() only returns when there's an error
    not_valid = validate_creds(username, password)
    if not_valid:
        return not_valid

    if check_user(username):
        return jsonify({
            'message': 'username already taken',
            'isSuccessful': False
        }), 409

    hashed_pass = salty_pass(username, password)
    if (add_user(username, hashed_pass)):
        return jsonify({
            'message': 'signed up',
            'isSuccessful': True
        }), 201
