запуск сервера командой 

uvicorn backend.src.main:app --reload

Проверить работу по ссылке

http://127.0.0.1:8000/docs#/default/upload_archive_upload_archive_post


Задача хакатона: Разработайте приложение для автоматического Code Review
с помощью LLM и RAG.

### Установка и запуск проекта

pip install -r requirements.txt

uvicorn backend.src.main:app --reload


### Основной функционал проекта
1. Загрузка архивов с кодом для Python, C# и TypeScript.
2. Разархивирование и анализ структуры проекта.
3. Линтинг кода с помощью:

    Pylint для Python
    dotnet format для C#
    ESLint для TypeScript
    Автоматическое Code Review на основе LLM.
    Генерация отчетов в формате PDF с результатами анализа.

### Команда:
Магомедов Меджид - back, тест и своего рода девопс
Юрий Винник - back, мльщик
Владимир Матвеев - мльщик, тестировщик, капитан
Егор Мощенок - мльщик, тестировщик

### Архитектура 
backend/
│   prompts/
│       py.txt
│       c#.txt
│       ts_structure.txt
│   src/
│       archive_handler.py
│       linter.py
│       main.py
│       evraz_api.py
│       globals.py
scripts/
│   ask_evraz.py
uploaded_code/
requirements.txt
.gitignore

main.py: Основная точка входа.
archive_handler.py: Парсинг и структура архива.
linter.py: Запуск линтеров и генерация PDF-отчетов.
evraz_api.py: Взаимодействие с LLM API.

### Демо видео
https://drive.google.com/file/d/1mK_cutf5HMjDH6elFv6NEJbgEL9KFnow/view?usp=sharing
