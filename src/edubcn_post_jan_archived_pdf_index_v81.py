#!/usr/bin/env python3
"""V81 — PADICAT public PDF captures AFTER the 29 Jan 2026 baseline.

New question: did February-October archived PDFs preserve older 507/627/F57/F87
offers absent in the Jan 29 snapshot? Enumerate only verified official public
directory prefixes, validate PDF payload and compare with known Jan originals.
No personal names, raw body, applicants, or non-target PDFs exported.
"""
import argparse,datetime,hashlib,io,json,re,time
from pathlib import Path
from urllib.parse import urlsplit
import requests,fitz
ROOT=Path(__file__).resolve().parents[1]
CDX="https://wayback.padicat.cat/cdx"
DIRECTORIES=[
 ("seleccio","https://www.edubcn.cat/rcs_gene/seleccio/"),
 ("extra_dc","https://www.edubcn.cat/rcs_gene/extra/03_nomenaments_dificil_cobertura/")
]
HEADERS={"User-Agent":"Mozilla/5.0 (academic study Catalonia archived 2025-26 public teacher vacancies; rate-limited)"}
HINT=re.compile(r"(?i)(?:GENSEC|GESEC|2526|25[-_]26|2025|2026|507|627|F57|F87|informatic|informatica|sistemes)")
TARGET=re.compile(r"(?i)(?:especialitat|especialidad|perfil|codi\s*especialitat|m[oò]dul\s*PFI).{0,35}\b(507|627|F57|F87)\b|\b(507|627|F57|F87)\b\s*[-:]?\s*(?:inform[aà]tic|sistemes\s+i\s+aplicacions)")
CURS=re.compile(r"(?i)(?:2025\s*[-/–]\s*2026|curs\s*2025.2026|\b2526\b)")
UA=HEADERS
def get_cdx(prefix):
    out={"directory":prefix,"http":None,"bytes":0,"count":0,"truncated":False,
         "error":None,"records":[]}
    try:
        r=requests.get(CDX,params={"url":prefix,"matchType":"prefix",
            "from":"20260201","to":"20261014","limit":"4000","output":"json"},
            headers=HEADERS,timeout=(12,43))
        out["http"]=r.status_code;out["bytes"]=len(r.content)
        if r.status_code!=200:
            out["error"]="HTTP_"+str(r.status_code);return out
        for line in r.text.splitlines():
            if not line.strip().startswith("{"):continue
            try:x=json.loads(line)
            except ValueError:continue
            if isinstance(x,dict) and re.fullmatch(r"\d{14}",str(x.get("timestamp") or "")):
                out["records"].append({k:x.get(k) for k in ("url","timestamp","status","mime","digest","length")})
        out["count"]=len(out["records"])
        out["truncated"]=out["count"]>=4000
    except Exception as e:out["error"]=type(e).__name__+": "+str(e)[:180]
    return out
def get_pdf(item):
    result={"original_url":item["url"],"archive_time":item["timestamp"],
      "http":None,"actual_pdf":False,"sha256":None,"pages":None,"target_specialties":[],
      "has_2025_26_course_text":False,"offer_date_markers":[],"error":None}
    u="https://wayback.padicat.cat/"+item["timestamp"]+"id_/"+item["url"]
    try:
        r=requests.get(u,headers=HEADERS,timeout=(12,33),stream=True)
        result["http"]=r.status_code
        if r.status_code!=200:return result
        data=bytearray()
        for chunk in r.iter_content(32768):
            data+=chunk
            if len(data)>6000000:
                result["error"]="too_many_bytes";return result
        blob=bytes(data)
        if not blob.startswith(b"%PDF-"):return result
        with fitz.open(stream=blob,filetype="pdf") as doc:
            text="\n".join(doc[i].get_text(sort=True) for i in range(len(doc)))
            result["pages"]=len(doc)
        result["actual_pdf"]=True
        result["sha256"]=hashlib.sha256(blob).hexdigest()
        result["target_specialties"]=sorted(set((m.group(1) or m.group(2)).upper()
                for m in TARGET.finditer(text)))
        result["has_2025_26_course_text"]=bool(CURS.search(text))
        result["offer_date_markers"]=sorted(set(re.findall(r"(?:2025|2026)[/-]\d\d[/-]\d\d",text)))[:12]
    except Exception as e:result["error"]=type(e).__name__+": "+str(e)[:140]
    return result
def main(output):
    source=json.loads((ROOT/"exports_padicat/EDUBCN_PADICAT_V45_ALL_PDFS.json").read_text(encoding="utf-8"))
    known=set(x["original_url"] for x in source["results"])
    assert len(known)==33,"Known Jan GENSEC original corpus changed"
    groups=[]
    for name,base in DIRECTORIES:
        r=get_cdx(base)
        groups.append({"type":name,"prefix":base,"index":r})
        print(name,"http",r["http"],"capture records",r["count"],flush=True)
        time.sleep(1)
    allrows=[{**x,"group":g["type"]} for g in groups for x in g["index"]["records"]]
    pdf=[x for x in allrows if str(x.get("url") or "").lower().split("?",1)[0].endswith(".pdf")
         and str(x.get("status"))=="200"]
    unique={}
    for x in pdf:
        if x["url"] not in unique or x["timestamp"]<unique[x["url"]]["timestamp"]:
            unique[x["url"]]=x
    not_jan=[x for x in unique.values() if x["url"] not in known]
    shortlist=[x for x in not_jan if HINT.search(urlsplit(x["url"]).path.rsplit("/",1)[-1])]
    checks=[]
    for item in shortlist[:65]:
        x=get_pdf(item)
        checks.append(x)
        print("candidate",item["timestamp"],item["url"].rsplit("/",1)[-1][:70],
            x["http"],"/".join(x["target_specialties"]),flush=True)
        time.sleep(.55)
    possible=[x for x in checks if x["actual_pdf"] and x["target_specialties"] and x["has_2025_26_course_text"]]
    rows_by_month={}
    for r in allrows:
        y=r["timestamp"][:6];rows_by_month[y]=rows_by_month.get(y,0)+1
    result={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "scope":"post-Jan 2026 PADICAT captures in two authentic EDUBCN public PDF directories",
        "jan_original_pdf_url_count":len(known),
        "groups":[{"type":g["type"],"prefix":g["prefix"],
            "http":g["index"]["http"],"response_bytes":g["index"]["bytes"],
            "captures":g["index"]["count"],"truncated":g["index"]["truncated"],
            "error":g["index"]["error"]} for g in groups],
        "index_records":len(allrows),
        "capture_records_by_month":dict(sorted(rows_by_month.items())),
        "unique_valid_status_pdf_urls_indexed":len(unique),
        "pdf_urls_not_in_jan_original_33":len(not_jan),
        "filename_hint_candidate_urls":len(shortlist),
        "hint_candidates_pdf_bodies_checked":len(checks),
        "new_possible_2025_26_target_pdf_bodies":len(possible),
        "new_possible_target_documents":possible,
        "candidate_checks":checks,
        "warnings":["Only EDUBCN archival PDFs after Jan 29 indexed; archive capture date is not actual publication date.",
         "A hit requires exact original document row-level code/dates before adding a census ID.",
         "A 0 exact match can be due to archive scope, no 2025-26 vacancy proof.",
         "Only 65 shortlisted filename-hint candidates inspected if more were returned; not full exhaustive.",
         "Jan corpus 33 originals is subset of 248 Jan archive PDF documents; V53/V56 prior audit for all.",
         "No names/PII or original PDF bodies saved."]}
    p=Path(output);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in ("index_records","unique_valid_status_pdf_urls_indexed",
        "pdf_urls_not_in_jan_original_33","filename_hint_candidate_urls",
        "hint_candidates_pdf_bodies_checked","new_possible_2025_26_target_pdf_bodies")}),flush=True)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",required=True);main(p.parse_args().output)
