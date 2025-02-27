from app import db
from app.models.referral import Referral
from app.models.user import User
from datetime import datetime
from flask import current_app
import random
import string
import logging


logger = logging.getLogger('app.referral')


class ReferralService:
    CACHE_TIMEOUT = 3600
    
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
        
        try:
            redis_client = current_app.redis
            cache_key = f'referral_code:user:{user_id}'
            redis_client.setex(cache_key, ReferralService.CACHE_TIMEOUT, code)
            logger.debug(f'Cached referral code')
        except Exception as error:
            logger.warning(f'Failed to cache referral code in Redis - {error}')
        
        logger.info(f'Referral code created')
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
            logger.warning(f'No active referral code found')
            raise ValueError("No active referral code found for this user")
        
        referral.is_active = False  # Деактивируем, а не удаляем физически
        db.session.commit()
        
        try:
            redis_client = current_app.redis
            cache_key = f"referral_code:user:{user_id}"
            redis_client.delete(cache_key)
            logger.debug(f'Deleted referral code cache')
        except Exception as error:
            logger.warning(f'Failed to delete referral code from Redis - {error}')
            
        logger.info(f'Referral code deactivated for user {user_id}')

    @staticmethod
    def get_code_by_email(email):
        """
        Получение активного реферального кода по email пользователя.
        """
        user = User.query.filter_by(email=email).first()
        if not user:
            logger.warning(f'User not found')
            raise ValueError("User not found")
        
        try:
            redis_client = current_app.redis
            cache_key = f"referral_code:user:{user.id}"
            cached_code = redis_client.get(cache_key)
            if cached_code:
                logger.debug('Received referral code from chace')
                return cached_code
        except Exception as error:
            logger.warning(f'Redis unavailable, falling back to DB: {error}')
        
        code = Referral.query.filter_by(user_id=user.id, is_active=True).first()
        logger.info(f'Retrieved referral code from DB')
        return code.code if code else None

    @staticmethod
    def get_referrals(user_id):
        """
        Получение списка рефералов пользователя по его ID.
        """
        referrals = User.query.filter_by(referred_by=user_id).all()
        logger.info(f'Retrieved {len(referrals)} referrals')
        return [{'id': user.id, 'email': user.email} for user in referrals]