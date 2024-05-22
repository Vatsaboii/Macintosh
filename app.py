from flask import Flask

from modules.pic_manage.routes import pic_manage_bp

app = Flask(__name__)

app.register_blueprint(pic_manage_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
