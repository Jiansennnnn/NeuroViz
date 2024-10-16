import os


current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
UPLOAD_LANDING_FOLDER = current_dir

## Extention handdle
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# History Cleaner
target_file_path = os.path.join(current_dir, '..', 'util', 'empty_history.py')

SCRIPT_PATH = target_file_path

PORT_NO = 7777