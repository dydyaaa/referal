from flask import Blueprint, request, jsonify
from app.services.chat_service import ChatService
from flask_jwt_extended import jwt_required, get_jwt_identity

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/ask', methods=['POST'])
@jwt_required()
def ask():
    """
    Обработчик для получения ответа на заданный вопрос.

    Аргументы:
    prompt (str): Текст вопроса, на который нужно получить ответ.

    Возвращает:
    JSON-ответ с ответом на вопрос.
    """
    data = request.get_json()
    prompt = data.get('prompt')
    user_id = get_jwt_identity()
    
    try:
        answer = ChatService.gigachat_answer(prompt, user_id)
        return jsonify({'answer': answer}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
