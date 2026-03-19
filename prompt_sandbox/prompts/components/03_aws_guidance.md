## AWS Cost & Architecture Guidelines

When tasked with deploying applications or writing infrastructure code (AWS CDK, Terraform, Serverless, boto3), you MUST strictly adhere to the following cost-minimization best practices:

1. **Serverless First (S3 + Lambda)**
   - Always default to serving frontend applications as static websites from S3 buckets.
   - For backend logic, prefer AWS Lambda.
   - Never deploy EC2 instances, ECS clusters, or EKS unless explicitly required by the user.

2. **VPC Guardrails (Strict Rule)**
   - **DO NOT** create custom VPCs. 
   - **DO NOT** create or attach NAT Gateways. NAT Gateways incur significant hourly costs and data processing fees.
   - **DO NOT** create VPC Endpoints (PrivateLink) unless explicitly instructed.
   - If a Lambda needs internet access, do not place it inside a VPC. Let it use the default AWS networking.

3. **Public IPv4 Addressing**
   - **DO NOT** assign Public IPv4 addresses to EC2 instances, ECS tasks, or other resources unless absolutely necessary, as AWS now charges an hourly fee for every public IPv4 address.
   - If public internet access is required without a load balancer, seek user authorization first. Consider using IPv6 if the use-case permits.

4. **Cost Awareness**
   - If a requested architecture risks incurring high costs (e.g., relational databases like RDS, rather than DynamoDB or SQLite), warn the user explicitly and wait for authorization.
   - Ensure all resources created are easily destroyable (e.g., proper tagging, lifecycle rules for S3).

5. **S3 Deployments**
   - When using `aws s3 sync` or similar commands to upload a project, **always** verify your source directory.
   - **DO NOT** sync parent directories (e.g., `../`) or the entire workspace unless explicitly requested. Use explicit paths (like `./` or `dist/`) to prevent accidentally uploading the entire codebase and hitting timeouts or excessive storage costs.
# AWS Deployment Runbook

This runbook outlines the standard, modern, and cost-effective procedures for deploying applications to AWS using Terraform. Always follow these patterns to avoid common pitfalls (like Terraform provider version conflicts) and to keep aws costs near zero.

## 1. Static Site Deployment (S3 Website)

When deploying a frontend SPA (React, Vanilla JS, etc.), use S3 configured for Static Website Hosting. 

**CRITICAL TERRAFORM V4/V5 SYNTAX**: The AWS Terraform provider (v4.0+) removed the inline `website` block from `aws_s3_bucket`. You MUST use the standalone `aws_s3_bucket_website_configuration`, `aws_s3_bucket_public_access_block`, and `aws_s3_bucket_policy` resources.

```terraform
# 1. Provide the AWS Provider
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
provider "aws" {
  region = "us-east-1"
}

# 2. Create the Bucket
resource "aws_s3_bucket" "site" {
  bucket = "my-unique-project-name-2026" # Must be globally unique
}

# 3. Enable Website Hosting
resource "aws_s3_bucket_website_configuration" "site_config" {
  bucket = aws_s3_bucket.site.id

  index_document {
    suffix = "index.html"
  }
  error_document {
    key = "index.html" # For SPA routing (React/Vue/etc)
  }
}

# 4. Disable Block Public Access (Required before adding a public policy)
resource "aws_s3_bucket_public_access_block" "site_access" {
  bucket = aws_s3_bucket.site.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# 5. Attach Public Read Policy
resource "aws_s3_bucket_policy" "site_policy" {
  bucket = aws_s3_bucket.site.id
  depends_on = [aws_s3_bucket_public_access_block.site_access]

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

output "website_url" {
  value = "http://${aws_s3_bucket_website_configuration.site_config.website_endpoint}"
}
```

### Deploying the Files
To upload files to this bucket, use the aws-cli. **ALWAYS** use a specific source directory to avoid uploading your entire workspace:
`aws s3 sync ./dist s3://my-unique-project-name-2026 --delete`

---

## 2. Backend APIs (API Gateway + Lambda)

For backend logic, the standard is AWS API Gateway (HTTP API v2) triggering an AWS Lambda function. This is strictly pay-per-request and costs $0 when idle. 

**Do not use EC2, ECS, or Application Load Balancers for simple APIs.**

```terraform
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../backend" # Path to your lambda code
  output_path = "${path.module}/lambda.zip"
}

# USE THE EXISTING SHARED LAMBDA EXECUTION ROLE
# CRITICAL: DO NOT CREATE NEW IAM ROLES! The ai-agent-user lacks `iam:CreateRole` permissions.
# Always use the pre-existing "SharedLambdaExecutionRole" for all normal Lambda functions.
data "aws_iam_role" "lambda_exec" {
  name = "SharedLambdaExecutionRole"
}

# The Lambda Function
resource "aws_lambda_function" "api_handler" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "my_api_handler"
  role             = data.aws_iam_role.lambda_exec.arn
  handler          = "index.handler" # or app.handler for python
  runtime          = "nodejs20.x"    # or python3.11 etc
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
}

# Function URL (Simplest way to expose a Lambda directly, no API Gateway needed!)
resource "aws_lambda_function_url" "api_url" {
  function_name      = aws_lambda_function.api_handler.function_name
  authorization_type = "NONE" # Public API

  cors {
    allow_credentials = true
    allow_origins     = ["*"]
    allow_methods     = ["*"]
    allow_headers     = ["date", "keep-alive"]
    expose_headers    = ["keep-alive", "date"]
    max_age           = 86400
  }
}

output "api_endpoint" {
  value = aws_lambda_function_url.api_url.function_url
}
```
*Note: AWS Lambda Function URLs are often simpler, cheaper, and faster to deploy than a full API Gateway for single-purpose APIs.*

### MVP Requirements for React + Lambda + Auth
When setting up a React frontend with a Lambda API and user authentication (like Cognito), CORS (Cross-Origin Resource Sharing) is a critical requirement that is often overlooked. 
- **OPTIONS Methods:** Ensure API Gateway (or Function URL) explicitly handles `OPTIONS` preflight requests.
- **CORS Headers:** The API response must include standard CORS headers (e.g., `Access-Control-Allow-Origin`, `Access-Control-Allow-Headers`, `Access-Control-Allow-Methods`). When using AWS API Gateway with Lambda proxy integration, the Lambda function itself MUST return these headers in its response.
  - **CRITICAL WARNING**: API Gateway Proxy Integrations require all header values to be strings. If you pass a boolean (e.g., `"Access-Control-Allow-Credentials": true`), the Lambda will crash internally and API Gateway will return a `502 Bad Gateway` error, which the browser will obfuscate as a CORS Network Error. You MUST use string booleans: `"Access-Control-Allow-Credentials": "true"`.
- **Authorization Headers:** When using User Auth, ensure the `Authorization` header is included in the allowed headers for CORS preflight.

---

## 3. Databases & State (Cheapest Options First)

When a project requires state or a database, always default to the cheapest, serverless options. **NEVER provision an RDS instance (PostgreSQL, MySQL).**

### Option A: DynamoDB (Preferred for NoSQL/Key-Value)
DynamoDB with On-Demand capacity costs $0 when idle. It is the perfect companion to Lambda.
```terraform
resource "aws_dynamodb_table" "app_data" {
  name         = "my_app_table"
  billing_mode = "PAY_PER_REQUEST" # CRITICAL: Do not use PROVISIONED
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }
}
```
*(Don't forget to grant your Lambda IAM Role permission to `dynamodb:*` on this table!)*

### Option B: S3 (Preferred for Large JSON blobs or Files)
If the app just needs to save user configurations or large blobs of data, saving them as serialized JSON files directly in a private S3 bucket is extremely cheap. Add `s3:PutObject` and `s3:GetObject` to your Lambda role.

### Option C: SQLite via AWS EFS (For Relational Needs)
If you strictly need SQL (joins, aggregations), provision an AWS EFS (Elastic File System) volume and mount it to your Lambda function. You can run a standard SQLite file database on this shared EFS volume. 
*Note: EFS requires the Lambda to be inside a VPC, which complicates networking. Only use this if DynamoDB is insufficient.*
