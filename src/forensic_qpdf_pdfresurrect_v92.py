#!/usr/bin/env python3
"""V92: independent qpdf + PDFResurrect checks on 13 mutable public DC PDFs.
No PDF bytes, page text, applicant data, or extracted versions are uploaded.
An incremental PDF revision is NOT a historical server-side overwrite.
"""
import csv
import datetime as dt
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path

import fitz
import requests

SOURCE = Path("exports_territorial/SSTT_V91_CHANGED_INPUT.csv")
OUT = Path("exports_territorial/SSTT_V92_QPDF_PDFRESURRECT.json")
MAX_BYTES = 14_000_000
CODE_RE = re.compile(r"(?<![\w\d])(?:507|627|F57|F87)(?![\w\d])", re.I)
DATE_RE = re.compile(r"(?<!\d)2025(?!\d)")

def command(args, cwd, timeout=30):
    try:
        p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return {"returncode": p.returncode, "output_excerpt": (p.stdout + "\n" + p.stderr)[-700:]}
    except Exception as e:
        return {"error": type(e).__name__}

def pdf_info(path):
    try:
        d = fitz.open(str(path))
        texts = [d[i].get_text("text") for i in range(min(40, len(d)))]
        s = "\n".join(texts)
        pages = len(d)
        repaired = bool(d.is_repaired)
        d.close()
        return {"valid": bool(pages and s.strip()), "pages": pages, "repaired": repaired,
                "text_sha256": hashlib.sha256(s.encode()).hexdigest(),
                "contains_2025": bool(DATE_RE.search(s)),
                "specialty_codes": sorted(set(CODE_RE.findall(s.upper())))}
    except Exception as e:
        return {"valid": False, "error": type(e).__name__}

def check(row):
    area = row["territori"]
    url = row["url"]
    o = {"territori": area, "url": url, "http": None, "is_pdf": False}
    with tempfile.TemporaryDirectory(prefix="dc_forensic_") as folder:
        base = Path(folder)
        path = base / "current.pdf"
        try:
            r = requests.get(url, timeout=30, headers={"User-Agent": "DC historic audit V92"}, stream=True)
            o["http"] = r.status_code
            if r.status_code != 200:
                return o
            raw = bytearray()
            for chunk in r.iter_content(65536):
                raw.extend(chunk)
                if len(raw) > MAX_BYTES:
                    o["error"] = "MAX_BYTES_EXCEEDED"
                    return o
            if not raw.startswith(b"%PDF-"):
                o["error"] = "NOT_PDF"
                return o
            path.write_bytes(raw)
            o.update({"is_pdf": True, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
            current = pdf_info(path)
            o["current_pdf"] = current
            o["qpdf_check"] = command(["qpdf", "--check", str(path)], folder)
            o["pdfresurrect_query"] = command(["pdfresurrect", str(path), "-q"], folder)
            o["pdfresurrect_extract"] = command(["pdfresurrect", str(path), "-w"], folder, 40)
            versions = []
            for old in sorted(base.rglob("*.pdf")):
                if old.resolve() == path.resolve():
                    continue
                info = pdf_info(old)
                info["sha256"] = hashlib.sha256(old.read_bytes()).hexdigest()
                info["bytes"] = old.stat().st_size
                info["different_text"] = (info.get("text_sha256") != current.get("text_sha256"))
                versions.append(info)
            o["extracted_versions"] = versions
            o["extracted_count"] = len(versions)
            o["valid_extracted_count"] = sum(v.get("valid", False) for v in versions)
            o["changed_text_count"] = sum(v.get("valid", False) and v.get("different_text", False) for v in versions)
            o["possible_2025_with_code"] = sum(
                v.get("valid", False) and v.get("different_text", False)
                and v.get("contains_2025", False) and bool(v.get("specialty_codes"))
                for v in versions)
        except Exception as e:
            o["error"] = type(e).__name__
    return o

def main():
    with SOURCE.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 13 or len(set(row["url"] for row in rows)) != 13:
        raise SystemExit("Expected 13 distinct public PDF URLs")
    results = []
    for row in rows:
        v = check(row)
        results.append(v)
        print(f'{v["territori"]}: HTTP={v.get("http")}, qpdf={v.get("qpdf_check",{}).get("returncode")}, extracted={v.get("extracted_count",0)}', flush=True)
    report = {
        "checked_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "method": "qpdf --check + pdfresurrect -q/-w on 13 mutable PDF URLs",
        "files": results,
        "total": len(results),
        "downloaded": sum(x.get("is_pdf",False) for x in results),
        "qpdf_clean": sum(x.get("qpdf_check",{}).get("returncode")==0 for x in results),
        "extracted_versions": sum(x.get("extracted_count",0) for x in results),
        "valid_extracted": sum(x.get("valid_extracted_count",0) for x in results),
        "changed_text_versions": sum(x.get("changed_text_count",0) for x in results),
        "possible_2025_with_code": sum(x.get("possible_2025_with_code",0) for x in results),
        "historical_publications_certified": 0,
        "warnings": [
            "Internal revisions are not proof of a 2025-2026 server publication.",
            "A fully overwritten PDF is not recoverable by qpdf or PDFResurrect.",
            "No raw PDFs, extracted pages, or personal data are persisted in artifacts.",
            "Even a 2025 reference with specialty code requires offer and publication-date verification."
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ["total","downloaded","qpdf_clean","extracted_versions","valid_extracted","changed_text_versions","possible_2025_with_code"]}))

if __name__ == "__main__":
    main()
