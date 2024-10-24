import os
from fastapi import UploadFile
from app.config.file import UPLOAD_FOLDER
from app.api.services.helper.file import validate_file

class UploadService():

    def __init__(self):
        pass

    def validate_file(self, file: UploadFile, allowed_extensions=None):
        if allowed_extensions:
            return validate_file(file, allowed_extensions)
        return validate_file(file)

    async def save_file(self, file: UploadFile) -> str:
        file_location = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_location, "wb") as f:
            f.write(await file.read())
        return file_location
