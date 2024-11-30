import os
import time
import backend.src.evraz_api as evraz_api

def send_to_evraz(project_dir, structure):
	for root, dirs, files in os.walk(project_dir):
		for file in files:
			file_path = os.path.join(root, file)
			message = f'Файл {file_path}\n'
			with open(file_path, 'r', encoding="utf-8") as f:
				read_data = f.read()
				evraz_api.generate_response(read_data, message)
				time.sleep(0.3)