# outputs.tf
# Purpose: Prints the new role's ARN after terraform apply finishes,
# so it can be copied into the GitHub Actions workflow file in the
# next step without having to dig through the AWS console.

output "github_actions_role_arn" {
  value = aws_iam_role.github_actions_test.arn
}