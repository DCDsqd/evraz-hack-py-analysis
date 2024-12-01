import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import FileResponse
from enum import Enum
from backend.src.archive_handler import parse_archive
from backend.src.linter import lint_python, lint_typescript, lint_csharp, generate_pdf_report
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

app = FastAPI()

NEURO_URL = "http://84.201.152.196:8020/v1/completions"
AUTHORIZATION = "Nmg7hPuSdKsluqNiBBzwL9Stz5JKGEx4"
MAX_TOKENS = 1000
MODEL = "mistral-nemo-instruct-2407"
TEMPERATURE = 0.3

MAX_WORKERS = 5


class Language(str, Enum):
    python = "python"
    csharp = "csharp"
    typescript = "typescript"



def send_request_to_neuro(prompt, file_content):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": file_content}
        ],
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE
    }
    headers = {
        "Authorization": AUTHORIZATION,
        "Content-Type": "application/json",
        "User-Agent": "insomnia/10.2.0"
    }
    response = requests.post(NEURO_URL, json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Neural network request failed: {response.text}")
    return response.json()["choices"][0]["message"]["content"]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/upload-archive")
async def upload_archive(
    file: UploadFile = File(...),
    language: Language = Query(..., description="Select the project language (python, csharp, typescript)")
):
    try:
        archive_content = await file.read()

        project_dir, structure = parse_archive(archive_content)

        if language == "python":
            lint_results = lint_python(project_dir)
        elif language == "csharp":
            lint_results = lint_csharp(project_dir)
        elif language == "typescript":
            lint_results = lint_typescript(project_dir)
        else:
            raise HTTPException(status_code=400, detail="Unsupported language")

        prompt_file_path = os.path.join("backend", "prompts", "py.txt")
        if not os.path.exists(prompt_file_path):
            raise HTTPException(status_code=500, detail="Prompt file for Python not found")
        with open(prompt_file_path, "r", encoding="utf-8") as f:
            py_prompt = f.read().strip()

        py_files = []
        for root, _, files in os.walk(project_dir):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                    py_files.append((file_path, file_content))

        results = []
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_file = {
                executor.submit(send_request_to_neuro, py_prompt, f"{file_path}\n\n{file_content}"): file_path
                for file_path, file_content in py_files
            }
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    response = future.result()
                    results.append(f"===========================\n{file_path}\n{response}\n===========================")
                except Exception as e:
                    results.append(f"===========================\n{file_path}\nError: {str(e)}\n===========================")

        combined_results = "\n".join(results)
        with open(prompt_file_path, "r", encoding="utf-8") as f:
            prompt = f.read().strip()
        print(111111111)
        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": structure}
            ],
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE
        }

        headers = {
            "Authorization": AUTHORIZATION,
            "Content-Type": "application/json",
            "User-Agent": "insomnia/10.2.0"
        }

        response = requests.post(NEURO_URL, json=payload, headers=headers)
        print(response)
        neural_response =  response.json()
        print(neural_response)
        if response.status_code == 200:
            neural_response = neural_response["choices"][0]["message"]["content"]
        else:
            neural_response = neural_response["error"]["message"]
        pdf_path = generate_pdf_report(project_dir, neural_response + "\n\n\n" + combined_results + "\n\n\n" + lint_results, language)

        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename="lint_report.pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.get("/download-report")
async def download_report(file_path: str):
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="application/pdf", filename=os.path.basename(file_path))


@app.post("/upload-code")
async def upload_code(
        file: UploadFile = File(...),
        language: Language = Query(..., description="Select the project language (python, csharp, typescript)")
):
    try:
        code_content = await file.read()
        code_path = f"uploaded_code/{language}/{file.filename}"
        os.makedirs(os.path.dirname(code_path), exist_ok=True)

        with open(code_path, 'wb') as f:
            f.write(code_content)

        return {"message": f"File '{file.filename}' uploaded successfully!", "language": language}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
