import os

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BASE_DIR = os.path.join(APP_ROOT, 'app')
UPLOAD_FOLDER = os.path.join(BASE_DIR, "upload")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

MAX_FILE_SIZE = 15 * 1024 * 1024  
ALLOWED_EXTENSIONS = {"pdf", "json"}