import requests
import logging
from app import db
from flask import current_app
from datetime import datetime
from app.models.user import User
from app.models.referral import Referral
from app.utils.message_sendrer import send_password
from app.utils.password_generator import generate_password
from werkzeug.security import generate_password_hash, check_password_hash


logger = logging.getLogger('app.auth')


class AuthService:
    @staticmethod
    def validate_email(email):
        """
        Проверка валидности email через Email Hunter API.
        """
        api_key = current_app.config.get('EMAIL_HUNTER_API_KEY')
        if not api_key:
            logger.error('Email Hunter API key is not configured')
            return True
        
        url = f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}'

        try:
            response = requests.get(url)
            data = response.json()
            logger.debug(f'Email Hunter response for {email}')
            return data.get("data", {}).get("status") == "valid"
        except requests.RequestException:
            logger.error('Email verification failed')
            return True # Если API недоступен, пропускаем валидацию

    @staticmethod
    def register(email, password, referral_code=None):
        """
        Регистрация нового пользователя.
        Аргументы:
            email: str - Email пользователя
            password: str - Пароль пользователя
            referral_code: str (опционально) - Реферальный код для связи с реферером
        Возвращает:
            User - Созданный объект пользователя
        Исключения:
            ValueError - Если email уже занят или реферальный код недействителен
        """
        # Проверка, существует ли пользователь с таким email
        if User.query.filter_by(email=email).first():
            logger.warning('Registration with existing email')
            raise ValueError('Email is already registered')
        
        if not AuthService.validate_email(email):
            logger.warning('Invalid email for registration')
            raise ValueError('Invalid email address')
        
        # Хеширование пароля
        password_hash = generate_password_hash(password)
        
        # Проверка реферального кода, если он указан
        referred_by = None
        if referral_code:
            referral = Referral.query.filter_by(code=referral_code, is_active=True).first()
            if not referral or referral.expires_at < datetime.now():
                logger.warning('Invalid or expired referral code')
                raise ValueError('Invalid or expired referral code')
            referred_by = referral.user_id
        
        # Создание нового пользователя
        new_user = User(
            email=email,
            password_hash=password_hash,
            referred_by=referred_by
        )
        
        db.session.add(new_user)
        db.session.commit()
        logger.info(f'User registered successfully: {email}')
        return new_user

    @staticmethod
    def login(email, password):
        """
        Аутентификация пользователя.
        Аргументы:
            email: str - Email пользователя
            password: str - Пароль пользователя
        Возвращает:
            User - Объект пользователя, если аутентификация успешна
        Исключения:
            ValueError - Если email или пароль неверны
        """
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            logger.warning(f'Failed login for {email}')
            raise ValueError("Invalid email or password")
        logger.info(f"Success login for {email}")
        return user
    
    @staticmethod
    def reset_password(email):
        """
        Сбрс пароля пользователя.
        Аргументы:
            email: str - Email пользователя
        Возвращает:
        ---
        Исключения:
            ValueError - Если пользователя с таким email не существует
        """
        user = User.query.filter_by(email=email).first()
        if not user:
            logger.warning(f'Failed change password for {email}')
            raise ValueError('Invalid email')
        
        new_password = generate_password()
        # print(new_password)
        
        try:
            send_password(email, new_password)
        except Exception as error:
            pass
        
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return user