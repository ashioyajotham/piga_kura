from flask import Blueprint, request, jsonify
from app.services.auth import AuthService
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        user = AuthService.register_user(
            email=data['email'],
            voter_id=data['voter_id'],
            password=data['password']
        )
        return jsonify({'message': 'Registration successful'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = AuthService.verify_user(data['email'], data['password'])
    if user:
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401
