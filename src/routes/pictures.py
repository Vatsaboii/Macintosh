from config import db
from flask import Blueprint, jsonify, request
import os
from src.utils.auth_utils import token_required
from src.utils.file_utils import move_file, random_hash

pictures_bp = Blueprint('pictures', __name__)


@pictures_bp.route('/upload', methods=['POST'])
@token_required
def upload_photo():
    if 'file' not in request.files:
        return jsonify({
            'message': 'File empty'
        }), 400

    if not request.get_json() or 'username' not in request.get_json():
        return jsonify({
            'message': 'Username not provided'
        }), 400

    username = request.get_json()['username']
    file = request.files['file']

    try:
        destination = move_file(username, file)
        photo_id = random_hash()

        # todo: return a list of tags with model method
        tags = model(username, file)

        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO photos (username, photo_path) VALUES (%s, %s)", (username, destination))
            photo_id = cursor.lastrowid
        db.commit()

        for tag in tags:
            with db.cursor() as cursor:
                cursor.execute(
                    "INSERT IGNORE INTO tags (tag_name, username) VALUES (%s, %s)", (tag, username))
                tag_id = cursor.lastrowid
                cursor.execute(
                    "INSERT IGNORE INTO photo_tags (photo_id, tag_id) VALUES (%s, %s)", (photo_id, tag_id))
            db.commit()

        response = jsonify({
            'photo_id': photo_id,
            'photo_path': destination,
            'tags': tags,
        })
        return response, 200
    except Exception as e:
        return jsonify({
            'message': f'Error uploading photo: {e}'
        }), 500


@pictures_bp.route('/delete/<photo_id>', methods=['DELETE'])
@token_required
def delete_photo(photo_id):
    if not photo_id:
        return jsonify({
            'message': 'photo_id not provided'
        }), 400

    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT photo_path FROM photos WHERE photo_id = %s", (photo_id,))
    photo = cursor.fetchone()
    cursor.close()

    if not photo:
        return jsonify({
            'message': 'Photo not found'
        }), 404

    photo_path = photo['photo_path']

    if os.path.exists(photo_path):
        os.remove(photo_path)
    else:
        return jsonify({
            'message': 'File not found on server'
        }), 404

    try:
        cursor = db.cursor()
        username = request.get_json().get('username')
        cursor.execute(
            "DELETE FROM photo_tags WHERE photo_id = %s", (photo_id,))
        cursor.execute(
            "DELETE FROM photos WHERE username = %s AND photo_id = %s", (username, photo_id))
        db.commit()
        cursor.close()
        return jsonify({
            'message': 'Photo deleted',
        }), 200
    except Exception as e:
        db.rollback()
        cursor.close()
        return jsonify({
            'message': f'Error deleting photo: {e}'
        }), 500
