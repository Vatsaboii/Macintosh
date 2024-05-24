from flask import Blueprint, jsonify

from config import db_connection
from modules.auth.auth import token_required

tag_manage_bp = Blueprint('tag_manage', __name__)

db = db_connection()


@tag_manage_bp.route('/tags/<user_id>', methods=['GET'])
@token_required
def get_tags(user_id):
    cursor = db.cursor()
    cursor.execute(
        "SELECT tag_id, tag_name FROM tags WHERE user_id = %s", (user_id))
    tags = cursor.fetchall()
    cursor.close()

    tag_list = []
    for tag in tags:
        tag_list.append({
            'tag_id': tag[0],
            'tag_name': tag[1]
        })

    return jsonify({
        'tags': tag_list
    }), 200


@tag_manage_bp.route('/tags/<photo_id>', methods=['GET'])
@token_required
def get_photo_tag(photo_id):
    cursor = db.cursor()
    # todo: fetch list of all tags for a picture
    # cursor.execute()
    tags = cursor.fetchall()
    cursor.close()

    tag_list = []
    for tag in tags:
        tag_list.append({
            'tag_id': tag[0],
            'tag_name': tag[1]
        })

    return jsonify({
        'tags': tag_list
    }), 200
