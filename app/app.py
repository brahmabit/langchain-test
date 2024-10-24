from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api.endpoints.file import router as upload_router
from app.api.endpoints.qna import router as qna_router
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

#We could potentially seprate out this as well
app.include_router(upload_router)
app.include_router(qna_router)

@app.get("/")
def root():
    #maybe used  for heartbeat etc.
    return JSONResponse(status_code=200, content={"Success": True, "Service":"QnA Service running."})