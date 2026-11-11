import os
from dotenv import load_dotenv
from flask import Flask
from .auth import auth_bp
from .models import db
from .services.populate_db import initialise_database
from .routes.games import games_bp

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(games_bp)

    initialise_database()

    return app