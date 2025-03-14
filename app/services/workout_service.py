import logging
from app import db
from flask import current_app
from datetime import datetime
from app.utils.validators import WorkoutValidate
from app.models.user import User
from app.models.workout import Workout
from app.models.exercise import Exercise
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import Forbidden


logger = logging.getLogger('app.auth')


class Calendar():
    @staticmethod
    def add_workout(user_id,
                    title,
                    workout_date,
                    notes,
                    workout_type):
        """
        Добавление новой тренировки.
        Аргументы:
            user_id: int - ID пользователя
            title: str - Название тренировки
            workout_date: datetime - Дата тренировки
            notes: str - Дополнительные сведения о тренировке
        Возвращает:
            None
        Исключения:
            ValueError: Если входные параметры некорректны
            TypeError: Если типы данных параметров не соответствуют ожидаемым
            SQLAlchemyError: При возникновении ошибок при работе с базой данных
        """
        
        workout_date = datetime.strptime(workout_date, '%Y-%m-%d')
        WorkoutValidate.add_workout_validate(
                    user_id,
                    title,
                    workout_date,
                    notes,
                    workout_type)
        
        try:
            new_workout = Workout(
                user_id=user_id,
                title=title,
                workout_date=workout_date,
                notes=notes,
                workout_type=workout_type
            )
            db.session.add(new_workout)
            db.session.commit()
            logger.info(f'Successfully added new workout: user_id={user_id}')
            logger.info(f'title={title}, date={workout_date}, type={workout_type}')
        except Exception as error:
            db.session.rollback()
            logger.error(f'Failed to add workout: {error}')
            raise SQLAlchemyError

    @staticmethod
    def get_all_user_workouts(user_id):
        """
        Получение списка всех тренировок.
        Аргументы:
            user_id: int - ID пользователя
        Возвращает:
            wokouts: List[dict] - Список всех тренировок пользователя в json формате
        Исключения:
            ValueError: Если входные параметры некорректны
            TypeError: Если типы данных параметров не соответствуют ожидаемым
            SQLAlchemyError: При возникновении ошибок при работе с базой данных
        """
        
        try:
            workouts = Workout.query.filter_by(user_id=user_id).all()
            workouts = [workout.to_dict(['id', 'title', 'workout_date']) for workout in workouts]
            logger.info(f'Successfully got workouts from database')
        except Exception as error:
            logger.error(f'Failed to get data from database {error}')
            raise SQLAlchemyError
        
        return workouts
    
    @staticmethod
    def get_workout(user_id, workout_id):
        """
        Получение информации о конкретной тренировоке.
        Аргументы:
            user_id: int - ID пользователя
            workout_id: int - ID тренировки
        Возвращает:
            wokout: dict - Список всех тренировок пользователя в json формате
        Исключения:
            ValueError: Если входные параметры некорректны
            TypeError: Если типы данных параметров не соответствуют ожидаемым
            SQLAlchemyError: При возникновении ошибок при работе с базой данных
        """

        WorkoutValidate.workout_validate(workout_id)
        
        try:
            workout = Workout.query.filter_by(id=workout_id).first()
            logger.info(f'Successfully got workout from database')
        except Exception as error:
            logger.error(f'Failed to get data from database {error}')
            raise SQLAlchemyError
        
        if workout.user_id != int(user_id):
            logger.warning(f'Access denied for user_id: {user_id}')
            raise Forbidden
        
        workout = workout.to_dict()

        return workout
    
    @staticmethod
    def delete_workout(user_id, workout_id):
        """
        Получение информации о конкретной тренировоке.
        Аргументы:
            user_id: int - ID пользователя
            workout_id: - тренировки
        Возвращает:
            None
        Исключения:
            ValueError: Если входные параметры некорректны
            TypeError: Если типы данных параметров не соответствуют ожидаемым
            SQLAlchemyError: При возникновении ошибок при работе с базой данных
        """
        
        WorkoutValidate.workout_validate(workout_id)
        
        try:
            workout = Workout.query.filter_by(id=workout_id).first()
        except Exception as error:
            db.session.rollback()
            logger.error(f'Failed to delete workout: {error}')
            raise SQLAlchemyError
            
        if workout.user_id != int(user_id):
            logger.warning(f'Access denied for user_id: {user_id}')
            raise Forbidden
        
        try:
            db.session.delete(workout)
            db.session.commit()
            logger.info(f'Successfully delete workout from database')
        except Exception as error:
            db.session.rollback()
            logger.error(f'Failed to delete workout: {error}')
            raise SQLAlchemyError
        