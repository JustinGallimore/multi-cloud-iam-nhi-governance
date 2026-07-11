"""
attestation_generator.py

Purpose: Reads the ownership mapping CSV from Phase 3 and generates
an attestation record for every identity. Each record represents a
request asking the identity owner to confirm they still need that
access. This is the input file that later steps will use to track
approvals, rejections, and non responses.

Run this from the project root with the venv activated:
python scripts/attestation_generator.py
"""

import csv
import json
from datetime import datetime, timedelta

INPUT_CSV = "docs/ownership_mapping.csv"
OUTPUT_JSON = "docs/attestation_records.json"
ATTESTATION_WINDOW_DAYS = 30


def generate_attestation_records():
    records = []
    today = datetime.now()
    due_date = today + timedelta(days=ATTESTATION_WINDOW_DAYS)

    with open(INPUT_CSV, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            record = {
                "Cloud": row["Cloud"],
                "IdentityType": row["IdentityType"],
                "Name": row["Name"],
                "Owner": row["Owner"],
                "RiskFlag": row["RiskFlag"],
                "AttestationStatus": "Pending",
                "DateSent": today.strftime("%Y-%m-%d"),
                "DueDate": due_date.strftime("%Y-%m-%d"),
            }
            records.append(record)

    return records


def save_records(records):
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
    print(f"Generated {len(records)} attestation records.")
    print(f"Saved to {OUTPUT_JSON}")


if __name__ == "__main__":
    records = generate_attestation_records()
    save_records(records)