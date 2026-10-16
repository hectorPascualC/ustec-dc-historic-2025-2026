#!/usr/bin/env python3
"""Prepare the 13 public PDF URLs whose SHA-256 changed from V24 to V86."""
import csv
import json
from pathlib import Path

source = Path("exports_territorial/SSTT_V87_AUDITORIA_COMPLETA_12_AMBITS.json")
output = Path("exports_territorial/SSTT_V91_CHANGED_INPUT.csv")
data = json.loads(source.read_text(encoding="utf-8"))
rows = data["pdf_changed_source_links"]
if len(rows) != 13 or len({row["url"] for row in rows}) != 13:
    raise SystemExit("Expected 13 unique changed public PDF URLs")
with output.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["territori", "url"])
    writer.writeheader()
    for row in rows:
        writer.writerow({"territori": row["area"], "url": row["url"]})
print("Prepared 13 distinct public SSTT PDF URLs")
