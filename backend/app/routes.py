from fastapi import APIRouter, UploadFile, File, Form
from app.aws import upload_to_s3, extract_text_from_s3_file

router  = APIRouter()

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    s3_url = upload_to_s3(file)

    bucket_name = s3_url.split("//")[1].split(".s3")[0]
    key = s3_url.split(".com/")[1]

    extracted_text = extract_text_from_s3_file(bucket_name, key)

    return {
        "message": "Resume uploaded and parsed",
        "s3_url": s3_url,
        "extracted_text": extracted_text
    }

job_descriptions = {}

@router.post("/upload-job-description")
async def upload_job_description(user_id: str = Form(...), jd_text: str = Form(...)):
    job_descriptions[user_id] = jd_text
    return {
        "message": "Job description has been stored successfully ✅",
        "user_id": user_id,
        "stored_text_snippet": jd_text[:100] + "..."
    }


