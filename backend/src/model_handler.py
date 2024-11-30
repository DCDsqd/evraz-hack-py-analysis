import requests

API_URL = "http://your_model_api_url"
API_KEY = "YOUR_API_KEY"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def generate_model_response(extracted_files_path: str):
    """
    Отправляет данные в модель и получает ответ.
    """
    data = {
        "input": extracted_files_path  # здесь может быть специфическая логика передачи данных в модель
    }
    response = requests.post(f"{API_URL}/process", json=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Ошибка при получении ответа от модели: {response.content}")
