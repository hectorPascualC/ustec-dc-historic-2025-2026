#!/usr/bin/env python3
"""Forensic scan for internal incremental revisions in public Generalitat DC PDFs.
No names, applicants, PDF bodies or previous-version binaries are published.
A PDF that has been fully replaced on the server cannot be restored this way.
"""
import argparse,csv,datetime,hashlib,io,json,re,requests,time
from pathlib import Path
import fitz
INPUT="exports_territorial/SSTT_PDFS.csv"
DATE2025=re.compile(r"\b2025\b")
DATE2026=re.compile(r"\b2026\b")
CODES=re.compile(r"(?<![\w\d])(?:507|627|F57|F87)(?![\w\d])",re.I)
MAX_BYTES=14000000
def load(path):
 with Path(path).open(encoding="utf-8-sig",newline="") as f:
  return list(csv.DictReader(f))
def probe(row):
 url=row.get("url","")
 territory=row.get("territori","")
 o={"territori":territory,"url":url,"http":None,"is_pdf":False,
    "bytes":0,"sha256":"","eof_markers":0,"prev_key_count":0,
    "version_candidates_checked":0,"valid_prior_revisions":0,
    "prior_revisions_with_changed_text":0,"prior_revisions_with_2025":0,
    "prior_revisions_with_2026":0,"prior_revisions_with_specialty_codes":[]}
 try:
  req=requests.get(url,headers={"User-Agent":"Mozilla/5.0 (historical DC public PDF forensic research)"},timeout=22)
  o["http"]=req.status_code
  data=req.content[:MAX_BYTES+1]
  o["bytes"]=len(data)
  if req.status_code!=200 or not data.startswith(b"%PDF") or len(data)>MAX_BYTES:return o
  o["is_pdf"]=True;o["sha256"]=hashlib.sha256(data).hexdigest()
  eof=list(re.finditer(rb"%%EOF",data))
  o["eof_markers"]=len(eof)
  o["prev_key_count"]=len(list(re.finditer(rb"/Prev\b",data)))
  latest=fitz.open(stream=data,filetype="pdf")
  o["latest_pages"]=len(latest)
  latest_text="\n".join(latest[i].get_text("text") for i in range(min(40,len(latest))))
  latest.close()
  for cut in eof[:-1][-6:]:
   # Candidate historic file is bytes up to this prior EOF marker.
   # Detect false positives by genuinely opening and comparing real page texts.
   prior=data[:cut.end()]+b"\n"
   o["version_candidates_checked"]+=1
   try:
    d=fitz.open(stream=prior,filetype="pdf")
    if len(d)==0 or d.is_repaired: d.close();continue
    older="\n".join(d[i].get_text("text") for i in range(min(40,len(d))))
    d.close()
    if not older.strip():continue
    o["valid_prior_revisions"]+=1
    if older!=latest_text:o["prior_revisions_with_changed_text"]+=1
    if DATE2025.search(older):o["prior_revisions_with_2025"]+=1
    if DATE2026.search(older):o["prior_revisions_with_2026"]+=1
    o["prior_revisions_with_specialty_codes"]=sorted(set(o["prior_revisions_with_specialty_codes"]+CODES.findall(older.upper())))
   except Exception:continue
 except Exception as e:o["error_type"]=type(e).__name__
 return o
def main():
 p=argparse.ArgumentParser();p.add_argument("--input",default=INPUT);p.add_argument("--output",required=True);arg=p.parse_args()
 rows=load(arg.input)
 out=[];seen=set()
 for row in rows:
  url=row.get("url","")
  if url in seen:continue
  seen.add(url)
  item=probe(row);out.append(item)
  print(f'{item["territori"]}: HTTP {item["http"]}, eof={item["eof_markers"]}, valid_old={item["valid_prior_revisions"]}',flush=True)
  time.sleep(.25)
 report={"checked_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"dataset":arg.input,
   "documents_checked":len(out),
   "downloaded_pdfs":sum(x["is_pdf"] for x in out),
   "multi_eof_files":sum(x["eof_markers"]>1 for x in out),
   "genuine_prior_versions_opened":sum(x["valid_prior_revisions"] for x in out),
   "prior_versions_with_changed_text":sum(x["prior_revisions_with_changed_text"] for x in out),
   "files_with_changed_prior_text":sum(x["prior_revisions_with_changed_text"]>0 for x in out),
   "potential_2025_2026_candidates":sum(x["prior_revisions_with_changed_text"]>0 and x["prior_revisions_with_2025"]>0 for x in out),
   "files":out,
   "warnings":[
    "Different PDF revisions are not necessarily from different publication dates.",
    "2025 mentioned in document text does not establish historical publication.",
    "An old URL reused for a fully replaced file cannot be reversed using PDFResurrect.",
    "Multiple EOF markers alone can appear for reasons other than actual historic changes.",
    "No applicant or teacher content is exported."],
   "historical_census_complete":False}
 f=Path(arg.output);f.parent.mkdir(parents=True,exist_ok=True)
 f.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({k:report[k] for k in ["documents_checked","downloaded_pdfs","multi_eof_files","genuine_prior_versions_opened","files_with_changed_prior_text","potential_2025_2026_candidates"]},ensure_ascii=False))
if __name__=="__main__":main()
