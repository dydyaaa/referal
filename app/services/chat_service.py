import requests
import json
import urllib3
import uuid
from app.services.user_service import UserService

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ChatService():
    def get_access_token() -> str:
        """
        Функция, генерирующая access_token для Gigachat

        Возвращает:
        result (str): access_token
        """
        new_uuid = uuid.uuid4()
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        payload='scope=GIGACHAT_API_PERS'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': f'{new_uuid}',
        'Authorization': f'Basic N2Q2NWI5MTctOTY2My00ZTViLTgxNWQtYWIxZGE4OTk1NzFkOjQzYmJhZWI0LWQ5ODktNDc4Yi05MjY1LWRlZTNkYjA5OTA3Yg=='
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        response_json = response.json()
        result = response_json['access_token']
        return result

    def gigachat_answer(prompt: str, user_id) -> str:
        """
        Генерирует ответ с использованием модели Gigachat на основе заданного промпта.
        
        Аргументы:
        prompt (str): Текст промпта для генерации ответа.

        Возвращает:
        result (str): Сгенерированный ответ на основе промпта в виде строки.
        """
        user_data = ChatService.get_user_data(user_id)
        prompt = f'{user_data} {prompt}'

        access_token = ChatService.get_access_token()
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        payload = json.dumps({
            "model": "GigaChat",
            "messages": [
                {
                "role": "user",
                "content": f'{prompt}'
                }
            ],
            "temperature": 1,
            "top_p": 0.1,
            "n": 1,
            "stream": False,
            "max_tokens": 512,
            "repetition_penalty": 1
            })
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
            }
        
        try:
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
            response_json = response.json()
            result = response_json['choices'][0]['message']['content']
            return result
        except Exception as e:
            result = str(e)
            return result
    
    def get_user_data(user_id):
        """
        Получает данные пользователя по user_id.

        Аргументы:
        user_id (int): Идентификатор пользователя.

        Возвращает:
        str: Форматированная строка с данными пользователя.
        """
        user_data = UserService.get_user_info(user_id)  # Получаем ORM-объект UserProfile

        # Обрабатываем возможные None у activity_level (или других полей)
        activity_level = user_data.activity_level if user_data.activity_level else "не указан"

        data = (
            f'Привет, меня зовут {user_data.full_name}. Представь, что ты мой фитнес тренер. '
            f'Мой рост {user_data.height_cm} см, вес {user_data.weight_kg} кг. '
            f'Моя цель - {user_data.goal}. '
            f'Мой уровень активности - {activity_level}. '
            f'Ответь на мой вопрос, используя эти данные, но не задавая допольнительных вопросов:'
        )

        return data
