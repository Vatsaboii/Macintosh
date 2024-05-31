from config import UPLOAD_DIR
import hashlib
import base64
import time
import os
from werkzeug.utils import secure_filename


def random_hash():
    timestamp = str(time.time())
    hashed = hashlib.sha256(timestamp.encode()).digest()
    encoded = base64.b64encode(hashed)
    result = ''.join(char for char in encoded.decode() if char.isalnum())[:6]
    return result


def move_file(username, file):
    user_dir = os.path.join(UPLOAD_DIR, username)
    os.makedirs(user_dir, exist_ok=True)
    filename = secure_filename(file.filename)
    destination = os.path.join(user_dir, filename)
    file.save(destination)
    return destination
