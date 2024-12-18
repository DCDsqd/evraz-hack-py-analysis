import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from backend.src.archive_handler import handle_zip_file
from backend.src.model_handler import generate_model_response
from backend.src.pdf_generator import generate_pdf_report
from backend.globals import PROJECT_DIR

TOKEN = "YOUR_BOT_API_TOKEN"
DOWNLOAD_PATH = os.path.join(PROJECT_DIR, "downloads/")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Отправьте мне .zip файл, и я создам PDF отчет.")

def handle_document(update: Update, context: CallbackContext):
    file = update.message.document
    file_name = file.file_name

    if file_name.endswith(".zip"):
        new_file = file.get_file()
        file_path = os.path.join(DOWNLOAD_PATH, file_name)
        new_file.download(file_path)
        update.message.reply_text(f"Загружен файл: {file_name}")

        try:
            extracted_files_path, structure = handle_zip_file(file_path)
            model_output = generate_model_response(extracted_files_path)
            pdf_path = generate_pdf_report(model_output, structure)
            update.message.reply_text("Генерация PDF завершена, отправляю файл...")
            update.message.reply_document(open(pdf_path, 'rb'))

        except Exception as e:
            update.message.reply_text(f"Произошла ошибка при обработке файла: {str(e)}")
    else:
        update.message.reply_text("Пожалуйста, отправьте .zip файл.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(MessageHandler(Filters.document.mime_type("application/zip"), handle_document))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
