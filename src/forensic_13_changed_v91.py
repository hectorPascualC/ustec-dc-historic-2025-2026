#!/usr/bin/env python3
"""Prepare the 13 public PDF URLs whose SHA-256 changed from V24 to V86."""
import csv
import json
import re
from pathlib import Path

source = Path("exports_territorial/SSTT_V87_AUDITORIA_COMPLETA_12_AMBITS.json")
output = Path("exports_territorial/SSTT_V91_CHANGED_INPUT.csv")
data = json.loads(source.read_text(encoding="utf-8"))
rows = data["pdf_changed_source_links"]
if len(rows) != 13 or len({row["url"] for row in rows}) != 13:
    raise SystemExit("Expected 13 unique changed public PDF URLs")
for row in rows:
    for field in ("old_sha256", "sha256_v86"):
        if not re.fullmatch(r"[0-9a-f]{64}", row.get(field, "")):
            raise SystemExit(f"Invalid {field} for {row.get('area')}")
    if row["old_sha256"] == row["sha256_v86"]:
        raise SystemExit("Unchanged PDF in changed-input manifest")
with output.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["territori", "url", "old_sha256", "sha256_v86"])
    writer.writeheader()
    for row in rows:
        writer.writerow({"territori": row["area"], "url": row["url"], "old_sha256": row["old_sha256"], "sha256_v86": row["sha256_v86"]})
print("Prepared 13 distinct public SSTT PDF URLs")
