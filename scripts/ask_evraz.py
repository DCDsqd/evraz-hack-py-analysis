import requests

API_URL = "http://84.201.152.196:8020/v1"
API_KEY = "Nmg7hPuSdKsluqNiBBzwL9Stz5JKGEx4"

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}


def generate_response(model_name, user_message):
    data = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": "отвечай на русском языке"
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
    user_message = input("Введите ваш вопрос модели: ")
    generate_response('mistral-nemo-instruct-2407', user_message)


if __name__ == "__main__":
    main()
