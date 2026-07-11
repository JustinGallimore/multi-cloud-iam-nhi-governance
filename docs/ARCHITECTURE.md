# Architecture

This document describes how the pieces of this project fit together.
For the story of how it was built, including troubleshooting, see
WALKTHROUGH.md.

## Overview

This project audits, maps, governs, and secures non-human identities
(service accounts, API keys, app registrations, and managed identities)
across AWS and Azure. It is built as a pipeline of small, single
responsibility scripts rather than one monolithic tool, so each stage
can be run, tested, and understood independently.

## Cloud Environments

- **AWS**: IAM users, roles, and access keys, audited via `boto3`
  using credentials configured through the AWS CLI.
- **Azure**: Entra ID service principals and app registrations,
  audited via `msgraph-sdk` using `DefaultAzureCredential` against a
  native internal admin account in a subscription-less, Entra ID only
  tenant.

Both environments are read using least-invasive, read-only API calls
wherever possible. In this lab, both were run under broad
administrative permissions (AdministratorAccess in AWS, Global Admin
in Entra ID); a production deployment would instead use narrowly
scoped, read-only permissions specific to each audit script.

## Data Pipeline

The system is built as a sequence of stages, each reading the output
of the previous stage and writing its own output file. No stage
mutates another stage's output file directly.

1. **Audit** (`scripts/aws/iam_audit.py`,
   `scripts/azure/azure_audit.py`) — Pulls raw identity data from each
   cloud and writes `aws_iam_audit.json` and `azure_iam_audit.json`.
   These files contain real account data and are excluded from the
   public repo via `.gitignore`.

2. **Ownership Mapping** (`scripts/ownership_mapping.py`) — Reads both
   audit files and produces a single unified view of every identity
   across both clouds, with an assigned Owner and a RiskFlag, written
   to `docs/ownership_mapping.csv`.

3. **Rotation Policy** (`docs/rotation-policy.md`) — A written policy
   document, not a script, that defines rotation intervals for static
   credentials and ties directly to the `NeedsRotation` flag produced
   during the audit stage.

4. **Attestation** (`scripts/attestation_generator.py`,
   `scripts/attestation_response_simulator.py`,
   `scripts/attestation_report.py`) — Three separate scripts, each
   owning one job: generating attestation requests from the ownership
   mapping, simulating owner responses, and producing a human readable
   markdown governance report (`docs/attestation_report.md`) that
   individually names every high-risk identity. Attestation output
   files (`attestation_records.json`, `attestation_results.json`)
   contain real identity data and are excluded from the public repo.

5. **OIDC Federation** (Terraform + GitHub Actions) — Secures the
   CI/CD layer itself, eliminating static AWS credentials from the
   pipeline that runs and will eventually deploy this project's
   infrastructure. Described in detail below.

## Single Responsibility Principle

Each script in this pipeline does exactly one thing:

- The audit scripts only read from the cloud and write raw JSON.
- The ownership mapping script only combines and classifies.
- Each attestation script only generates, simulates, or reports, never
  more than one of the three.

This mirrors how the same principle was applied to the Terraform
configuration in Phase 6, where provider setup, the IAM role and trust
policy, and outputs are each defined in their own file
(`provider.tf`, `oidc_role.tf`, `outputs.tf`).

## Credential Handling

No cloud credentials are hardcoded in this repository. AWS access is
authenticated via the AWS CLI's locally configured credentials, Azure
access via `DefaultAzureCredential`, and both are read from the local
environment at runtime, never committed to source control.

Files that contain real audit output, Terraform state, or other
sensitive local data are excluded from the public repository via
`.gitignore`. Where sample output is useful for a public reader,
clearly labeled sample files are provided instead of real data (see
Phase 7).

## OIDC Federation for CI/CD (Phase 6)

GitHub Actions authenticates to AWS using OpenID Connect rather than
static access keys. The trust relationship works as follows:

1. AWS IAM trusts `token.actions.githubusercontent.com` as an OIDC
   identity provider, registered manually in the AWS console.
2. An IAM role, `github-actions-oidc-test-role`, defined in Terraform
   at `terraform/aws/oidc_role.tf`, trusts that identity provider, but
   only for tokens where the `sub` claim matches
   `repo:JustinGallimore/multi-cloud-iam-nhi-governance:ref:refs/heads/main`
   and the `aud` claim matches `sts.amazonaws.com`.
3. When the `.github/workflows/oidc-test.yml` workflow runs, GitHub
   issues a short lived token matching those exact claims. AWS
   validates the token against the role's trust policy and issues
   temporary credentials scoped to that role.
4. No AWS access keys or secrets exist in GitHub at any point. Trust
   is established entirely through the scoped relationship between the
   identity provider and the IAM role's condition block.

This role currently grants no permissions beyond what any
authenticated AWS principal has by default, `sts:GetCallerIdentity`.
It exists to prove the OIDC trust chain works end to end before
expanding to real deployment permissions in a future iteration.