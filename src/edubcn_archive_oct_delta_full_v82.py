#!/usr/bin/env python3
"""V82 — Full PDF delta audit: Jan29 vs Oct04 2026 PADICAT EDUBCN snapshots.

Enumerate both actual public CDX corpora, compare URL & archive digest to
avoid recounting Jan's 248 already-audited documents, and inspect ALL October
new or changed PDFs for 2025-26 difficult-coverage 507/627/F57/F87 evidence.
Do NOT export original PDF text, personnel identities, or private data.
"""
import argparse,datetime,hashlib,json,re,time
from pathlib import Path
from urllib.parse import urlsplit
from concurrent.futures import ThreadPoolExecutor,as_completed
import requests,fitz
CDX="https://wayback.padicat.cat/cdx"
DIR="https://www.edubcn.cat/rcs_gene/seleccio/"
WINDOWS={"jan":"20260129","oct":"20261004"}
HEAD={"User-Agent":"Mozilla/5.0 (academic public education archive 2025-26, low-volume metadata research)"}
CODE=re.compile(r"(?<![A-Za-z0-9])(507|627|F57|F87)(?![A-Za-z0-9])",re.I)
EXPLICIT=re.compile(r"(?i)(?:(?:especialitat|especialidad|perf[ií]l|especialitats)[\s:/\-–.]{0,15}(?:[^\n]{0,55}))?\b(507|627|F57|F87)\b\s*[-:/]?\s*(?:inform[aàá]tic|sistemes|sistemas|professor|programa\s+de\s+formaci[oó])|(?:especialitat|especialidad|perf[ií]l)\s*[:\-]?\s*(?:507|627|F57|F87)\b")
COURSE=re.compile(r"(?i)2025\s*[-/–]\s*2026|2025\s*-\s*26|\b2526\b|curs\s*25.26")
DC=re.compile(r"(?i)dif[ií]cil\s+cobertura|dif[ií]cil\s+provisi[oó]|convocat[oò]ria.{0,30}docents?\s+secund[aà]ria")
def index(stamp):
    obj={"date":stamp,"status":None,"bytes":0,"records":None,"truncated":False,"error":None}
    try:
        r=requests.get(CDX,params={"url":DIR,"matchType":"prefix","from":stamp,
           "to":stamp,"output":"json","limit":"2500"},headers=HEAD,timeout=(12,65))
        obj["status"]=r.status_code;obj["bytes"]=len(r.content)
        if r.status_code!=200:obj["error"]="HTTP_"+str(r.status_code);return obj,[]
        rows=[]
        for line in r.text.splitlines():
            if not line.startswith("{"):continue
            try:x=json.loads(line)
            except ValueError:continue
            if isinstance(x,dict) and re.fullmatch(r"\d{14}",str(x.get("timestamp") or "")):
                if x.get("url","").startswith(DIR):
                    rows.append({k:x.get(k) for k in ("url","timestamp","status","mime","digest","length")})
        obj["records"]=len(rows);obj["truncated"]=len(rows)>=2500
        return obj,rows
    except Exception as e:obj["error"]=type(e).__name__+": "+str(e)[:145];return obj,[]
def pdf_records(rows):
    grouped={}
    for row in rows:
        u=str(row.get("url") or "")
        if u.lower().split("?",1)[0].endswith(".pdf") and str(row.get("status"))=="200":
            old=grouped.get(u)
            if old is None or str(row["timestamp"])<str(old["timestamp"]):grouped[u]=row
    return grouped
def fetch(row):
    url=str(row["url"]);stamp=str(row["timestamp"])
    result={"original_url":url,"capture_timestamp":stamp,"status":None,"valid_pdf":False,
      "sha256":None,"pages":None,"target_specialties":[],"has_period_2025_26":False,
      "has_difficult_coverage":False,"pdf_target_evidence":False,"error":None}
    try:
        s=requests.Session()
        r=s.get("https://wayback.padicat.cat/"+stamp+"id_/"+url,
             headers=HEAD,timeout=(12,36),stream=True)
        result["status"]=r.status_code
        if r.status_code!=200:return result
        data=bytearray()
        for block in r.iter_content(32768):
            data.extend(block)
            if len(data)>10000000:result["error"]="limit_10MB";return result
        r.close()
        raw=bytes(data)
        if not raw.startswith(b"%PDF-"):return result
        with fitz.open(stream=raw,filetype="pdf") as d:
            result["pages"]=len(d)
            # parse up to 55 pages to bound exceptionally long personnel lists
            txt="\n".join(d[i].get_text(sort=True) for i in range(min(len(d),55)))
        result["valid_pdf"]=True;result["sha256"]=hashlib.sha256(raw).hexdigest()
        result["target_specialties"]=sorted(set(c.upper() for c in EXPLICIT.findall(txt)))
        result["has_period_2025_26"]=bool(COURSE.search(txt))
        result["has_difficult_coverage"]=bool(DC.search(txt))
        result["pdf_target_evidence"]=bool(result["target_specialties"] and result["has_period_2025_26"]
          and (result["has_difficult_coverage"] or bool(re.search(r"(?i)GENSEC|GESEC",url))))
    except Exception as e:result["error"]=type(e).__name__+": "+str(e)[:135]
    return result
def main(dest):
    checks={};snap={}
    for k,st in WINDOWS.items():
        meta,rows=index(st);checks[k]=meta;snap[k]=pdf_records(rows)
        print(k,meta["status"],meta["records"],"PDF URL",len(snap[k]),flush=True)
        time.sleep(.6)
    jan=snap["jan"];octo=snap["oct"]
    jan_urls=set(jan);oct_urls=set(octo)
    newer=oct_urls-jan_urls
    common=oct_urls&jan_urls
    modified={u for u in common if jan[u].get("digest") and octo[u].get("digest")
                   and jan[u]["digest"]!=octo[u]["digest"]}
    equal={u for u in common if jan[u].get("digest")==octo[u].get("digest")}
    required=sorted(newer|modified)
    if len(required)>650:raise RuntimeError("Excessive archive delta: bound workload and inspect manually")
    results=[]
    if checks["jan"]["status"]==200 and checks["oct"]["status"]==200 and not checks["jan"]["truncated"] and not checks["oct"]["truncated"]:
        # At most 3 simultaneous requests to public archive; no bulk raw-data retention.
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures={pool.submit(fetch,octo[url]):url for url in required}
            for ix,future in enumerate(as_completed(futures),1):
                try:res=future.result()
                except Exception as e:res={"original_url":futures[future],
                           "error":"worker_"+type(e).__name__}
                results.append(res)
                if ix%20==0 or res.get("pdf_target_evidence"):
                    print("processed",ix,"/",len(required),"possible",sum(x.get("pdf_target_evidence",False) for x in results),flush=True)
    valid=sum(bool(x.get("valid_pdf")) for x in results)
    found=[x for x in results if x.get("pdf_target_evidence")]
    report={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "scope":"Full Jan29 vs Oct04 PADICAT EDUBCN /rcs_gene/seleccio/ PDF capture comparison",
      "archive_cdx":checks,"jan_distinct_pdf_urls":len(jan),
      "oct_distinct_pdf_urls":len(octo),"oct_url_already_in_jan":len(common),
      "oct_urls_not_in_jan":len(newer),"same_url_archive_digest_changed":len(modified),
      "same_url_digest_unchanged":len(equal),
      "delta_unique_pdf_urls_to_read":len(required),
      "delta_pdf_bodies_read":len(results),"valid_pdf_bodies":valid,
      "possible_2025_26_507_627_pfi_pdf_count":len(found),
      "candidate_2025_26_documents":found,
      "delta_checks":results,
      "warnings":["All Jan PDFs were text-scanned previously in V53/V56; only Oct new/changed PDF bodies re-read.",
        "Each match must be checked against explicit DC vacancy code and publication time prior to census addition.",
        "PDF archive time is not original public posting time; archive metadata is not proof of month.",
        "A PDF without 2025-26 text may nonetheless have a real 2025-26 offer; recall heuristic limits.",
        "Exact codes 507/627/F57/F87 in arbitrary administrative files can be false positives.",
        "No actual PDF bytes or applicant names/identities/bare staff details stored."]}
    p=Path(dest);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:report[k] for k in ("jan_distinct_pdf_urls","oct_distinct_pdf_urls",
      "oct_urls_not_in_jan","same_url_archive_digest_changed",
      "delta_pdf_bodies_read","valid_pdf_bodies","possible_2025_26_507_627_pfi_pdf_count")}),flush=True)
if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("--output",required=True);main(a.parse_args().output)
