#!/usr/bin/env python3
"""Bounded Common Crawl historical DC CDXJ search and safe WARC byte-range fetch.

No bulk queries or proxy rotation; stop at consecutive HTTP 503.
A WARC record must be returned with HTTP 206 and a genuine PDF magic header.
No applicant names or PDF full text are written into a public repository.
"""
import argparse,datetime,hashlib,io,json,re,time
from pathlib import Path
from urllib.parse import quote
import requests

COLLECTIONS=["CC-MAIN-2025-47","CC-MAIN-2025-51","CC-MAIN-2026-04","CC-MAIN-2026-08"]
ORIGIN="https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/"
TARGETS=[
 ("Barcelonès","exact",ORIGIN+"barcelones/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/Barcelones-SEC-dificil-cobertura-oferta-vacants_07112025.pdf"),
 ("Girona","prefix",ORIGIN+"girona/personal-docent/nomenaments-telematics/dificil-cobertura/"),
 ("Catalunya Central","prefix",ORIGIN+"catalunya-central/personal-docent/nomenaments-telematics/dificil-cobertura/")
]
UA="Mozilla/5.0 (public-archive historical DC PDF research; slow low-impact requests)"
def parse_cdx(text):
 out=[]
 for line in text.splitlines():
  try:
   o=json.loads(line.strip())
   if isinstance(o,dict):out.append(o)
  except (ValueError,TypeError):pass
 return out
def query(coll,territory,kind,url):
 out={"collection":coll,"territory":territory,"match":kind,"target":url,
      "status":None,"records":[],"bytes":0}
 q=f"https://index.commoncrawl.org/{coll}-index"
 p={"url":url if kind=="exact" else url+"*","output":"json","filter":"status:200","pageSize":"25"}
 try:
  r=requests.get(q,params=p,timeout=(10,32),headers={"User-Agent":UA,"Accept":"application/json,text/plain"})
  out["status"]=r.status_code;out["bytes"]=len(r.content)
  if r.status_code==200:
   rows=parse_cdx(r.text)
   for row in rows[:25]:
    out["records"].append({k:row.get(k) for k in
      ("url","timestamp","status","mime","mime-detected","digest","filename","offset","length")})
  elif r.status_code==503:out["error"]="503 rate limiting: stop consecutive requests"
  elif r.status_code not in (404,):out["error"]="non-success CDX HTTP "+str(r.status_code)
 except Exception as ex:out["error"]=type(ex).__name__+": "+str(ex)[:170]
 return out
def download_warc(entry):
 out={"original_url":entry.get("url"),"capture_at":entry.get("timestamp"),
      "downloaded":False,"is_pdf":False,"sha256":None,"pages":0,
      "target_codes":[],"has_2025":False,"has_2026":False}
 try:
  filename=entry.get("filename")
  if not filename or not re.match(r"^crawl-data/CC-MAIN-[0-9-]+/",filename):return {**out,"error":"missing/untrusted WARC file"}
  offset=int(entry.get("offset","-1"));length=int(entry.get("length","0"))
  if not(0<=offset and 100<=length<=3_000_000):return {**out,"error":"no safe byte range"}
  endpoint="https://data.commoncrawl.org/"+filename
  r=requests.get(endpoint,headers={"Range":f"bytes={offset}-{offset+length-1}","User-Agent":UA},
                 timeout=(12,40),stream=True)
  out["http"]=r.status_code
  if r.status_code!=206:
   r.close();return {**out,"error":"expected HTTP 206 byte-range, refused full WARC"}
  compressed=bytearray()
  for part in r.iter_content(16384):
   compressed.extend(part)
   if len(compressed)>length+100:raise ValueError("slice exceeded advertised byte length")
  r.close()
  from warcio.archiveiterator import ArchiveIterator
  records=list(ArchiveIterator(io.BytesIO(compressed)))
  if not records:return {**out,"error":"no valid WARC record"}
  data=records[0].content_stream().read(9_000_000)
  out["downloaded"]=True;out["is_pdf"]=data.startswith(b"%PDF-")
  if not out["is_pdf"]:return {**out,"error":"WARC payload is not a PDF"}
  out["sha256"]=hashlib.sha256(data).hexdigest()
  import fitz
  document=fitz.open(stream=data,filetype="pdf")
  out["pages"]=len(document)
  txt="\n".join(document[i].get_text("text") for i in range(min(40,len(document))))
  document.close()
  out["target_codes"]=sorted(set(re.findall(r"(?<!\w)(507|627|F57|F87)(?!\w)",txt,re.I)))
  out["has_2025"]=bool(re.search(r"(?<!\d)2025(?!\d)",txt))
  out["has_2026"]=bool(re.search(r"(?<!\d)2026(?!\d)",txt))
 except Exception as e:out["error"]=type(e).__name__+": "+str(e)[:145]
 return out
def run(output):
 queried=[];status503=0;stop=False
 # Limit the entire run to 12 sequential queries, no concurrency.
 for coll in COLLECTIONS:
  if stop:break
  for territory,kind,url in TARGETS:
   row=query(coll,territory,kind,url)
   queried.append(row)
   print(f'{coll} {territory} HTTP={row["status"]} hits={len(row["records"])}',flush=True)
   if row["status"]==503:status503+=1
   else:status503=0
   if status503>=2:
    stop=True
    print("Two consecutive 503 responses: stop; not an absence claim.",flush=True)
    break
   time.sleep(8.0)
 hits=[x for row in queried for x in row["records"] if
       ".pdf" in (x.get("url") or "").lower() and
       "dificil-cobertura" in (x.get("url") or "").lower()]
 seen=set();pdf_records=[]
 for x in hits:
  key=(x.get("url"),x.get("timestamp"),x.get("digest"))
  if key not in seen:pdf_records.append(x);seen.add(key)
 checked=[download_warc(x) for x in pdf_records[:3]]
 result={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "collections":COLLECTIONS,"queries":queried,"queries_executed":len(queried),
         "stopped_due_to_503":stop,"total_index_records":sum(len(x["records"]) for x in queried),
         "unique_pdf_index_records":len(pdf_records),
         "warc_download_attempts":len(checked),"verified_pdfs":sum(x["is_pdf"] for x in checked),
         "warc_pdfs":checked,
         "warnings":["Index CDX failures do not demonstrate no original DC offers existed.",
           "A WARC capture timestamp is not the original publication date.",
           "PDF specialty code mentioned somewhere in a document needs row-level verification.",
           "Only anonymized metadata and SHA256, never PDF contents or personnel, are exported."]}
 p=Path(output);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({k:result[k] for k in
    ("queries_executed","stopped_due_to_503","total_index_records","verified_pdfs")},ensure_ascii=False))
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--output",required=True)
 args=ap.parse_args();run(args.output)
