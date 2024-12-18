import requests
import json


API_URL = "http://84.201.152.196:8020/v1"
API_KEY = "Nmg7hPuSdKsluqNiBBzwL9Stz5JKGEx4"

MODEL_NAME = 'mistral-nemo-instruct-2407'

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}


def greeting():
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        print(" Приветственное сообщение получено успешно.")
    else:
        print(" Ошибка получения приветственного сообщения:", response.content)


def get_models():
    response = requests.get(f"{API_URL}/models", headers=headers)
    if response.status_code == 200:
        models = response.json()
        print(" Доступные модели:", models)
        return models
    else:
        print(" Ошибка получения списка моделей:", response.content)
        return []


def get_default_context():
    static_context_arr = {}
    try:
        with open('static_context.json', 'r', encoding='utf-8') as f:
            static_context_data = json.load(f)
            static_context_arr = static_context_data.get('static_context', {})
    except FileNotFoundError:
        print("Файл static_context.json не найден.")
    except json.JSONDecodeError:
        print("Ошибка декодирования JSON из файла static_context.json.")

    return static_context_arr


def generate_response(user_message, system_message, static_context_arr=None, model_name=MODEL_NAME):
    if not static_context_arr:
        static_context_arr = get_default_context()

    data = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": system_message
            },
            static_context_arr,
            {
                "role": "user",
                "content": user_message
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.3
    }

    response = requests.post(f"{API_URL}/completions", json=data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            message = result['choices'][0].get('message', {})
            if message.get('role') == 'assistant':
                content = message.get('content', '')
                print("Ответ от ассистента:", content)
            else:
                print("Неверная структура ответа (отсутствует сообщение от ассистента).")
        else:
            print("Неверная структура ответа (отсутствуют выборы).")
    else:
        print("Ошибка генерации ответа:", response.content)
