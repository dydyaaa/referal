from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.services.auth_service import AuthService


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email, password = data.get('email'), data.get('password')
    referral_code = data.get('referral_code')
    
    try:
        user = AuthService.register(email, password, referral_code)
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'message': 'User registered', 
                        'user_id': user.id, 
                        'access_token': access_token}), 201
    except ValueError as error:
        return jsonify({'message': f'{error}'}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email, password = data.get('email'), data.get('password')
    
    try:
        user = AuthService.login(email, password)
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'message': 'User authorized',
                        'user_id': user.id,
                        'access_token': access_token}), 200
    except ValueError as error:
        return jsonify({'message': f'{error}'}), 401
