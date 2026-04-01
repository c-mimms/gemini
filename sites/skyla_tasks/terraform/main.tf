terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region  = "us-east-1"
  profile = "AdministratorAccess-302205098862"
}

data "aws_acm_certificate" "wildcard" {
  domain      = "*.cbmo.net"
  statuses    = ["ISSUED"]
}

data "aws_route53_zone" "primary" {
  name = "cbmo.net"
}

resource "aws_cloudfront_distribution" "skyla_cdn" {
  enabled             = true
  default_root_object = "index.html"
  aliases             = ["skyla.cbmo.net"]
  comment             = "CloudFront for skyla.cbmo.net"

  origin {
    domain_name = "gemini-designs-portfolio-2026-v2.s3.us-east-1.amazonaws.com"
    origin_id   = "s3-skyla"
    origin_path = "/skyla_tasks"
  }

  default_cache_behavior {
    target_origin_id       = "s3-skyla"
    viewer_protocol_policy = "redirect-to-https"
    cache_policy_id        = "658327ea-f89d-4fab-a63d-7e88639e58f6"
    
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

resource "aws_route53_record" "skyla_alias" {
  zone_id = data.aws_route53_zone.primary.zone_id
  name    = "skyla.cbmo.net"
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.skyla_cdn.domain_name
    zone_id                = aws_cloudfront_distribution.skyla_cdn.hosted_zone_id
    evaluate_target_health = false
  }
}

output "cloudfront_id" {
  value = aws_cloudfront_distribution.skyla_cdn.id
}
