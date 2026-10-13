#!/usr/bin/env python3
"""V62 — bounded Common Crawl index check of 11 REAL dated Barcelones PDFs.

Only authentic URL list V22. Match each PDF with contemporaneous Common Crawl
collections plus March 2026 captures of February documents. Never treat errors
or 404 for a given crawl as no offers. On actual WARC metadata, independently
validate retrieved PDF payload before asserting historic recovery.
"""
import argparse,csv,datetime,gzip,hashlib,io,json,re,time
from pathlib import Path
import requests
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"cens/INDEX_PDFS_BCO_V22_11_LOTS.csv"
UA={"User-Agent":"Mozilla/5.0 (public historical educational PDF research; noncommercial; low rate)"}
COLLECTIONS=[
 "CC-MAIN-2025-47","CC-MAIN-2025-51","CC-MAIN-2026-04",
 "CC-MAIN-2026-08","CC-MAIN-2026-12"
]
def collection_for(date):
 if date<"2025-11-21":return "CC-MAIN-2025-47"
 if date<"2025-12-31":return "CC-MAIN-2025-51"
 if date<"2026-02-01":return "CC-MAIN-2026-04"
 if date<"2026-02-20":return "CC-MAIN-2026-08"
 return "CC-MAIN-2026-12"
def sources():
 with SOURCE.open(encoding="utf-8-sig",newline="") as f:
  records=list(csv.DictReader(f))
 assert len(records)==11,"V22 has changed; audit source before execution"
 for r in records:
  assert r["origen"].startswith("https://educacio.gencat.cat/") and r["origen"].endswith(".pdf")
 return records
def query(coll,row):
 url=row["origen"]
 meta={"date_nominal":row["data_nom_fitxer"],"filename":row["pdf_nom"],
       "original_url":url,"collection":coll,"status":None,"records":[]}
 try:
  r=requests.get("https://index.commoncrawl.org/"+coll+"-index",
      params={"url":url,"output":"json"},headers=UA,timeout=(9,21))
  meta["status"]=r.status_code
  if r.status_code==200:
   for line in r.text.splitlines()[:15]:
    try:item=json.loads(line)
    except ValueError:continue
    if isinstance(item,dict) and "filename" in item:
     meta["records"].append({k:item.get(k) for k in
       ("url","timestamp","status","mime","mime-detected","filename","offset","length","digest")})
  elif r.status_code==404:
   try:msg=r.json().get("error","")
   except Exception:msg=r.text[:100]
   meta["no_capture_returned"]=str(msg)[:150]
  else:meta["error"]="http_"+str(r.status_code)+" "+r.text[:130]
 except Exception as e:meta["error"]=type(e).__name__+": "+str(e)[:160]
 return meta
def inspect_warc(rec):
 out={"record_url":rec.get("url"),"timestamp":rec.get("timestamp"),
   "pdf_verified":False,"sha256":None,"bytes":0,"pages":0,
   "has_2025_26":False,"specialty_codes":[]}
 try:
  filename=rec.get("filename") or ""
  if not re.fullmatch(r"crawl-data/CC-MAIN-[0-9-]+/[A-Za-z0-9_./-]+\.warc\.gz",filename):
   out["error"]="unsafe WARC filename";return out
  offset=int(rec.get("offset") or "-1");length=int(rec.get("length") or "0")
  if not(0<=offset and 100<=length<=3500000):
   out["error"]="invalid WARC byte-range";return out
  r=requests.get("https://data.commoncrawl.org/"+filename,
       headers={"Range":f"bytes={offset}-{offset+length-1}",**UA},
       timeout=(10,35))
  if r.status_code!=206:
   out["error"]="WARC_range_http_"+str(r.status_code);return out
  from warcio.archiveiterator import ArchiveIterator
  body=r.content
  if len(body)>length+128:
   out["error"]="exceeded_range";return out
  for record in ArchiveIterator(io.BytesIO(body)):
   if record.rec_type=="response":
    payload=record.content_stream().read(15000000)
    if not payload.startswith(b"%PDF-"):
     out["error"]="non-PDF payload";return out
    import fitz
    out["pdf_verified"]=True
    out["sha256"]=hashlib.sha256(payload).hexdigest()
    out["bytes"]=len(payload)
    with fitz.open(stream=payload,filetype="pdf") as d:
     out["pages"]=len(d)
     text="\n".join(d[i].get_text() for i in range(len(d)))
    out["has_2025_26"]=bool(re.search(r"2025\s*[-/–]\s*2026",text,re.I))
    out["specialty_codes"]=sorted(set(re.findall(r"(?<!\w)(507|627|F57|F87)(?!\w)",text,re.I)))
    return out
  out["error"]="no WARC response record"
 except Exception as e:out["error"]=type(e).__name__+": "+str(e)[:160]
 return out

def main(out):
 rows=sources()
 jobs=[(collection_for(r["data_nom_fitxer"]),r) for r in rows]
 # Follow-up index March for Feb lots only, if the PDF persisted
 jobs.extend(("CC-MAIN-2026-12",r) for r in rows
     if r["data_nom_fitxer"]>="2026-02-01" and collection_for(r["data_nom_fitxer"])!="CC-MAIN-2026-12")
 result=[]
 streak_bad=0;stopped=False
 for coll,row in jobs:
  a=query(coll,row);result.append(a)
  print(f'{coll} {row["pdf_nom"]} {a["status"]} hits={len(a["records"])}',flush=True)
  streak_bad=streak_bad+1 if a["status"] in (429,502,503,504) else 0
  if streak_bad>=2:
   stopped=True;break
  time.sleep(1.4)
 hits=[]
 seen=set()
 for query_result in result:
  for rec in query_result["records"]:
   key=(rec.get("url"),rec.get("timestamp"),rec.get("digest"))
   if key not in seen:
    hits.append(rec);seen.add(key)
 scans=[inspect_warc(r) for r in hits[:4]]
 output={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "source_file":str(SOURCE.relative_to(ROOT)),"known_dated_pdf_urls":len(rows),
 "planned_queries":len(jobs),"executed_queries":len(result),"stopped_due_to_server_backoff":stopped,
 "successful_index_queries":sum(x["status"]==200 for x in result),
 "explicit_no_captures_404":sum(x["status"]==404 for x in result),
 "blocked_index_queries":sum(x["status"] not in (200,404) for x in result),
 "index_records":sum(len(x["records"]) for x in result),
 "unique_warc_records":len(hits),"warc_downloads_tested":len(scans),
 "verified_historical_pdf_bodies":sum(x["pdf_verified"] for x in scans),
 "queries":result,"warc_checks":scans,
 "warnings":["Only a defined sample of dated official files and dated crawl collections; not a full CC archive search.",
    "HTTP 404 No Captures means only this collection's index has none for an exact URL.",
    "429/5xx failures are technical blocks. Archive timestamp is not publication date.",
    "Do not add a new vacancy just because an ID appears again; verify original source and publication date.",
    "Do not publicly archive any complete original WARC/PDF bodies, text or personal applicant information."]}
 p=Path(out);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(output,indent=2,ensure_ascii=False),encoding="utf-8")
 print(json.dumps({k:output[k] for k in ("planned_queries","executed_queries","stopped_due_to_server_backoff",
   "explicit_no_captures_404","blocked_index_queries","unique_warc_records","verified_historical_pdf_bodies")}),flush=True)
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--output",required=True);main(p.parse_args().output)
