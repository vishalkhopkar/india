terraform {
  required_version = ">= 1.10"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.66"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.7"
    }
  }

  # State lives in S3 so each GitHub Actions run picks up where the last left off. The bucket
  # and region are passed by the workflow (-backend-config), which also creates the bucket.
  backend "s3" {
    key          = "feedback-service/terraform.tfstate"
    encrypt      = true
    use_lockfile = true
  }
}

# Region comes from AWS_REGION, which the workflow sets.
provider "aws" {
  default_tags {
    tags = {
      Project   = var.name
      ManagedBy = "terraform"
    }
  }
}

data "aws_region" "current" {}
data "aws_caller_identity" "current" {}
