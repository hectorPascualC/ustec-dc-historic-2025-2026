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
import resource
import os
import signal
import subprocess
import time
import tempfile
from pathlib import Path

import fitz
import requests

SOURCE = Path("exports_territorial/SSTT_V91_CHANGED_INPUT.csv")
OUT = Path("exports_territorial/SSTT_V92_QPDF_PDFRESURRECT.json")
MAX_BYTES = 14_000_000
MAX_EXTRACTED_BYTES = 56_000_000
MAX_EXTRACTED_FILES = 32
HASH_RE = re.compile(r"^[a-f0-9]{64}$")
CODE_RE = re.compile(r"(?<![\w\d])(?:507|627|F57|F87)(?![\w\d])", re.I)
DATE_RE = re.compile(r"(?<!\d)202[56](?!\d)")

def command(args, cwd, timeout=30, monitor_extraction=False):
    def limits():
        resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_EXTRACTED_BYTES, MAX_EXTRACTED_BYTES))
        resource.setrlimit(resource.RLIMIT_CPU, (min(timeout, 40), min(timeout, 40) + 1))
    try:
        with subprocess.Popen(args, cwd=cwd, stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL, preexec_fn=limits,
                              start_new_session=True) as p:
            started = time.monotonic()
            while p.poll() is None:
                if monitor_extraction:
                    files = [x for x in Path(cwd).rglob("*")
                             if x.is_file() and x.name != "current.pdf"]
                    if len(files) > MAX_EXTRACTED_FILES or sum(
                        x.stat().st_size for x in files if x.exists()
                    ) > MAX_EXTRACTED_BYTES:
                        os.killpg(p.pid, signal.SIGKILL)
                        p.wait()
                        return {"error": "EXTRACTION_QUOTA_EXCEEDED"}
                if time.monotonic() - started > timeout:
                    os.killpg(p.pid, signal.SIGKILL)
                    p.wait()
                    return {"error": "TimeoutExpired"}
                time.sleep(0.05)
            return {"returncode": p.returncode}
    except Exception as e:
        return {"error": type(e).__name__}

def pdf_info(path):
    try:
        digest = hashlib.sha256()
        codes = set()
        has_date = False
        with fitz.open(str(path)) as d:
            pages = len(d)
            repaired = bool(d.is_repaired)
            has_text = False
            for page in d:
                s = page.get_text("text")
                if s.strip():
                    has_text = True
                digest.update(s.encode("utf-8"))
                digest.update(b"\n")
                has_date = has_date or bool(DATE_RE.search(s))
                codes.update(CODE_RE.findall(s.upper()))
        return {"valid": bool(pages and has_text), "pages": pages, "repaired": repaired,
                "text_sha256": digest.hexdigest(),
                "contains_2025_or_2026": has_date,
                "specialty_codes": sorted(codes)}
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
            if r.status_code >= 500:
                o["status"] = "BLOCKED"
                o["error"] = "HTTP_5XX"
                r.close()
                return o
            if r.status_code != 200:
                o["status"] = "BLOCKED"
                o["error"] = "HTTP_NON_200"
                r.close()
                return o
            raw = bytearray()
            for chunk in r.iter_content(65536):
                raw.extend(chunk)
                if len(raw) > MAX_BYTES:
                    o["status"] = "BLOCKED"
                    o["error"] = "MAX_BYTES_EXCEEDED"
                    r.close()
                    return o
            r.close()
            if not raw.startswith(b"%PDF-"):
                o["status"] = "BLOCKED"
                o["error"] = "NOT_PDF"
                return o
            path.write_bytes(raw)
            o.update({"is_pdf": True, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
            expected = {key: row[key].strip().lower() for key in ("old_sha256", "sha256_v86") if row.get(key, "").strip()}
            o["expected_hashes"] = expected
            o["hash_match"] = {key: (o["sha256"] == value) for key, value in expected.items()}
            o["hash_comparison_status"] = ("MATCH" if any(o["hash_match"].values()) else "CHANGED") if expected else "NO_BASELINE"
            current = pdf_info(path)
            o["current_pdf"] = current
            o["qpdf_check"] = command(["qpdf", "--check", str(path)], folder)
            if o["qpdf_check"].get("error") or o["qpdf_check"].get("returncode") != 0:
                o["status"] = "BLOCKED"
                o["error"] = o["qpdf_check"].get("error") or "QPDF_NONZERO_EXIT"
                return o
            o["pdfresurrect_query"] = command(["pdfresurrect", str(path), "-q"], folder)
            if o["pdfresurrect_query"].get("error") or o["pdfresurrect_query"].get("returncode") != 0:
                o["status"] = "BLOCKED"
                o["error"] = o["pdfresurrect_query"].get("error") or "PDFRESURRECT_QUERY_NONZERO_EXIT"
                return o
            o["pdfresurrect_extract"] = command(["pdfresurrect", str(path), "-w"], folder, 40, monitor_extraction=True)
            extraction = o["pdfresurrect_extract"]
            if extraction.get("error") or extraction.get("returncode") != 0:
                o["status"] = "BLOCKED"
                o["error"] = extraction.get("error") or "PDFRESURRECT_NONZERO_EXIT"
                o["pdfresurrect_returncode"] = extraction.get("returncode")
                return o
            versions = []
            extracted_files = [p for p in base.rglob("*") if p.is_file() and p != path]
            extracted_bytes = sum(p.stat().st_size for p in extracted_files)
            if len(extracted_files) > MAX_EXTRACTED_FILES or extracted_bytes > MAX_EXTRACTED_BYTES:
                o["status"] = "BLOCKED"
                o["error"] = "EXTRACTION_QUOTA_EXCEEDED"
                o["extracted_files"] = len(extracted_files)
                o["extracted_bytes"] = extracted_bytes
                return o
            for old in sorted(base.rglob("*.pdf")):
                if old.resolve() == path.resolve():
                    continue
                info = pdf_info(old)
                digest = hashlib.sha256()
                with old.open("rb") as stream:
                    for block in iter(lambda: stream.read(65536), b""):
                        digest.update(block)
                info["sha256"] = digest.hexdigest()
                info["bytes"] = old.stat().st_size
                info["different_text"] = (info.get("text_sha256") != current.get("text_sha256"))
                versions.append(info)
            o["status"] = "PARTIAL"
            o["extracted_versions"] = versions
            o["extracted_count"] = len(versions)
            o["valid_extracted_count"] = sum(v.get("valid", False) for v in versions)
            o["changed_text_count"] = sum(v.get("valid", False) and v.get("different_text", False) for v in versions)
            o["possible_2025_2026_with_code"] = sum(
                v.get("valid", False) and v.get("different_text", False)
                and v.get("contains_2025_or_2026", False) and bool(v.get("specialty_codes"))
                for v in versions)
        except Exception as e:
            o["status"] = "BLOCKED"
            o["error"] = type(e).__name__
        finally:
            if "r" in locals():
                r.close()
    return o

def main():
    with SOURCE.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 13 or len(set(row["url"] for row in rows)) != 13:
        raise SystemExit("Expected 13 distinct public PDF URLs")
    for row in rows:
        for key in ("old_sha256", "sha256_v86"):
            if not HASH_RE.fullmatch(row.get(key, "").strip().lower()):
                raise SystemExit(f"Missing/invalid {key} for {row.get('territori', 'unknown')}")
        if not row["url"].startswith("https://"):
            raise SystemExit("Only HTTPS public PDF URLs are permitted")
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
        "possible_2025_2026_with_code": sum(x.get("possible_2025_2026_with_code",0) for x in results),
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
    print(json.dumps({k: report[k] for k in ["total","downloaded","qpdf_clean","extracted_versions","valid_extracted","changed_text_versions","possible_2025_2026_with_code"]}))

if __name__ == "__main__":
    main()
