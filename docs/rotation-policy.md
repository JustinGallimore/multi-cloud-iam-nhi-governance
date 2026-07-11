# Access Key & Credential Rotation Policy

## Purpose

This policy defines the standards for rotating static credentials, AWS IAM access keys and Azure app registration client secrets, across the Multi-Cloud IAM and Non-Human Identity Governance environment. Static credentials that are never rotated are one of the most common paths to unauthorized access in real world breaches, since a credential leaked once, even years earlier, remains valid indefinitely unless a rotation policy forces it to expire.

## Scope

This policy applies to:
- AWS IAM user access keys
- Azure app registration client secrets and certificates
- Any future service account credentials created in either cloud environment covered by this project

This policy does not apply to short lived, automatically expiring credentials such as AWS STS temporary tokens or Azure managed identity tokens, since those are not the type of static credential this project's audit was designed to catch.

## Rotation Intervals

| Credential Type | Maximum Age | Action Required |
|---|---|---|
| AWS IAM access key | 90 days | Rotate immediately |
| Azure app registration client secret | 90 days | Rotate immediately |
| Azure app registration client secret | 60-89 days | Schedule rotation within 2 weeks |

### Why 90 days

A 90 day maximum aligns with widely recognized industry baselines, including AWS's own Trusted Advisor and Security Hub default checks, which flag access keys older than 90 days as a finding. This project adopts that same threshold rather than inventing a new one, since aligning with an industry standard makes this policy immediately recognizable and defensible in a real audit, rather than requiring a novel justification each time.

90 days also reflects a practical balance. Shorter intervals, such as 30 days, create excessive operational overhead for a small team or single administrator to manage manually, increasing the odds that rotation gets skipped entirely due to friction. Longer intervals, such as 180 days or a year, leave a wide window during which a leaked but still valid credential could be exploited undetected. 90 days is short enough to limit exposure meaningfully while remaining realistic to enforce without full automation in place.

Once the OIDC federation work in Phase 6 is complete for CI/CD pipeline authentication, the long term goal is to eliminate static credentials for that use case entirely, making this rotation interval a compensating control for the credentials that still remain, such as this project's own CLI setup keys, rather than the primary defense.

## Roles and Responsibilities

**Identity Owner** — The individual or team listed in `docs/ownership_mapping.csv` for a given credential. Responsible for initiating rotation before the maximum age threshold is reached, and for updating any dependent systems or scripts that reference the old credential.

**Security/IAM Administrator** — Responsible for running the audit scripts (`scripts/aws/iam_audit.py` and `scripts/azure/azure_audit.py`) on a recurring basis, reviewing the output for credentials approaching or exceeding the maximum age, and notifying the relevant Identity Owner.

In this lab environment, both roles are held by the same person, Justin Gallimore, acting as both the tenant administrator and the account owner for every credential in scope. In a real organization, these responsibilities would typically be split across a platform or security team (running audits, setting policy) and individual application or service owners (actually rotating their own credentials), since no single person can reasonably own rotation for every credential in a company at scale.

## Enforcement and Verification

Compliance with this policy is verified automatically rather than manually tracked. The AWS audit script (`scripts/aws/iam_audit.py`) calculates the age in days of every IAM user access key and sets a `NeedsRotation` flag to `true` for any key exceeding 90 days. The Azure audit script (`scripts/azure/azure_audit.py`) performs the equivalent check against app registration client secret expiration dates.

The ownership mapping script (`scripts/ownership_mapping.py`) consumes both audit outputs and surfaces any credential requiring action directly in the `RiskFlag` column of `docs/ownership_mapping.csv`, alongside the responsible owner, so that a single sorted view of that file shows exactly what needs attention and who is accountable for it.

### Verification Cadence

This policy is considered enforced when the audit scripts are run and reviewed on a regular cadence. For this lab environment, that cadence is monthly. In a production environment, this would typically run on an automated schedule, for example a scheduled GitHub Actions workflow or a cron job, rather than being triggered manually, removing the possibility of the check being forgotten or skipped.

### Exceptions

Any credential that cannot be rotated within the required window, for example due to a dependency on a third party integration with its own rotation constraints, must have that exception documented directly in this file with a stated reason and a target remediation date, rather than being silently left out of compliance.