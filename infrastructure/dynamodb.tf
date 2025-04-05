resource "aws_dynamodb_table" "resume_data" {
  name           = "resume-optimizer-data"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "user_id"
  range_key      = "resume_id"

  attribute {
    name = "user_id"
    type = "S"
  }

  attribute {
    name = "resume_id"
    type = "S"
  }

  tags = {
    Name        = "ResumeOptimizerTable"
    Environment = "dev"
  }
}
