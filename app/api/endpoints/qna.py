from fastapi import APIRouter, UploadFile, File, HTTPException, Request, Form
from typing import Annotated
from fastapi.responses import JSONResponse, FileResponse
from typing import List
import json

from app.api.services.vector import VectorService
from app.api.services.file import UploadService
import traceback

router = APIRouter(
     prefix="/v1/qna"
)

@router.post("/question")
async def ask_question(req: Request):
    input = await req.json()
    vector_service = VectorService()
    try:
        res = await vector_service.answer_question_for_document(input.get('questions'), input.get('filename'))
        #print(res)
        return JSONResponse(status_code=200, content={"Success": True, "Data": res})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/upload-file-question-file-answer")
async def answer_file_question_file(req: Request, question_file: UploadFile, document_file: UploadFile, download_as_file: Annotated[bool, Form()] = False):
    upload_service = UploadService()
    vector_service = VectorService()
    #validate question file
    upload_service.validate_file(question_file, {"json"})
    upload_service.validate_file(document_file, {"pdf", "json"})

    is_doc_file_processed = False
    is_question_file_processed = False

    #Doc file processing
    try:
        file_location = await upload_service.save_file(document_file)
        #print(file_location)
        vector_process = await vector_service.generate_embeddings(file_location)
        is_doc_file_processed = True
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"Success": False, "Data": str(e), "Source": "Document File"})
    
    #Question file processing
    #read the question file(json) list of questions
    try:
        question_file_content = await question_file.read()
        questions = json.loads(question_file_content)
        res = await vector_service.answer_question_for_document(questions)
        is_question_file_processed = True
    except Exception as e:
        return JSONResponse(status_code=500, content={"Success": False, "Data": str(e), "Source": "Question File"})
    
    if is_doc_file_processed and is_question_file_processed:
        print("Download as file: ", download_as_file)
        if download_as_file or download_as_file == "true" or download_as_file == "True":
            response_content = json.dumps(res)
            response_filename = "response.json"
            with open(response_filename, "w") as response_file:
                response_file.write(response_content)
            return FileResponse(response_filename, media_type='application/octet-stream', filename=response_filename)
        return JSONResponse(status_code=200, content={"Success": True, "Data": res})
    else:
        return JSONResponse(status_code=500, content={"Success": False, "Data": "Processing failed."})

    




