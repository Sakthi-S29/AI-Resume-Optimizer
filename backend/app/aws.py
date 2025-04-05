import boto3
import uuid
from fastapi import UploadFile
import os

BUCKET_NAME = "resume-optimizer-381ec673"

s3 = boto3.client("s3")

def upload_to_s3(file: UploadFile) -> str:
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"resumes/{uuid.uuid4()}.{file_extension}"

    s3.upload_fileobj(file.file, BUCKET_NAME, unique_filename)

    return f"https://{BUCKET_NAME}.s3.amazonaws.com/{unique_filename}"