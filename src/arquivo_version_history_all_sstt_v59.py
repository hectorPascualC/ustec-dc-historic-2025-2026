#!/usr/bin/env python3
"""V59 — Arquivo.pt URL versionHistory across all official SSTT document URLs.

Input: existing 30 confirmed 2026 PDF URLs in exports_territorial/SSTT_PDFS.csv.
No guessed endpoints and no private data. Unfiltered versionHistory is deliberate:
Arquivo.pt's optional 'to' filter has previously returned unexplained zeros.
"""
import argparse,csv,datetime,hashlib,io,json,re,time
from pathlib import Path
from urllib.parse import urlsplit
import requests
import fitz

API="https://arquivo.pt/textsearch"
INPUT="exports_territorial/SSTT_PDFS.csv"
UA={"User-Agent":"Mozilla/5.0 (public educational archive URL version history research; bounded requests)"}
COURSE25=re.compile(r"curs\s*(?:2025\s*[-/–]\s*2026|25\s*[-/–]\s*26)|2025\s*[-/–]\s*2026",re.I)
COURSE26=re.compile(r"curs\s*(?:2026\s*[-/–]\s*2027|26\s*[-/–]\s*27)|2026\s*[-/–]\s*2027",re.I)
SPECIALTY=re.compile(r"(?<!\w)(?:507|627|F57|F87)(?!\w)",re.I)
CONTROL="https://educacio.gencat.cat/"
EXTRA=[
 ("Consorci d'Educacio de Barcelona","https://www.edubcn.cat/rcs_gene/seleccio/GESEC2526_147_INS_ESCOLA_DEL_TREBALL_627.pdf"),
 ("Consorci d'Educacio de Barcelona","https://www.edubcn.cat/rcs_gene/seleccio/GESEC2526_167_INS_PEDRALBES_507_INFORMATICA.pdf"),
]

def inventory():
    with open(INPUT,encoding="utf-8-sig",newline="") as f:
        data=list(csv.DictReader(f))
    unique={}
    for x in data:
        url=x.get("url","")
        if url.startswith(("http://","https://")) and url.lower().endswith(".pdf"):
            unique[url]={"territory":x.get("territori") or "", "kind":x.get("tipus") or ""}
    for territory,url in EXTRA:
        unique[url]={"territory":territory,"kind":"historical_control"}
    return [{"url":u,**a} for u,a in sorted(unique.items())]

def get_history(url):
    result={"api_http":None,"estimated_total":None,"returned":0,"error":None,"captures":[]}
    try:
        r=requests.get(API,params={"versionHistory":url,"maxItems":"50"},
            timeout=(12,34),headers=UA)
        result["api_http"]=r.status_code
        if r.status_code!=200:return result
        body=r.json()
        items=body.get("response_items") or []
        result["estimated_total"]=body.get("estimated_nr_results")
        result["returned"]=len(items)
        for item in items:
            t=str(item.get("tstamp") or "")
            if not re.fullmatch(r"\d{14}",t):continue
            result["captures"].append({"timestamp":t,
                "original_url":str(item.get("originalURL") or ""),
                "archive_file":str(item.get("linkToOriginalFile") or ""),
                "mime":str(item.get("mimeType") or ""),
                "status":str(item.get("statusCode") or ""),
                "source_digest":str(item.get("digest") or "")})
    except Exception as exc:
        result["error"]=type(exc).__name__+": "+str(exc)[:150]
    return result

def inspect_pdf(cap):
    out={"capture_at":cap["timestamp"],"pdf_ok":False,"sha256":None,
        "page_count":0,"mentions_course_2025_26":False,
        "mentions_course_2026_27":False,"codes":[],"download_error":None}
    if cap["status"]!="200" or not cap["archive_file"].startswith("https://arquivo.pt/"):
        out["download_error"]="not_200_or_not_archived_file";return out
    try:
        r=requests.get(cap["archive_file"],headers=UA,timeout=(12,40))
        if r.status_code!=200 or not r.content.startswith(b"%PDF-"):
            out["download_error"]="HTTP_"+str(r.status_code)+"_or_not_pdf";return out
        blob=r.content
        if len(blob)>12000000:
            out["download_error"]="size_limit_exceeded";return out
        out["pdf_ok"]=True;out["sha256"]=hashlib.sha256(blob).hexdigest()
        with fitz.open(stream=blob,filetype="pdf") as doc:
            out["page_count"]=len(doc)
            text="\n".join(doc[i].get_text(sort=True) for i in range(len(doc)))
        out["mentions_course_2025_26"]=bool(COURSE25.search(text))
        out["mentions_course_2026_27"]=bool(COURSE26.search(text))
        out["codes"]=sorted({m.upper() for m in SPECIALTY.findall(text)})
    except Exception as exc:
        out["download_error"]=type(exc).__name__+": "+str(exc)[:130]
    return out

def main(dest):
    cases=inventory()
    checks=[]
    control=get_history(CONTROL)
    print("CONTROL root",control["api_http"],control["returned"],flush=True)
    for i,x in enumerate(cases):
        hist=get_history(x["url"])
        verified=[]
        for cap in hist["captures"]:
            if cap["mime"].lower() in ("application/pdf","application/x-pdf") and cap["status"]=="200":
                verified.append(inspect_pdf(cap))
        checks.append({**x,"history":hist,"pdf_inspections":verified})
        print(f"[{i+1}/{len(cases)}] {x['territory']}: {hist['returned']} archived; {sum(v['pdf_ok'] for v in verified)} PDFs",flush=True)
        time.sleep(.55)
    result={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "archive":"Arquivo.pt documented versionHistory public API",
        "method":"exact confirmed official PDF URLs from V24, never inferred locations",
        "control_homepage":{"http":control["api_http"],"version_count":control["returned"],
            "captures":[{"timestamp":x["timestamp"],"status":x["status"]}
            for x in control["captures"][:8]]},
        "checked_urls":len(cases),
        "territories":sorted({x["territory"] for x in cases}),
        "archive_versions_found":sum(x["history"]["returned"] for x in checks),
        "pdf_binaries_recovered":sum(sum(y["pdf_ok"] for y in x["pdf_inspections"]) for x in checks),
        "historical_pdfs_flagged":sum(sum(y["pdf_ok"] and y["mentions_course_2025_26"] for y in x["pdf_inspections"]) for x in checks),
        "checks":checks,
        "warnings":["A working archive control does not establish complete territorial capture coverage.",
            "2025-26 result PDF is not original vacancy posting, nor does a PDF timestamp establish publication date.",
            "Inputs came only from verified existing official PDF links in repo; current PDF versions are overwritten.",
            "Public output excludes original PDF contents, names, addresses, ID document numbers and private data.",
            "If estimated_total > returned, pagination is pending and this check is not exhaustive."]
    }
    path=Path(dest);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps({k:result[k] for k in ("checked_urls","territories","archive_versions_found",
        "pdf_binaries_recovered","historical_pdfs_flagged")},ensure_ascii=False))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True)
    main(p.parse_args().output)
