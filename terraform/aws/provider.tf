# provider.tf
# Purpose: Tells Terraform this project targets AWS, and which region
# to create resources in. No credentials are hardcoded here, Terraform
# uses whatever AWS CLI profile is already configured locally.

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-2"
}