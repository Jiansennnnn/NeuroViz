import os


current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
UPLOAD_LANDING_FOLDER = current_dir

## Extention handdle
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
