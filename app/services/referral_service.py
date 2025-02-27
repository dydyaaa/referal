from app import db
from app.models.referral import Referral
from app.models.user import User
from datetime import datetime
import random
import string


class ReferralService:
    @staticmethod
    def create_code(user_id, expires_at):
        """
        Создание нового реферального кода для пользователя.
        Деактивирует существующий активный код, если он есть.
        """
        # Деактивируем существующий код
        Referral.query.filter_by(user_id=user_id, is_active=True).update({'is_active': False})
        
        # Генерируем новый код
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        expires_at = datetime.strptime(expires_at, '%Y-%m-%d')
        
        new_code = Referral(code=code, user_id=user_id, expires_at=expires_at)
        db.session.add(new_code)
        db.session.commit()
        return code

    @staticmethod
    def delete_code(user_id):
        """
        Удаление активного реферального кода пользователя.
        Аргументы:
            user_id: int - ID пользователя
        Исключения:
            ValueError - Если активного кода нет
        """
        referral = Referral.query.filter_by(user_id=user_id, is_active=True).first()
        if not referral:
            raise ValueError("No active referral code found for this user")
        
        referral.is_active = False  # Деактивируем, а не удаляем физически
        db.session.commit()

    @staticmethod
    def get_code_by_email(email):
        """
        Получение активного реферального кода по email пользователя.
        """
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError("User not found")
        code = Referral.query.filter_by(user_id=user.id, is_active=True).first()
        return code.code if code else None

    @staticmethod
    def get_referrals(user_id):
        """
        Получение списка рефералов пользователя по его ID.
        """
        referrals = User.query.filter_by(referred_by=user_id).all()
        return [{'id': user.id, 'email': user.email} for user in referrals]