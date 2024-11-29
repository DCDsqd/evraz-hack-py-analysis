from fastapi import FastAPI, File, UploadFile, HTTPException
import os
import zipfile
from io import BytesIO
from enum import Enum
from backend.src.archive_handler import parse_archive

app = FastAPI()


# Enum для выбора языка проекта
class Language(str, Enum):
    python = "python"
    csharp = "csharp"
    typescript = "typescript"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/upload-archive/")
async def upload_archive(
        file: UploadFile = File(...),
        language: Language = Query(..., description="Select the project language (python, csharp, typescript)")
):
    try:
        # Чтение архива из памяти
        archive_content = await file.read()

        # Парсим структуру архива с уникальной папкой для каждого запроса
        structure = parse_archive(archive_content)

        # Здесь можно добавить обработку или сохранение информации о языке
        return {
            "message": "Archive uploaded and extracted successfully!",
            "language": language,
            "structure": structure
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/upload-code/")
async def upload_code(
        file: UploadFile = File(...),
        language: Language = Query(..., description="Select the project language (python, csharp, typescript)")
):
    try:
        # Прочитать файл с кодом
        code_content = await file.read()
        code_path = f"uploaded_code/{language}/{file.filename}"
        os.makedirs(os.path.dirname(code_path), exist_ok=True)

        with open(code_path, 'wb') as f:
            f.write(code_content)

        return {"message": f"File '{file.filename}' uploaded successfully!", "language": language}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
