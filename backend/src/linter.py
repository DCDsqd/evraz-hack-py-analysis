import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


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

    trimmed_logs = []
    for line in logs.split('\n'):
        if base_path in line:
            line = line.replace(base_path, '')
        trimmed_logs.append(line)
    return '\n'.join(trimmed_logs)

def generate_pdf_report(base_path: str, lint_results: str, language: str, output_pdf_path: str = "linter_report.pdf"):
    max_line_length = 115
    base_path += "\evraz-hack-py-analysis"
    lint_results = trim_logs(lint_results, base_path)

    lines = []
    for line in lint_results.split('\n'):
        while len(line) > max_line_length:
            lines.append(line[:max_line_length])
            line = line[max_line_length:]
        lines.append(line)

    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica", 10)

    y_position = height - 40

    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y_position, f"Репорт умного линтера - {language.capitalize()}")
    y_position -= 20

    c.setFont("Helvetica", 10)
    for line in lines:
        if y_position < 40:
            c.showPage()
            c.setFont("Helvetica", 10)
            y_position = height - 40

        c.drawString(40, y_position, line)
        y_position -= 12

    c.save()
    return output_pdf_path
