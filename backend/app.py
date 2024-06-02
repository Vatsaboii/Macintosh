from flask import Flask

from src.routes.auth import auth_bp
from src.routes.pictures import pictures_bp
from src.routes.tags import tags_bp

app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(pictures_bp, url_prefix='/api')
app.register_blueprint(tags_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
