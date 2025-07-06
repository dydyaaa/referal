import logging
from app import db
from flask import current_app
from app.models.user import User
from app.models.personal_info import UserProfile
from app.utils.password_generator import generate_password
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError
from botocore.exceptions import ClientError
from PIL import Image
from io import BytesIO
from app.tasks.send_messages_tasks import send_password

logger = logging.getLogger('app.user')


class UserService:
    @staticmethod
    def upload_avatar(file, user_id):
        """
        Добавление аватара пользователя.
        Аргументы: 
            file: binary - загруженый аватар
            user_id: int - ID пользователя
        Возвращает:
            avatar_url: str - url на аватар пользователя
        Исключения:
            ClientError: Ошибка загрузки аватара на S3 хранилище
            SQLAlchemyError: При возникновении ошибок при работе с базой данных
        """
        
        config = current_app.config
        
        file_name = f'user_{user_id}.jpg'
        key = f'avatars/{file_name}'
        avatar_url = f'{config['S3_URL']}/{config['BUCKET_NAME']}/avatars/{file_name}'
        
        try:
            Image.open(BytesIO(file.read())).verify()
            file.seek(0)
        except Exception:
            logger.warning(f'File is not an image!')
            raise TypeError
        
        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > 5242880:
            logger.warning(f'File is too big')
            raise ValueError
        
        try:
            s3_client = current_app.s3_client
            s3_client.upload_fileobj(
                file,
                Bucket=config['BUCKET_NAME'],
                Key=key)
        except Exception as error:
            logger.error(f'Failed to upload avatar_url: {error}')
            raise ClientError

        try:
            user = User.query.filter_by(id=user_id).first()
            user.avatar_url = avatar_url
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            logger.error(f'Failed to add avatar_url: {error}')
            raise SQLAlchemyError
        
        return avatar_url
    
    
    @staticmethod
    def reset_password(email):
        """
        Сбрс пароля пользователя.
        Аргументы:
            email: str - Email пользователя
        Возвращает:
            None
        ---
        Исключения:
            ValueError - Если пользователя с таким email не существует
        """
        user = User.query.filter_by(email=email).first()
        if not user:
            logger.warning(f'Failed change password for {email}')
            raise ValueError('Invalid email')
        
        new_password = generate_password()
        
        try:
            from app.app_factory import celery
            result = celery.send_task('app.tasks.send_messages_tasks.send_password', args=(email, new_password))

        except Exception as error:
            logger.critical(f'Mail was not send! {error}')
        
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return user
    
    @staticmethod
    def change_password(user_id, new_password, new_password_again):
        """
        Смена пароля пользователя.
        Аргументы:
            user_id: int - ID пользователя
            new_password: str - Новый пароль
            new_password_again: str - Новый пароль еще раз
        Возвращает:
            User: Измененный объект пользователя
        Исключения:
            ValueError: Пароли не совпадают
        """
        user = User.query.filter_by(id=user_id).first()
        
        if new_password == new_password_again:
            user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            return user
        
        raise ValueError('Passwords are not equal')
    
    @staticmethod
    def add_user_info(user_id, full_name, phone_number=None, height_cm=None, weight_kg=None, goal=None, activity_level=None):
        """
        Добавление или обновление информации о пользователе.
        Аргументы:
            user_id: int - ID пользователя
            full_name: str - Полное имя пользователя
            phone_number: str - Номер телефона (необязательно)
            height_cm: float - Рост в сантиметрах (необязательно)
            weight_kg: float - Вес в килограммах (необязательно)
            goal: str - Цель пользователя (необязательно)
            activity_level: str - Уровень активности (необязательно)
        Возвращает:
            UserProfile: Объект профиля пользователя
        Исключения:
            SQLAlchemyError: Ошибка при работе с базой данных
        """
        try:
            profile = UserProfile.query.filter_by(user_id=user_id).first()
            if not profile:
                profile = UserProfile(user_id=user_id)
            
            profile.full_name = full_name
            profile.phone_number = phone_number
            profile.height_cm = height_cm
            profile.weight_kg = weight_kg
            profile.goal = goal
            profile.activity_level = activity_level
            
            db.session.add(profile)
            db.session.commit()
            
            return profile
        
        except SQLAlchemyError as error:
            db.session.rollback()
            logger.error(f'Failed to add or update user info: {error}')
            raise SQLAlchemyError('Ошибка при добавлении или обновлении информации о пользователе')
        
    @staticmethod
    def get_user_info(user_id):
        """
        Получение информации о пользователе.
        Аргументы:
            user_id: int - ID пользователя
        Возвращает:
            UserProfile: Объект профиля пользователя
        Исключения:
            SQLAlchemyError: Ошибка при работе с базой данных
        """
        try:
            profile = UserProfile.query.filter_by(user_id=user_id).first()
            if not profile:
                raise ValueError('User profile not found')
            return profile
        
        except SQLAlchemyError as error:
            logger.error(f'Failed to get user info: {error}')
            raise SQLAlchemyError('Ошибка при получении информации о пользователе')
        
    @staticmethod
    def change_user_info(user_id, full_name=None, phone_number=None, height_cm=None, weight_kg=None, goal=None, activity_level=None):
        """
        Изменение информации о пользователе.
        Аргументы:
            user_id: int - ID пользователя
            full_name: str - Полное имя пользователя (необязательно)
            phone_number: str - Номер телефона (необязательно)
            height_cm: float - Рост в сантиметрах (необязательно)
            weight_kg: float - Вес в килограммах (необязательно)
            goal: str - Цель пользователя (необязательно)
            activity_level: str - Уровень активности (необязательно)
        Возвращает:
            UserProfile: Объект профиля пользователя
        Исключения:
            SQLAlchemyError: Ошибка при работе с базой данных
        """
        
        try:
            profile = UserProfile.query.filter_by(user_id=user_id).first()
            if not profile:
                raise ValueError('User profile not found')
            
            if full_name is not None:
                profile.full_name = full_name
            if phone_number is not None:
                profile.phone_number = phone_number
            if height_cm is not None:
                profile.height_cm = height_cm
            if weight_kg is not None:
                profile.weight_kg = weight_kg
            if goal is not None:
                profile.goal = goal
            if activity_level is not None:
                profile.activity_level = activity_level
            
            db.session.commit()
            return profile
        
        except SQLAlchemyError as error:
            db.session.rollback()
            logger.error(f'Failed to change user info: {error}')
            raise SQLAlchemyError('Ошибка при изменении информации о пользователе')