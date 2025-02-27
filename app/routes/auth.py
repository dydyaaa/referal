from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from app.services.auth_service import AuthService 


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email, password = data.get('email'), data.get('password')
    referral_code = data.get('referral_code')
    
    user = AuthService.register(email, password, referral_code)
    return jsonify({'message': 'User registered', 'user_id': user.id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email, password = data.get('email'), data.get('password')
    
    user = AuthService.login(email, password)
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200