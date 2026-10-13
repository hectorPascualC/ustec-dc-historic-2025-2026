#!/usr/bin/env python3
"""V53: Audit remaining PADICAT EDUBCN PDFs not read by V45/V47 (archive 2026-01-29).

Read ALL extractable pages; do not store names, applicants, or raw PDF text.
Find only strictly evidenced 507/627/F57/F87 vacancy contextual markers.
A hit is a candidate, NOT proof of a new vacancy; further validation required.
"""
import argparse, concurrent.futures, datetime, hashlib, json, re
from pathlib import Path
import requests
import fitz

CDX = "https://wayback.padicat.cat/cdx"
ROOT = "https://www.edubcn.cat/rcs_gene/seleccio/"
UA = {"User-Agent": "Mozilla/5.0 (public historical Catalan education research; audit metadata only)"}
OLD_EXCLUSIONS = re.compile(r"resultat|resultad|proposta|admes|excl[oò]s|nomenament|tribunal|acta_|resoluci[oó]", re.I)
OLD_GENSEC = re.compile(r"GENSEC|GESEC", re.I)
COURSE = re.compile(r"2025\s*[-/–]\s*2026|curs\s+2025", re.I)
CONTEXT = [
    re.compile(r"(?<!\w)(507)\s*[-–.:]?\s*Inform[aà]tica\b", re.I),
    re.compile(r"\bInform[aà]tica\s*\(\s*(507)\s*\)", re.I),
    re.compile(r"(?<!\w)(627)\s*[-–.:]?\s*Sistemes\s+i\s+aplicacions\s+inform[aà]tiques\b", re.I),
    re.compile(r"\bSistemes\s+i\s+aplicacions\s+inform[aà]tiques\s*\(\s*(627)\s*\)", re.I),
    re.compile(r"\b(?:ESPECIALITAT|PERFIL|CODI\s+D[’']ESPECIALITAT)\s*[:\s]{0,16}(507|627|F57|F87)(?!\w)",re.I),
]
PFI = re.compile(r"(?<!\w)(F57|F87)(?!\w)", re.I)
NOTICE = re.compile(r"d[ií]f[ií]cil\s+(?:provisi[oó]|cobertura)|vacants?\s+i\s+substitucions", re.I)

def load_index():
    r = requests.get(CDX, params={"url":ROOT,"matchType":"prefix","from":"20251101",
        "to":"20260305","output":"json","limit":"500"}, headers=UA, timeout=(12,50))
    r.raise_for_status()
    return [json.loads(line) for line in r.text.splitlines() if line.lstrip().startswith("{")]

def choose(rows):
    selected = {}
    reasons = {}
    for x in rows:
        url = str(x.get("url") or "")
        if not url.lower().startswith(ROOT.lower()) or not url.lower().endswith(".pdf") or str(x.get("status"))!="200":
            continue
        filename = url.rsplit("/",1)[-1]
        if OLD_GENSEC.search(filename):
            reasons["prior_gensec_geSec"] = reasons.get("prior_gensec_geSec",0)+1
            continue
        if not OLD_EXCLUSIONS.search(filename):
            reasons["prior_v47_noncoded"] = reasons.get("prior_v47_noncoded",0)+1
            continue
        selected[url] = {"url":url,"ts":str(x.get("timestamp") or "")}
    return sorted(selected.values(),key=lambda x:x["url"]), reasons

def check(row):
    url,ts=row["url"],row["ts"]
    result = {"url_hash":hashlib.sha256(url.encode()).hexdigest()[:20],
              "valid_pdf":False,"text_extracted":False,"pages":0,
              "pages_read":0,"codes":[],"notice":False,"course":False,
              "sha256":None,"status":None}
    if not re.fullmatch(r"\d{14}",ts):
        result["error"]="invalid_capture_timestamp";return result
    try:
        archive=f"https://wayback.padicat.cat/{ts}id_/{url}"
        r=requests.get(archive,headers=UA,timeout=(12,50))
        result["status"]=r.status_code
        blob=r.content
        if r.status_code!=200 or not blob.startswith(b"%PDF") or len(blob)>11000000:
            return result
        result["valid_pdf"]=True
        result["sha256"]=hashlib.sha256(blob).hexdigest()
        with fitz.open(stream=blob,filetype="pdf") as doc:
            result["pages"]=len(doc)
            # Completeness matters: unlike V47, inspect all extractable pages.
            text="\n".join(doc[i].get_text("text",sort=True) for i in range(len(doc)))
            result["pages_read"]=len(doc)
        result["text_extracted"]=bool(text.strip())
        result["course"]=bool(COURSE.search(text))
        result["notice"]=bool(NOTICE.search(text))
        codes=set()
        for pattern in CONTEXT:
            codes.update(m.group(1).upper() for m in pattern.finditer(text))
        # PFI codes count only where vacancy and 2025-26 course context co-occur.
        if result["course"] and result["notice"]:
            codes.update(m.upper() for m in PFI.findall(text))
        result["codes"]=sorted(codes)
        if codes:
            # Store URL only for contextual matches requiring manual validation.
            result["original_url"]=url
            result["capture_time"]=ts
    except Exception as ex:
        result["error_type"]=type(ex).__name__
    return result

def main(output):
    index=load_index()
    selected, prior=choose(index)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        records=list(pool.map(check,selected))
    candidates=[r for r in records if r["codes"]]
    report={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "archive_scope":"EDUBCN PADICAT 2025-11 to 2026-03 CDX, actual Jan 29 historical PDF captures",
        "cdx_rows":len(index),"prior_group_row_counts":prior,
        "remaining_excluded_by_v47_name_files":len(selected),
        "valid_pdf_downloads":sum(r["valid_pdf"] for r in records),
        "all_pages_read":sum(r["pages_read"] for r in records),
        "pdfs_with_some_extractable_text":sum(r["text_extracted"] for r in records),
        "candidate_count":len(candidates),"candidates":candidates,
        "error_types":{k:sum(r.get("error_type")==k for r in records) for k in sorted({r.get("error_type") for r in records if r.get("error_type")})},
        "http_counts":{str(k):sum(r["status"]==k for r in records) for k in sorted({r["status"] for r in records if r["status"] is not None})},
        "noncandidate_sha256":sorted(set(r["sha256"] for r in records if r["valid_pdf"] and not r["codes"])),
        "limits":["Only files omitted by V47 filename exclusion are audited. 33 GENSEC and 87 noncoded offerlike files were audited in V45 and V47.",
            "A match to a code in text is not independently verified DC offer or date; do not add without opening original evidence.",
            "Some documents may be scans without extractable text. No OCR run.",
            "Captures do not establish posting dates; results may be different documents from offers.",
            "No original PDF text, applicant identifiers, names, phone numbers or emails stored."]}
    dest=Path(output);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps({k:report[k] for k in ("cdx_rows","remaining_excluded_by_v47_name_files",
        "valid_pdf_downloads","all_pages_read","pdfs_with_some_extractable_text","candidate_count")},ensure_ascii=False))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True)
    main(p.parse_args().output)
