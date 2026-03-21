# AWS CloudFront + ACM Subdomain Architecture

## Overview
This document outlines the architecture deployed to securely host multiple static sites mapped to subdomains of `cbmo.net`. 

### Components
1. **Amazon S3**: Acts as the centralized storage origin. Each static site lives in a subfolder (e.g., `/georgia-mining/`, `/trump/`, `/sites-index/`).
2. **AWS Certificate Manager (ACM)**: A single wildcard certificate (`*.cbmo.net`) was provisioned in the `us-east-1` region to provide free SSL/TLS for all current and future subdomains.
3. **Amazon CloudFront**: A unique Content Delivery Network (CDN) distribution was created for each subdomain. Each distribution points to the specific S3 subfolder (`OriginPath`) and enforces HTTPS using the wildcard certificate.
4. **Amazon Route 53**: Dynamic `A` ALIAS records were created to seamlessly route traffic from the readable subdomains to their respective CloudFront edge nodes.

---

## Should We Have Used Terraform?

**Absolutely.** While using the AWS CLI allowed us to rapidly prototype and deploy the infrastructure on the fly, using **Terraform** (or AWS CDK) is highly recommended for managing this kind of architecture. 

Here is why migrating to Terraform would be beneficial:

1. **State Management**: Terraform keeps track of exactly what has been deployed. If you want to add a 5th site, you simply add three lines of code and run `terraform apply` instead of manually piecing together 4 JSON files and CLI commands.
2. **Idempotency**: Running a Terraform script multiple times is perfectly safe; it only applies changes where configuration has drifted.
3. **Version Control**: You can commit your infrastructure to a Git repository, allowing you to review changes, track history, and document your architecture natively within the codebase alongside your site deployments.
4. **Clean Teardowns**: If you ever want to decommission a site, you just delete the block of code. Terraform will safely untangle and delete the associated CloudFront distribution and Route 53 records without leaving stale "ghost" records behind.

---

## Future Replication (Terraform Blueprint)

If you decide to migrate this architecture to Terraform in the future, you can define your sites in a clean map variable and use a `for_each` loop. 

Here is a simplified blueprint of how you would replicate this setup in Terraform:

```hcl
variable "sites" {
  type = map(string)
  default = {
    news     = "/trump"
    mining   = "/georgia-mining"
    museum   = "/museum"
    research = "/research"
    sites    = "/sites-index"
  }
}

# Assume the Wildcard Cert and S3 Bucket exist natively
data "aws_acm_certificate" "wildcard" {
  domain      = "*.cbmo.net"
  statuses    = ["ISSUED"]
}

data "aws_route53_zone" "primary" {
  name         = "cbmo.net"
}

# Dynamically generate a CloudFront Distribution for every site
resource "aws_cloudfront_distribution" "cdn" {
  for_each = var.sites

  enabled             = true
  default_root_object = "index.html"
  aliases             = ["${each.key}.cbmo.net"]

  origin {
    domain_name = "gemini-designs-portfolio-2026-v2.s3.us-east-1.amazonaws.com"
    origin_id   = "s3-${each.key}"
    origin_path = each.value
  }

  default_cache_behavior {
    target_origin_id       = "s3-${each.key}"
    viewer_protocol_policy = "redirect-to-https"
    cache_policy_id        = "658327ea-f89d-4fab-a63d-7e88639e58f6" # Managed CachingOptimized
    
    allowed_methods = ["GET", "HEAD"]
    cached_methods  = ["GET", "HEAD"]
  }

  viewer_certificate {
    acm_certificate_arn      = data.aws_acm_certificate.wildcard.arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
  
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
}

# Dynamically route the ALIAS records to the new CF distributions
resource "aws_route53_record" "alias" {
  for_each = var.sites

  zone_id = data.aws_route53_zone.primary.zone_id
  name    = "${each.key}.cbmo.net"
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.cdn[each.key].domain_name
    zone_id                = aws_cloudfront_distribution.cdn[each.key].hosted_zone_id
    evaluate_target_health = false
  }
}
```
