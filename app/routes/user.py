from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService


user_bp = Blueprint('user', __name__)

@user_bp.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    try:
        user = UserService.reset_password(email)
        return jsonify({'message': f'Password reset for {user.email}'}), 200
    except ValueError as error:
        return jsonify({'message': f'{error}'}), 400
    
@user_bp.route('/change_password', methods=['POST'])
@jwt_required()
def chage_password():
    data = request.get_json()
    user_id = get_jwt_identity()
    new_password = data.get('new_password')
    new_password_again = data.get('new_password_again')
    
    try:
        user = UserService.change_password(user_id, new_password, new_password_again)
        return jsonify({'message': f'Password change for {user.email}'}), 200
    except ValueError as error:
        return jsonify({'message': f'{error}'}), 400
    
@user_bp.route('/upload_avatar', methods=['POST'])
@jwt_required()
def upload_avatar():
    file = request.files["avatar"]
    user_id = get_jwt_identity()
    
    try:
        avatar_url = UserService.upload_avatar(file, user_id)
    except TypeError:
        return jsonify({'message': 'file is not an image'}), 401
    except ValueError:
        return jsonify({'message': 'file is too big'}), 401
    
    return jsonify({'message': 'avatar upload', 'avatar_url': avatar_url}), 201