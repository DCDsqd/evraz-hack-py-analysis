from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf_report(model_output: dict, structure: str, output_pdf_path="generated_report.pdf"):
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica", 10)

    y_position = height - 40

    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y_position, "PDF Отчет: Результаты обработки данных")
    y_position -= 20

    c.setFont("Helvetica", 10)
    c.drawString(40, y_position, f"Структура файлов: \n{structure}")
    y_position -= 20

    c.drawString(40, y_position, f"Ответ от модели: \n{model_output}")
    
    c.save()
    return output_pdf_path
