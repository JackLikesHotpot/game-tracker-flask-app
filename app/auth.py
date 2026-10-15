from flask import Blueprint, jsonify, request, session
from .models import User


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({'error': 'Email and password are required.'}), 400
        
        user = User.query.filter_by(email=email).first()

        if user:
            if user.check_password(password):
                session['loggedin'] = True
                session['id'] = user.user_id
                session['username'] = user.profile.username
                return jsonify({"message": "Logged in successfully!"}), 200
            else:
                return (
                jsonify({"error": "Invalid email or password"}),
                401,
                )
        else:
            return (
            jsonify({"error": "Invalid email or password"}),
            401,
            )
            
    pass

