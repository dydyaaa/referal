from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.workout_service import Calendar
from werkzeug.exceptions import Forbidden


workout_bp = Blueprint('workout', __name__)

@workout_bp.route('/add_workout', methods=['POST'])
@jwt_required()
def add_workout():
    data = request.get_json()
    user_id = get_jwt_identity()

    title = data.get('title')
    workout_date = data.get('workout_date')
    notes = data.get('notes')
    workout_type = data.get('workout_type', 'regular workout')
    
    try:
        Calendar.add_workout(user_id, title, workout_date, notes, workout_type)
    except ValueError as error:
        return jsonify({'error': f'{error}'}), 400
    except TypeError as error:
        return jsonify({'error': f'{error}'}), 400
    
    return jsonify({'workout': "created"}), 201

@workout_bp.route('/get_all_user_workouts', methods=['GET'])
@jwt_required()
def get_all_user_workouts():

    user_id = get_jwt_identity()
    workouts = Calendar.get_all_user_workouts(user_id)
    
    return jsonify({'workouts': workouts}), 200

@workout_bp.route('/get_workout/<int:workout_id>', methods=['GET'])
@jwt_required()
def get_workout(workout_id):
    
    user_id = get_jwt_identity()

    try:
        workout = Calendar.get_workout(user_id, workout_id)
    except TypeError as error:
        return jsonify({'error': f'{error}'}), 400
    except Forbidden:
        return jsonify({'error': 'Access denied'}), 403
        
    return jsonify({'workout': workout}), 200

@workout_bp.route('/delete_workout/<int:workout_id>', methods=['DELETE'])
@jwt_required()
def delete_workout(workout_id):
    
    user_id = get_jwt_identity()

    try:
        Calendar.delete_workout(user_id, workout_id)
    except TypeError as error:
        return jsonify({'error': f'{error}'}), 400
    except Forbidden:
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify({'workout': 'deleted'}), 200

from flask import render_template_string
import hmac
import hashlib
import time
BOT_TOKEN = '6840735329:AAEUloVHprQ359KieM1tChYeMhsReJXKdSQ'

@workout_bp.route('/test')
def index():
    return render_template_string('''
        <h1>Авторизация через Telegram</h1>
        <script async src="https://telegram.org/js/telegram-widget.js?22"
                data-telegram-login="evdakimoff_bot"
                data-size="large"
                data-onauth="onTelegramAuth(user)"
                data-request-access="write"></script>
        <script>
            function onTelegramAuth(user) {
                fetch('/workout/telegram_callback', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(user)
                }).then(response => response.json())
                  .then(data => alert(data.message));
            }
        </script>
    ''')
    
@workout_bp.route('/telegram_callback', methods=['POST'])
def telegram_callback():
    data = request.get_json()

    # Проверка подлинности данных
    if not verify_telegram_data(data):
        return {'message': 'Ошибка авторизации'}, 403

    # Данные пользователя из Telegram
    user_id = data['id']
    first_name = data.get('first_name', '')
    username = data.get('username', '')

    # Здесь вы можете привязать Telegram ID к аккаунту на сайте
    # Например, сохранить в базе данных
    print(f"Пользователь авторизован: ID={user_id}, Имя={first_name}, Username={username}")

    return {'message': f'Добро пожаловать, {first_name}!'}

def verify_telegram_data(data):
    received_hash = data.get('hash')
    auth_date = data.get('auth_date')

    # Проверяем, что данные свежие (например, не старше 24 часов)
    if int(time.time()) - int(auth_date) > 86400:
        return False

    # Формируем строку для проверки
    data_check_string = '\n'.join([f'{k}={v}' for k, v in sorted(data.items()) if k != 'hash'])
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return computed_hash == received_hash