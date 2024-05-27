from flask import Blueprint, jsonify
from config import db_connection
from modules.auth.auth import token_required

tag_manage_bp = Blueprint('tag_manage', __name__)

db = db_connection()


@tag_manage_bp.route('/tags/user/<user_id>', methods=['GET'])
@token_required
def get_tags(user_id):
    cursor = db.cursor()
    cursor.execute(
        "SELECT tag_id, tag_name FROM tags WHERE user_id = %s", (user_id,))
    tags = cursor.fetchall()
    cursor.close()

    tag_list = []
    for tag in tags:
        tag_list.append({
            'tag_id': tag[0],
            'tag_name': tag[1]
        })

    return jsonify({
        'tags': tag_list,
        'isSuccessful': True
    }), 200


@tag_manage_bp.route('/tags/photo/<photo_id>', methods=['GET'])
@token_required
def get_photo_tags(photo_id):
    cursor = db.cursor()
    cursor.execute(
        "SELECT t.tag_id, t.tag_name FROM tags t INNER JOIN photo_tags pt ON t.tag_id = pt.tag_id WHERE pt.photo_id = %s",
        (photo_id,)
    )
    tags = cursor.fetchall()
    cursor.close()

    tag_list = []
    for tag in tags:
        tag_list.append({
            'tag_id': tag[0],
            'tag_name': tag[1]
        })

    return jsonify({
        'tags': tag_list,
        'isSuccessful': True
    }), 200
