from fastapi import APIRouter, UploadFile, File, Form
from app.aws import upload_to_s3, extract_text_from_s3_file
from app.utils import score_resume_against_jd, store_score_in_dynamodb, get_score_history
from app.resume_generator import generate_resume

router  = APIRouter()

@router.post("/upload-resume")
async def upload_resume(resume: UploadFile = File(...)):
    s3_url = upload_to_s3(resume)

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


@router.post("/score-resume")
async def score_resume(user_id: str = Form(...), resume_text: str = Form(...)):
    jd_text = job_descriptions.get(user_id)
    if not jd_text:
        return {"error": "Job Description not found for this user."}
    
    score_result = score_resume_against_jd(resume_text, jd_text)
    print("DEBUG score_result:", score_result)
    store_score_in_dynamodb(user_id, resume_text, jd_text, score_result)
    return {
        "message": "ATS score has been calculated ✅",
        "score": score_result["score_percent"],
        "matched_keywords": score_result["matched_keywords"],
        "missing_keywords": score_result["missing_keywords"],
        "suggestions": score_result.get("suggestions", {})
    }

@router.get("/score-history/{user_id}")
def score_history(user_id: str):
    return get_score_history(user_id)

@router.get("/generate-resume")
def generate_sample_resume():
    resume = generate_resume(
        name="Sakthi Sharan Mahadevan",
        email="sakthisharanm@gmail.com",
        skills=["python", "aws", "docker", "fastapi"],
        education="Master of Applied Computer Science, Dalhousie University, 2026",
        certifications=["AWS Certified Cloud Practitioner"],
        projects=[
            {
                "title": "AI Resume Optimizer",
                "situation": "Users struggle to get interviews due to ATS failures.",
                "task": "Build a system to analyze and improve resume scores.",
                "action": "Used Python, FastAPI, S3, DynamoDB, React, Tailwind.",
                "result": "Improved resume match score by up to 40%."
            },
            {
                "title": "Community Smells Detector",
                "situation": "GitHub repos suffer from poor team collaboration.",
                "task": "Detect anti-patterns like Radio Silence or Siloing.",
                "action": "Built a web tool on top of CSDetector using GitHub API.",
                "result": "Helped teams identify collaboration issues proactively."
            }
        ]
    )
    return resume

