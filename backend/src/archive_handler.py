import zipfile
import os
import uuid
from io import BytesIO


def parse_archive(archive_content: bytes, root_dir: str = "extracted_files"):
    """
    Распаковывает архив в уникальную папку, парсит структуру и возвращает строку с иерархией файлов и папок.

    :param archive_content: Содержимое архива в байтах.
    :param root_dir: Корневая папка для извлечения файлов.
    :return: Строка, представляющая структуру архива.
    """
    # Генерация уникального идентификатора для каждой сессии
    unique_dir = str(uuid.uuid4())
    extract_path = os.path.join(root_dir, unique_dir)

    try:
        os.makedirs(extract_path, exist_ok=True)

        with zipfile.ZipFile(BytesIO(archive_content)) as archive:
            archive.extractall(extract_path)  # Извлекаем все файлы в уникальную папку

            # Получаем структуру файлов и директорий
            structure = get_directory_structure(extract_path)
            return structure

    except zipfile.BadZipFile:
        raise Exception("Bad zip file")
    except Exception as e:
        raise Exception(f"Error extracting archive: {str(e)}")


def get_directory_structure(root_dir: str, indent: str = "") -> str:
    """
    Рекурсивно обходит директорию и строит строку с её иерархией.

    :param root_dir: Путь к корневой директории.
    :param indent: Отступ для текущего уровня.
    :return: Строка с иерархией файлов и папок.
    """
    structure = ""
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path):
            structure += f"{indent}├── {item}/\n"
            structure += get_directory_structure(item_path, indent + "│   ")
        else:
            structure += f"{indent}├── {item}\n"
    return structure
