from io import BytesIO
import os
import uuid
import zipfile
from datetime import datetime


def parse_archive(archive_content: bytes, root_dir: str = "extracted_files"):
    """
    Распаковывает архив в уникальную папку, парсит структуру и возвращает строку с иерархией файлов и папок.

    :param archive_content: Содержимое архива в байтах.
    :param root_dir: Корневая папка для извлечения файлов.
    :return: Путь к извлеченной папке и строку с иерархией файлов и папок.
    """

    # Получаем текущую дату и время и форматируем их
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Создаем уникальную папку для каждого запроса, добавляя таймстамп
    unique_dir = f"{timestamp}_{uuid.uuid4()}"
    
    extract_path = os.path.join(root_dir, unique_dir)

    try:
        # Создаем директорию для извлечения
        os.makedirs(extract_path, exist_ok=True)

        # Открываем и распаковываем архив
        with zipfile.ZipFile(BytesIO(archive_content)) as archive:
            archive.extractall(extract_path)  # Извлекаем все файлы в уникальную папку

            # Получаем структуру директорий
            structure = get_directory_structure(extract_path)

            # Возвращаем путь к извлеченной папке и структуру
            return extract_path, structure

    except zipfile.BadZipFile:
        raise Exception("Bad zip file")
    except Exception as e:
        raise Exception(f"Error extracting archive: {str(e)}")


def get_directory_structure(root_dir: str) -> str:
    """
    Получает структуру директорий и файлов в виде строки с отступами.
    :param root_dir: Путь к корневой директории.
    :return: Строка, представляющая структуру файлов и папок.
    """
    structure = ""
    for root, dirs, files in os.walk(root_dir):
        # Определяем уровень вложенности
        level = root.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        structure += f"{indent}{os.path.basename(root)}/\n"

        # Добавляем файлы на текущем уровне
        for f in files:
            structure += f"{indent}    {f}\n"
    return structure
