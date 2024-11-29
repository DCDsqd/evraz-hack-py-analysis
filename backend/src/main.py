import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from backend.src.archive_handler import parse_archive

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# Эндпоинт для загрузки архива (любого типа)
@app.post("/upload-archive/")
async def upload_archive(file: UploadFile = File(...)):
    try:
        # Чтение архива из памяти
        archive_content = await file.read()

        # Парсим структуру архива
        structure = parse_archive(archive_content)

        return {"structure": structure}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Эндпоинт для загрузки исходного кода (Python, C# или TypeScript)
@app.post("/upload-code/")
async def upload_code(file: UploadFile = File(...)):
    try:
        # Прочитать файл с кодом
        code_content = await file.read()
        code_path = os.path.join("uploaded_code", file.filename)
        os.makedirs(os.path.dirname(code_path), exist_ok=True)

        with open(code_path, 'wb') as f:
            f.write(code_content)  # Сохранить файл с кодом

        return {"message": f"File '{file.filename}' uploaded successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
