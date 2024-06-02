from flask import Flask
from flask_cors import CORS

from src.routes.auth import auth_bp
from src.routes.pictures import pictures_bp
from src.routes.tags import tags_bp

app = Flask(__name__)
CORS(app)


app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(pictures_bp, url_prefix='/api')
app.register_blueprint(tags_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
