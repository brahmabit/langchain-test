from fastapi import HTTPException, UploadFile
from fastapi.responses import JSONResponse

from app.config.file import MAX_FILE_SIZE, ALLOWED_EXTENSIONS

def validate_file(file: UploadFile, allowed_extensions=ALLOWED_EXTENSIONS, max_file_size=MAX_FILE_SIZE):
    if not file.filename.split(".")[-1].lower() in allowed_extensions:
        raise HTTPException(
            status_code=400, detail=f"File type not allowed: {file.filename}. Only PDF/JSON file is allowed."
        )
    if file.size > max_file_size:
        raise HTTPException(
            status_code=413, detail=f"File too large. Max size is {max_file_size} bytes."
        )