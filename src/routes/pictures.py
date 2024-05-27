from config import db
from flask import Blueprint, jsonify, request
import os
from src.utils.auth_utils import token_required

pictures_bp = Blueprint('pictures', __name__)


@pictures_bp.route('/upload', methods=['POST'])
@token_required
def upload_photo():
    if 'file' not in request.files:
        return jsonify({
            'message': 'File empty'
        }), 400

    if not request.get_json() or 'user_id' not in request.get_json():
        return jsonify({
            'message': 'user_id not provided'
        }), 400

    user_id = request.form['user_id']
    file = request.files['file']

    try:
        # todo: import model method
        res_data = model(user_id, file)
        return jsonify({
            'message': 'Photo uploaded successfully',
            'data': res_data
        }), 201
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
        user_id = request.get_json().get('user_id')
        cursor.execute(
            "DELETE FROM photo_tags WHERE photo_id = %s", (photo_id,))
        cursor.execute(
            "DELETE FROM photos WHERE user_id = %s AND photo_id = %s", (user_id, photo_id))
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
