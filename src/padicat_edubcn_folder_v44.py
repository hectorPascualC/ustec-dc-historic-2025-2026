#!/usr/bin/env python3
"""Search PADICAT public CDX per month for historic EDUBCN DC original PDFs.

Search the actual selection-document directory, not just the Jan29 frontend
snapshot's links. Return document metadata and specialty hints, no applicant data.
"""
import argparse,datetime,json,re,time
from pathlib import Path
import requests
CDX="https://wayback.padicat.cat/cdx"
DIRECTORIES=[
 "https://www.edubcn.cat/rcs_gene/seleccio/",
 "http://www.edubcn.cat/rcs_gene/seleccio/",
 "https://www.edubcn.cat/rcs_gene/extra/03_nomenaments_dificil_cobertura/",
]
MONTHS=[("20251101","20251130"),("20251201","20251231"),("20260101","20260131"),("20260201","20260228")]
UA={"User-Agent":"Mozilla/5.0 (low frequency noncommercial historical Catalonia DC document index research)"}
def get_index(path,lo,hi):
 out={"url":path,"from":lo,"to":hi,"status":None,"records":[]}
 try:
  r=requests.get(CDX,params={"url":path,"matchType":"prefix","from":lo,"to":hi,"limit":"900","output":"json"},
    timeout=(10,31),headers=UA)
  out["status"]=r.status_code;out["response_bytes"]=len(r.content)
  if r.status_code==200:
   for s in r.text.splitlines():
    try:
     x=json.loads(s)
     if isinstance(x,dict):
      o={k:x.get(k) for k in ("timestamp","url","status","mime","digest","length","source-coll")}
      out["records"].append(o)
    except ValueError:pass
   out["hit_limit"]=len(out["records"])>=900
 except Exception as e:out["error"]=type(e).__name__+": "+str(e)[:150]
 return out
def match(row):
 u=(row.get("url") or "").lower()
 # Require original PDF URL and original HTTP response status 200
 if not ".pdf" in u:return False
 if str(row.get("status",""))!="200":return False
 if not "edubcn.cat" in u:return False
 return bool(re.search(r"(?:^|[/_.-])(?:507|627|f57|f87)(?:[/_.-]|$)",u))
def run(path):
 results=[]
 for base in DIRECTORIES:
  for a,b in MONTHS:
   r=get_index(base,a,b);results.append(r)
   print(f'{base[8:47]:39s} {a[:6]} HTTP={r["status"]} n={len(r["records"])}',flush=True)
   time.sleep(.65)
 records=[{**x,"query_url":r["url"]} for r in results for x in r["records"]]
 pdf=[x for x in records if ".pdf" in (x.get("url") or "").lower() and str(x.get("status"))=="200"]
 matches=[x for x in pdf if match(x)]
 seen=set();unique=[]
 for x in matches:
  key=(x.get("url"),x.get("timestamp"))
  if key not in seen:seen.add(key);unique.append(x)
 report={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "scope":"historic archive captures 2025-11-01 to 2026-02-28, 3 authentic EDUBCN PDF paths",
  "queries": [{k:r[k] for k in ("url","from","to","status","response_bytes")} |
     {"capture_count":len(r["records"]),"hit_limit":r.get("hit_limit",False),"error":r.get("error","")} for r in results],
  "query_count":len(results),"all_capture_records":len(records),
  "valid_pdf_capture_records":len(pdf),"target_pdf_filename_hits":len(unique),
  "target_pdf_metadata":unique[:300],
  "unique_target_urls":len(set(x.get("url") for x in unique)),
  "warnings":["Filename code matches are candidate evidence only; PDF must be independently parsed before census admission.",
  "Archive capture timestamp not original publication date.",
  "Queries may be incomplete when hit_limit is true, or content archived on alternative hosts.",
  "Only public source URLs and archive metadata saved; no candidate or teacher details."]}
 out=Path(path);out.parent.mkdir(parents=True,exist_ok=True)
 out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({k:report[k] for k in ("query_count","all_capture_records","valid_pdf_capture_records","unique_target_urls")}))
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--output",required=True)
 run(p.parse_args().output)
