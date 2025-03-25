import logging
from app import db
from flask import current_app
from app.models.user import User
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