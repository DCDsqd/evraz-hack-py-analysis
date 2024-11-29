import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
from fpdf import FPDF


# Функция для линтинга Python кода
def lint_python(project_dir: str) -> str:
    try:
        result = subprocess.run(
            ['pylint', '--output-format=text', project_dir],
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception as e:
        return f"Error linting Python project: {str(e)}"


# Функция для линтинга C# кода
def lint_csharp(project_dir: str) -> str:
    try:
        result = subprocess.run(
            ['dotnet', 'format', '--check'],
            cwd=project_dir,
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception as e:
        return f"Error linting C# project: {str(e)}"


# Функция для линтинга TypeScript кода
def lint_typescript(project_dir: str) -> str:
    try:
        result = subprocess.run(
            ['eslint', '--format', 'unix', '--ext', '.ts', project_dir],
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception as e:
        return f"Error linting TypeScript project: {str(e)}"



def generate_pdf_report(lint_results: str, language: str) -> str:
    """
    Генерирует PDF с отчетом о линтинге.
    :param lint_results: Строка с результатами линтинга.
    :param language: Язык программирования (для заголовка).
    :return: Путь к сохраненному PDF файлу.
    """
    # Создаем объект PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Заголовок отчета
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(10, 10, f"Linter Report - {language.capitalize()} Project", ln=True, align='C')

    # Текст отчета
    pdf.ln(10)  # Добавляем отступ после заголовка
    pdf.set_font('Arial', '', 12)

    # Разбиваем результат линтинга на строки и добавляем их в PDF
    lines = lint_results.splitlines()

    for line in lines:
        # Добавляем строку в PDF с автоматическим переносом
        pdf.multi_cell(0, 10, line)

    # Сохраняем PDF в файл
    pdf_output_path = "lint_report.pdf"
    pdf.output(pdf_output_path)

    return pdf_output_path
