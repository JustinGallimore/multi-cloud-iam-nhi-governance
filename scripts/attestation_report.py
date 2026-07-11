"""
attestation_report.py

Purpose: Reads the completed attestation results and generates a
clean markdown governance report. This is the human readable
deliverable, the kind of document that would actually get handed
to a manager or auditor after an attestation cycle closes.

Run this from the project root with the venv activated:
python scripts/attestation_report.py
"""

import json
from datetime import datetime

INPUT_JSON = "docs/attestation_results.json"
OUTPUT_MD = "docs/attestation_report.md"


def load_results():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def build_report(records):
    total = len(records)
    approved = [r for r in records if r["AttestationStatus"] == "Approved"]
    rejected = [r for r in records if r["AttestationStatus"] == "Rejected"]
    no_response = [r for r in records if r["AttestationStatus"] == "No Response"]

    approved_pct = round((len(approved) / total) * 100, 1)
    rejected_pct = round((len(rejected) / total) * 100, 1)
    no_response_pct = round((len(no_response) / total) * 100, 1)

    report_date = datetime.now().strftime("%Y-%m-%d")

    lines = []
    lines.append("# Identity Attestation Report")
    lines.append("")
    lines.append(f"**Report Date:** {report_date}")
    lines.append(f"**Total Identities Reviewed:** {total}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Approved: {len(approved)} ({approved_pct}%)")
    lines.append(f"- Rejected: {len(rejected)} ({rejected_pct}%)")
    lines.append(f"- No Response: {len(no_response)} ({no_response_pct}%)")
    lines.append("")

    lines.append("## High Priority: No Response")
    lines.append("")
    lines.append("These identities had no owner confirmation by the due date. "
                  "In a real environment these would be escalated to the "
                  "security team for manual review, and access may be "
                  "suspended pending confirmation.")
    lines.append("")
    if no_response:
        lines.append("| Cloud | Identity Type | Name | Owner | Due Date |")
        lines.append("|---|---|---|---|---|")
        for r in no_response:
            lines.append(
                f"| {r['Cloud']} | {r['IdentityType']} | {r['Name']} | "
                f"{r['Owner']} | {r['DueDate']} |"
            )
    else:
        lines.append("No identities fall into this category for this cycle.")
    lines.append("")

    lines.append("## Queued for Removal: Rejected")
    lines.append("")
    lines.append("These identities were explicitly marked as no longer needed "
                  "by their owner. Recommended action is to revoke access "
                  "within the next maintenance window.")
    lines.append("")
    if rejected:
        lines.append("| Cloud | Identity Type | Name | Owner | Response Date |")
        lines.append("|---|---|---|---|---|")
        for r in rejected:
            lines.append(
                f"| {r['Cloud']} | {r['IdentityType']} | {r['Name']} | "
                f"{r['Owner']} | {r['ResponseDate']} |"
            )
    else:
        lines.append("No identities fall into this category for this cycle.")
    lines.append("")

    return "\n".join(lines)


def save_report(content):
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Report saved to {OUTPUT_MD}")


if __name__ == "__main__":
    records = load_results()
    report_content = build_report(records)
    save_report(report_content)
    print("Report generation complete.")