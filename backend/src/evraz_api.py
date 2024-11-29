import requests

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


def generate_response(user_message, system_message, model_name=MODEL_NAME):
    data = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": system_message
            },
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
        # Извлечение и вывод ответа от ассистента
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


def main():


if __name__ == "__main__":
    main()
