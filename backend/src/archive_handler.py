from io import BytesIO
import os
import uuid
import zipfile
from datetime import datetime


def parse_archive(archive_content: bytes, root_dir: str = "extracted_files"):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    unique_dir = f"{timestamp}_{uuid.uuid4()}"
    
    extract_path = os.path.join(root_dir, unique_dir)

    try:
        os.makedirs(extract_path, exist_ok=True)

        with zipfile.ZipFile(BytesIO(archive_content)) as archive:
            archive.extractall(extract_path)

            structure = get_directory_structure(extract_path)

            return extract_path, structure

    except zipfile.BadZipFile:
        raise Exception("Bad zip file")
    except Exception as e:
        raise Exception(f"Error extracting archive: {str(e)}")


def get_directory_structure(root_dir: str) -> str:
    structure = ""
    for root, dirs, files in os.walk(root_dir):
        level = root.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        structure += f"{indent}{os.path.basename(root)}/\n"

        for f in files:
            structure += f"{indent}    {f}\n"
    return structure
