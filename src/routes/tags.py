from config import db
from flask import Blueprint, jsonify
from src.utils.auth_utils import token_required

tags_bp = Blueprint('tag_manage', __name__)


@tags_bp.route('/tags/user/<username>', methods=['GET'])
@token_required
def get_tags(username):
    cursor = db.cursor()
    cursor.execute(
        "SELECT tag_id, tag_name FROM tags WHERE username = %s", (username,))
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


@tags_bp.route('/tags/photo/<photo_id>', methods=['GET'])
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
        'tags': tag_list
    }), 200
