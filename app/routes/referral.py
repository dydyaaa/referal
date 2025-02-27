from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.referral_service import ReferralService

referral_bp = Blueprint('referral', __name__)

@referral_bp.route('/code', methods=['POST'])
@jwt_required()
def create_referral_code():
    user_id = get_jwt_identity()
    data = request.get_json()
    expires_at = data.get('expires_at')  # формат: "YYYY-MM-DD"
    
    code = ReferralService.create_code(user_id, expires_at)
    return jsonify({'referral_code': code}), 201

@referral_bp.route('/code', methods=['DELETE'])
@jwt_required()
def delete_referral_code():
    user_id = get_jwt_identity()
    ReferralService.delete_code(user_id)
    return jsonify({'message': 'Referral code deleted'}), 200

@referral_bp.route('/code/by-email', methods=['GET'])
def get_code_by_email():
    email = request.args.get('email')
    code = ReferralService.get_code_by_email(email)
    return jsonify({'referral_code': code}), 200

@referral_bp.route('/referrals', methods=['GET'])
@jwt_required()
def get_referrals():
    user_id = get_jwt_identity()
    referrals = ReferralService.get_referrals(user_id)
    return jsonify({'referrals': referrals}), 200