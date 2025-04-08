resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "resume_storage" {
  bucket = "resume-optimizer-${random_id.suffix.hex}"
  force_destroy = true

  tags = {
    Name        = "resume-optimizer-bucket"
    Environment = "dev"
  }
}

resource "aws_s3_bucket_public_access_block" "block_public" {
  bucket = aws_s3_bucket.resume_storage.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

output "s3_bucket_name" {
  value = aws_s3_bucket.resume_storage.bucket
  description = "The name of the created S3 bucket"
}