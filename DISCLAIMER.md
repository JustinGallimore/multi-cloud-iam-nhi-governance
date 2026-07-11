# Disclaimer

This repository documents a personal homelab project built for
learning and portfolio purposes. It is not affiliated with, sponsored
by, or run against any employer, client, or production environment,
past or present.

## Lab Environment

- The AWS account used in this project is a personal account created
  specifically for this lab, not a production or employer-owned
  account.
- The Azure tenant used in this project is a personal Entra ID tenant,
  not affiliated with any organization.
- Any account IDs, tenant IDs, ARNs, role names, or other identifiers
  visible in this repository, its screenshots, or its documentation
  belong to this isolated personal lab environment and grant no access
  to anyone outside of it.
- Where credential exposure incidents are documented in
  TROUBLESHOOTING.md, the exposed credentials were rotated and deleted
  immediately upon discovery, and no exposed credential remains valid.

## Simulated Data

Some data in this project is simulated rather than sourced from real
users or organizations, and is clearly labeled as such where it
appears:

- Identity attestation responses (Approved, Rejected, No Response) are
  generated using weighted random simulation, since no real coworkers
  exist in this lab to respond to attestation requests. This is
  documented in `docs/attestation-policy.md`.
- Real audit output files (containing live identity data from this
  personal lab) are excluded from this public repository. Any sample
  output files included in `docs/` are clearly labeled as samples.

## Purpose

This project exists to demonstrate hands-on IAM engineering skills,
including cloud identity auditing, governance workflow automation, and
secure CI/CD authentication patterns. It is not intended as a
production-ready tool, a security audit framework for any real
organization, or professional security advice. Anyone adapting
concepts from this repository for a production environment should
apply appropriate scoped permissions, real notification integrations,
and organizational review processes not present in this lab
environment.