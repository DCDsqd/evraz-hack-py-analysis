from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import zipfile
import os
from io import BytesIO

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/upload-project-archive/")
async def upload_archive(file: UploadFile = File(...)):
    # Проверка на тип файла
    if file.content_type != 'application/zip':
        return JSONResponse(content={"error": "File is not a zip archive"}, status_code=400)

    try:
        # Чтение архива из памяти
        zip_content = await file.read()
        with zipfile.ZipFile(BytesIO(zip_content)) as archive:
            archive.extractall("extracted_files")  # Извлечь содержимое архива
            return {"message": "Archive uploaded and extracted successfully!"}

    except zipfile.BadZipFile:
        return JSONResponse(content={"error": "Bad zip file"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)