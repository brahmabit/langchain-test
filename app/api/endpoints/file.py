from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List

import traceback

from app.api.services.file import UploadService
from app.api.services.vector import VectorService

router = APIRouter(
     prefix="/v1/file"
)


@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    file_locations = []
    vector_processing = []
    upload_service = UploadService()
    vector_service = VectorService()

    for file in files:
        upload_service.validate_file(file)
        try:
            file_location = await upload_service.save_file(file)
            file_locations.append(file_location)
            vector_process = await vector_service.generate_embeddings(file_location)
            vector_processing.append(vector_process)
        except Exception as e:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(
        status_code=201,
        content={"Success": True, "Data": file_locations, "vector_processing": vector_processing},
    )

