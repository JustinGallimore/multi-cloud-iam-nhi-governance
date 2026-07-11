# Multi-Cloud IAM and Non-Human Identity Governance

A homelab project that audits, maps, and governs non-human identities
(service accounts, API keys, app registrations, and managed
identities) across AWS and Azure, then secures its own CI/CD pipeline
using OIDC federation instead of static credentials.

## What This Project Does

- Audits IAM users, roles, and access keys in AWS, and service
  principals and app registrations in Azure Entra ID
- Maps every identity across both clouds into a single ownership view
  with automated risk classification
- Runs a recurring identity attestation cycle, confirming with owners
  that access is still needed, and produces a governance report
  naming every high-risk finding
- Defines a rotation policy for static credentials, tied directly to
  audit findings
- Uses Terraform to configure OIDC federation between GitHub Actions
  and AWS, eliminating static AWS access keys from CI/CD entirely

## Tech Stack

- **AWS**: IAM, OIDC Identity Provider
- **Azure**: Entra ID, Microsoft Graph API
- **Python**: `boto3`, `azure-identity`, `msgraph-sdk` (async)
- **Terraform**: AWS provider, IAM role and OIDC trust policy
- **GitHub Actions**: OIDC token-based AWS authentication
- **Documentation**: Markdown, structured as a phased build

## Architecture

Read [ARCHITECTURE.md](docs/ARCHITECTURE.md) for a full breakdown of
the data pipeline, how each script owns a single responsibility, and
how the OIDC trust relationship is structured.

## Build Walkthrough

Read [WALKTHROUGH.md](docs/WALKTHROUGH.md) for a phase by phase,
screenshot by screenshot account of how this project was built,
including real errors encountered and how each was diagnosed and
fixed.

## Troubleshooting Log

Read [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for a running log
of real issues hit during this build, root causes, and fixes.

## Governance Documents

- [rotation-policy.md](docs/rotation-policy.md) — credential rotation
  intervals and enforcement
- [attestation-policy.md](docs/attestation-policy.md) — identity
  attestation cycle definition
- [attestation_report.md](docs/attestation_report.md) — sample output
  from a completed attestation cycle

## Project Structure

├── scripts/
│   ├── aws/iam_audit.py
│   ├── azure/azure_audit.py
│   ├── ownership_mapping.py
│   ├── attestation_generator.py
│   ├── attestation_response_simulator.py
│   └── attestation_report.py
├── terraform/aws/
│   ├── provider.tf
│   ├── oidc_role.tf
│   └── outputs.tf
├── .github/workflows/
│   └── oidc-test.yml
├── docs/
│   ├── ARCHITECTURE.md
│   ├── WALKTHROUGH.md
│   ├── TROUBLESHOOTING.md
│   ├── rotation-policy.md
│   ├── attestation-policy.md
│   └── attestation_report.md
└── screenshots/

## Note on Data

Real audit output and attestation results contain live account
identifiers and are excluded from this repository via `.gitignore`.
See [DISCLAIMER.md](DISCLAIMER.md) for more on the nature of this lab
environment and how excluded data is handled.

## Status

Phases 1 through 6 complete. Phase 7 (final documentation polish and
sample files) in progress.