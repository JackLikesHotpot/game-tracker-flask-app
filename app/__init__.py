import os
from dotenv import load_dotenv
from flask import Flask
from .routes import main as main_bp
from .auth import auth_bp
from .models import db


load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    db.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app