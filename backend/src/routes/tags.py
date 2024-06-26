from config import db
from flask import Blueprint, jsonify
from src.utils.auth_utils import token_required

tags_bp = Blueprint('tag_manage', __name__)


# retrieves available tags for a user
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


# retrieves all pictures associated with a particular tag
@tags_bp.route('/photo/tags/<tag_id>', methods=['GET'])
@token_required
def get_photos_by_tag(tag_id):
    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT p.photo_path 
            FROM photos p 
            INNER JOIN photo_tags pt ON p.photo_id = pt.photo_id 
            WHERE pt.tag_id = %s
        """, (tag_id,))
        photo_paths = cursor.fetchall()
        cursor.close()

        photos = [photo['photo_path'] for photo in photo_paths]

        return jsonify({
            'photos': photos
        }), 200
    except Exception as e:
        return jsonify({
            'message': f'Error retrieving photos: {e}'
        }), 500


# retrieves all tag_id from a particular picture
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
