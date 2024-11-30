import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from enum import Enum
from backend.src.archive_handler import parse_archive
from backend.src.linter import lint_python, lint_typescript, lint_csharp, generate_pdf_report

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
        project_dir, structure = parse_archive(archive_content)
        print(project_dir)
        # Линтинг кода в зависимости от языка
        if language == "python":
            lint_results = lint_python(project_dir)
        elif language == "csharp":
            lint_results = lint_csharp(project_dir)
        elif language == "typescript":
            lint_results = lint_typescript(project_dir)
        else:
            raise HTTPException(status_code=400, detail="Unsupported language")

        # Генерация PDF отчета
        pdf_path = generate_pdf_report(project_dir, lint_results, language)

        return {"message": "Archive uploaded, extracted, and linted successfully!",
                "structure": structure,
                "pdf_report": pdf_path}
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
