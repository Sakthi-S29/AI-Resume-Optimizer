from fastapi import APIRouter, UploadFile, File
from app.aws import upload_to_s3

router  = APIRouter()

@router.get("/ping")
def ping():
    return {"pong": True}

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    file_url = upload_to_s3(file)
    return {"message": "Resume uploaded successfully ✅", "s3_url": file_url}