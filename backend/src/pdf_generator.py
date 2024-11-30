from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf_report(model_output: dict, structure: str, output_pdf_path="generated_report.pdf"):
    """
    Генерирует PDF отчет на основе вывода модели и структуры данных.
    """
    # Создание PDF
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter  # Размер страницы

    # Шрифт и размер шрифта
    c.setFont("Helvetica", 10)

    # Начальная позиция для текста
    y_position = height - 40  # Отступ сверху от края страницы

    # Добавляем заголовок
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y_position, "PDF Отчет: Результаты обработки данных")
    y_position -= 20  # Отступ после заголовка

    # Добавляем структуру файлов
    c.setFont("Helvetica", 10)
    c.drawString(40, y_position, f"Структура файлов: \n{structure}")
    y_position -= 20  # Отступ после структуры

    # Добавляем результат работы модели
    c.drawString(40, y_position, f"Ответ от модели: \n{model_output}")
    
    # Сохраняем PDF
    c.save()
    return output_pdf_path
