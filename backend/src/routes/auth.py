from config import db
from flask import Blueprint, jsonify, make_response, request
from src.utils.auth_utils import check_user, gen_token, if_empty, salty_pass, validate_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def auth():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # if_empty() only returns when there's an error
    not_valid = if_empty(username, password)
    if not_valid:
        return not_valid

    if not check_user(username):
        return jsonify({
            'message': 'user does not exist'
        }), 401

    if validate_user(username, password):
        token = gen_token(username)
        response = make_response(jsonify({
            'message': 'logged in'
        }))
        response.set_cookie('token', token)
        return response, 200
    else:
        return jsonify({
            'message': 'incorrect password'
        }), 401


@auth_bp.route('/signup', methods=['POST'])
def signup():

    def add_user(username, hashed_pass):
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pass))
            db.commit()
            cursor.close()
            return True
        except Exception as e:
            db.rollback()
            cursor.close()
            return False

    data = request.get_json()
    username = data['username']
    password = data['password']

    # if_empty() only returns when there's an error
    not_valid = if_empty(username, password)
    if not_valid:
        return not_valid

    if check_user(username):
        return jsonify({
            'message': 'username already taken'
        }), 409

    hashed_pass = salty_pass(username, password)
    if add_user(username, hashed_pass):
        return jsonify({
            'message': 'signed up'
        }), 201
    else:
        return jsonify({
            'message': 'error signing up'
        }), 500
