import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


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

def trim_logs(logs: str, base_path: str) -> str:
    """
    Убирает лишнюю часть пути из логов, оставляя относительный путь.

    :param logs: Логи линтера как строка.
    :param base_path: Базовый путь, который нужно удалить из логов.
    :return: Отредактированные логи.
    """
    trimmed_logs = []
    for line in logs.split('\n'):
        # Если строка содержит базовый путь, удаляем его
        if base_path in line:
            line = line.replace(base_path, '')
        trimmed_logs.append(line)
    return '\n'.join(trimmed_logs)

def generate_pdf_report(base_path: str, lint_results: str, language: str, output_pdf_path: str = "linter_report.pdf"):
    """
    Генерирует PDF отчет с результатами линтинга, добавляя автоперенос строк для длинных сообщений.

    :param lint_results: Результаты линтинга как строка.
    :param language: Язык проекта (python, csharp, typescript).
    :param output_pdf_path: Путь для сохранения итогового PDF.
    """
    # Максимальная длина строки в символах перед переносом
    max_line_length = 115
    base_path += "\evraz-hack-py-analysis"
    lint_results = trim_logs(lint_results, base_path)

    # Разбиваем результат на строки, если они длиннее max_line_length
    lines = []
    for line in lint_results.split('\n'):
        while len(line) > max_line_length:
            lines.append(line[:max_line_length])
            line = line[max_line_length:]
        lines.append(line)

    # Создание PDF
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter  # Размер страницы

    # Шрифт и размер шрифта
    c.setFont("Helvetica", 10)

    # Начальная позиция для текста
    y_position = height - 40  # Отступ сверху от края страницы

    # Добавляем заголовок
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y_position, f"Linter Report - {language.capitalize()} Project")
    y_position -= 20  # Отступ после заголовка

    # Добавляем результаты линтинга
    c.setFont("Helvetica", 10)
    for line in lines:
        # Если строка не помещается на странице, переходим на новую
        if y_position < 40:
            c.showPage()
            c.setFont("Helvetica", 10)
            y_position = height - 40

        c.drawString(40, y_position, line)
        y_position -= 12  # Отступ между строками

    # Сохраняем PDF
    c.save()
    return output_pdf_path
