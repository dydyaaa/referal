from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.nutrition_service import NutritionService
from datetime import datetime

nutrition_bp = Blueprint('nutrition', __name__)

@nutrition_bp.route('/add_food_log', methods=['POST'])
@jwt_required()
def add_food_log():
    """
    Добавление записи о приеме пищи.
    Аргументы:
        meal_type: str - Тип приема пищи (завтрак, обед, ужин и т.д.)
        calories: float - Количество калорий
        protein: float - Количество белков
        fat: float - Количество жиров
        carbs: float - Количество углеводов
        weight_grams: float - Вес продукта в граммах
        description: str - Описание продукта (необязательно)
    Возвращает:
        dict - Словарь с информацией о добавленной записи
    """
    user_id = get_jwt_identity()
    data = request.json

    try:
        food_log = NutritionService.add_food_log(
            user_id=user_id,
            meal_type=data.get('meal_type'),
            calories=data.get('calories'),
            protein=data.get('protein'),
            fat=data.get('fat'),
            carbs=data.get('carbs'),
            weight_grams=data.get('weight_grams'),
            description=data.get('description'),
            date=datetime.strptime(data.get('date'), "%Y-%m-%d").date()
        )
        return jsonify(food_log), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@nutrition_bp.route('/food_logs', methods=['GET'])
@jwt_required()
def get_food_logs():
    """
    Получение списка записей о приеме пищи для текущего пользователя в конкретную дату.
    Параметры запроса:
        date (str) - Дата в формате YYYY-MM-DD (опционально, по умолчанию - сегодня)
    Возвращает:
        list - Список словарей с информацией о приемах пищи
    """
    user_id = get_jwt_identity()
    date_str = request.args.get('date')

    try:
        food_logs = NutritionService.get_food_logs(user_id, date_str)
        return jsonify(food_logs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400