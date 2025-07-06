import logging
from flask import current_app
from datetime import datetime, date
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models.user import User
from app.models.referral import Referral
from app.models.foodlog import FoodLog


logger = logging.getLogger('app.nutrition')

class NutritionService:
    @staticmethod
    def add_food_log(user_id, meal_type, calories, protein, fat, carbs, weight_grams, description=None, date=None):
        """
        Добавление записи о приеме пищи.
        Аргументы:
            user_id: int - ID пользователя
            meal_type: str - Тип приема пищи (завтрак, обед, ужин и т.д.)
            calories: float - Количество калорий
            protein: float - Количество белков
            fat: float - Количество жиров
            carbs: float - Количество углеводов
            weight_grams: float - Вес продукта в граммах
            description: str - Описание продукта (необязательно)
        Возвращает:
            dict - Словарь с информацией о добавленной записи
        Исключения:
            SQLAlchemyError - Ошибка при добавлении новой записи
        """
        try:
            food_log = FoodLog(
                user_id=user_id,
                meal_type=meal_type,
                calories=calories,
                protein=protein,
                fat=fat,
                carbs=carbs,
                weight_grams=weight_grams,
                description=description,
                date=date or datetime.now()
            )
            db.session.add(food_log)
            db.session.commit()
            return food_log.to_dict()
        except SQLAlchemyError as error:
            db.session.rollback()
            logger.error(f'Failed to add food log: {error}')
            raise SQLAlchemyError('Ошибка при добавлении записи о приеме пищи')
        

    def get_food_logs(user_id, date_str):
        """
        Получение списка записей о приеме пищи для текущего пользователя в конкретную дату.
        Аргументы:
            user_id: int - ID пользователя
            date: datetime - Дата для фильтрации записей
        Возвращает:
            list - Список словарей с информацией о приемах пищи
        Исключения:
            SQLAlchemyError - Ошибка при получении записей
        """
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            food_logs = FoodLog.query.filter_by(user_id=user_id, date=date).all()
            return [log.to_dict() for log in food_logs]
        except SQLAlchemyError as error:
            logger.error(f'Failed to get food logs: {error}')
            raise SQLAlchemyError('Ошибка при получении записей о приеме пищи')
        
    
    def get_today_macros_percent(user_id):
        logs = FoodLog.query.filter_by(user_id=user_id, date=date.today()).all()

        total_protein = sum(log.protein for log in logs)
        total_fat = sum(log.fat for log in logs)
        total_carbs = sum(log.carbs for log in logs)

        total_macros = total_protein + total_fat + total_carbs

        if total_macros == 0:
            return {
                'protein_percent': 33,
                'fat_percent': 33,
                'carbs_percent': 34
            }
        
        protein_percent = (total_protein / total_macros) * 100
        fat_percent = (total_fat / total_macros) * 100
        carbs_percent = (total_carbs / total_macros) * 100

        return {
            'protein_percent': round(protein_percent, 2),
            'fat_percent': round(fat_percent, 2),
            'carbs_percent': round(carbs_percent, 2)
        }