# oidc_role.tf
# Purpose: Defines the IAM role that GitHub Actions will assume via
# OIDC federation. The trust policy is scoped to a specific GitHub
# repo and branch, so no other repo could ever assume this role even
# if they somehow obtained a valid GitHub OIDC token.

# References the OIDC identity provider already created manually in
# the AWS console in Step 1. Terraform does not recreate it, it just
# looks it up so the trust policy below can reference its ARN.
data "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"
}

resource "aws_iam_role" "github_actions_test" {
  name = "github-actions-oidc-test-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = data.aws_iam_openid_connect_provider.github.arn
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          }
          StringLike = {
            "token.actions.githubusercontent.com:sub" = "repo:JustinGallimore/multi-cloud-iam-nhi-governance:ref:refs/heads/main"
          }
        }
      }
    ]
  })

  tags = {
    Purpose = "OIDC federation test Phase 6 portfolio project"
  }
}

# No inline policy is attached here on purpose. sts:GetCallerIdentity
# does not require any IAM permission grant, it is available to any
# authenticated principal by default. This role exists purely to
# prove the trust relationship works end to end.