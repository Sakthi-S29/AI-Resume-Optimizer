import boto3
import uuid
from fastapi import UploadFile
import os

BUCKET_NAME = "resume-optimizer-5022f4e4"

s3 = boto3.client("s3")

def upload_to_s3(file: UploadFile) -> str:
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"resumes/{uuid.uuid4()}.{file_extension}"

    s3.upload_fileobj(file.file, BUCKET_NAME, unique_filename)

    return f"https://{BUCKET_NAME}.s3.amazonaws.com/{unique_filename}"

def extract_text_from_s3_file(s3_bucket: str, s3_key: str) -> str:
    textract = boto3.client("textract")

    response = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': s3_bucket,
                'Name': s3_key
            }
        }
    ) 

    extracted_text_from_s3_file = ""
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            extracted_text_from_s3_file += item['Text'] + "\n"

    return extracted_text_from_s3_file