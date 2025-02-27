from app import db
from app.models.user import User
from app.models.referral import Referral
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class AuthService:
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
            raise ValueError("Email is already registered")
        
        # Хеширование пароля
        password_hash = generate_password_hash(password)
        
        # Проверка реферального кода, если он указан
        referred_by = None
        if referral_code:
            referral = Referral.query.filter_by(code=referral_code, is_active=True).first()
            if not referral or referral.expires_at < datetime.now():
                raise ValueError("Invalid or expired referral code")
            referred_by = referral.user_id
        
        # Создание нового пользователя
        new_user = User(
            email=email,
            password_hash=password_hash,
            referred_by=referred_by
        )
        
        db.session.add(new_user)
        db.session.commit()
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
            raise ValueError("Invalid email or password")
        return user