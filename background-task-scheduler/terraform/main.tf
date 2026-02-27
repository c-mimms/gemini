terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "site" {
  bucket = "gemini-design-background-task-scheduler"
}

resource "aws_s3_bucket_website_configuration" "site" {
  bucket = aws_s3_bucket.site.bucket

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_policy" "site" {
  bucket = aws_s3_bucket.site.bucket
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.site.arn}/*"
      }
    ]
  })
}

resource "aws_s3_object" "index" {
  bucket       = aws_s3_bucket.site.bucket
  key          = "index.html"
  source       = "../index.html"
  content_type = "text/html"
  etag         = filemd5("../index.html")
}

resource "aws_s3_object" "style" {
  bucket       = aws_s3_bucket.site.bucket
  key          = "style.css"
  source       = "../style.css"
  content_type = "text/css"
  etag         = filemd5("../style.css")
}

resource "aws_s3_object" "script" {
  bucket       = aws_s3_bucket.site.bucket
  key          = "script.js"
  source       = "../script.js"
  content_type = "application/javascript"
  etag         = filemd5("../script.js")
}

output "website_url" {
  value = "http://${aws_s3_bucket_website_configuration.site.website_endpoint}"
}
