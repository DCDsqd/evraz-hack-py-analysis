import zipfile
import os

def handle_zip_file(file_path: str):
    """
    Распаковывает .zip файл и возвращает структуру файлов и путь к распакованной папке.
    """
    extract_path = f"extracted/{os.path.basename(file_path).replace('.zip', '')}"

    try:
        # Распаковываем архив
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        # Получаем структуру директорий
        structure = get_directory_structure(extract_path)

        return extract_path, structure

    except zipfile.BadZipFile:
        raise Exception("Невалидный .zip файл.")
    except Exception as e:
        raise Exception(f"Ошибка при распаковке архива: {str(e)}")

def get_directory_structure(root_dir: str) -> str:
    """
    Получает структуру директорий и файлов в виде строки с отступами.
    :param root_dir: Путь к корневой директории.
    :return: Строка, представляющая структуру файлов и папок.
    """
    structure = ""
    for root, dirs, files in os.walk(root_dir):
        level = root.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        structure += f"{indent}{os.path.basename(root)}/\n"
        for f in files:
            structure += f"{indent}    {f}\n"
    return structure
