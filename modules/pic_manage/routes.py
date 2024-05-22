from config import db_connection
from flask import Blueprint, jsonify, request
import os

pic_manage_bp = Blueprint('pic_manage', __name__)

db = db_connection()


@pic_manage_bp.route('/upload', methods=['POST'])
def upload_photo():
    if 'file' not in request.files:
        return jsonify({
            'message': 'File empty'
        }), 400

    if not 'user_id' in request.get_json:
        return jsonify({
            'message': 'user_id not provided'
        }), 400

    user_id = request.form['user_id']
    file = request.files['file']

    # res_data = model(user_id, file)
    # returns photo_id, photo_path, tags {tag_id, tag_name}

    # return jsonify({
    #     res_data
    # })


@pic_manage_bp.route('/delete/<photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    if not photo_id:
        return jsonify({
            'message': 'photo_id not provided'
        }), 400

    # delete photo from cloud
    cursor = db.cursor()
    cursor.execute(
        "SELECT photo_path from PHOTOS where photo_id = %s", (photo_id))
    photo = cursor.fetchone
    cursor.close()

    if not photo:
        return jsonify({
            'message': 'Photo not found'
        }), 404

    photo_path = photo[0]

    if os.path.exists(photo_path):
        os.remove(photo_path)
    else:
        return jsonify({
            'message': 'File not found on server'
        }), 404

    # todo: delete from photos and photo_tags table
