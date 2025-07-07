from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService
from sqlalchemy.exc import SQLAlchemyError


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
    
@user_bp.route('/get_email', methods=['GET'])
@jwt_required()
def get_email():
    user_id = get_jwt_identity()
    
    try:
        email = UserService.get_email(user_id)
        return jsonify({'email': email}), 200
    except ValueError as error:
        return jsonify({'message': f'{error}'}), 400
    except TypeError as error:
        return jsonify({'message': f'{error}'}), 400
    except SQLAlchemyError as error:
        return jsonify({'message': 'Database error'}), 500
    
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

@user_bp.route('/get_user_info', methods=['GET'])
@jwt_required()
def get_user_info():
    user_id = get_jwt_identity()
    
    try:
        user_info = UserService.get_user_info(user_id)
        return jsonify({'user_info': user_info.to_dict()}), 200
    except ValueError as error:
        return jsonify({'message': f'{error}'}), 400
    except TypeError as error:
        return jsonify({'message': f'{error}'}), 400
    except SQLAlchemyError as error:
        return jsonify({'message': 'Database error'}), 500
    
@user_bp.route('/add_user_info', methods=['POST'])
@jwt_required()
def add_user_info():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    try:
        user_info = UserService.add_user_info(
            user_id=user_id,
            full_name=data.get('full_name'),
            phone_number=data.get('phone_number'),
            height_cm=data.get('height_cm'),
            weight_kg=data.get('weight_kg'),
            goal=data.get('goal'),
            activity_level=data.get('activity_level')
        )
        return jsonify({'user_info': user_info.to_dict()}), 201
    except ValueError as error:
        return jsonify({'message': f'{error}'}), 400
    except TypeError as error:
        return jsonify({'message': f'{error}'}), 400
    except SQLAlchemyError as error:
        return jsonify({'message': 'Database error'}), 500
    
@user_bp.route('/change_user_info', methods=['PUT'])
@jwt_required()
def change_user_info():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    try:
        user_info = UserService.change_user_info(
            user_id=user_id,
            full_name=data.get('full_name'),
            phone_number=data.get('phone_number'),
            height_cm=data.get('height_cm'),
            weight_kg=data.get('weight_kg'),
            goal=data.get('goal'),
            activity_level=data.get('activity_level')
        )
        return jsonify({'user_info': user_info.to_dict()}), 200
    except ValueError as error:
        return jsonify({'message': f'{error}'}), 400
    except TypeError as error:
        return jsonify({'message': f'{error}'}), 400
    except SQLAlchemyError as error:
        return jsonify({'message': 'Database error'}), 500