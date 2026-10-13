#!/usr/bin/env python3
"""V47: Find 507/627/F57/F87 hiding in archived non-GENSEC EDUBCN PDF contents.

Search public PADICAT snapshots, never current API. No private names/content
persisted. Target detection requires explicit profile/specialty vicinity or
the unabbreviated specialty title; digit occurrence alone is insufficient.
"""
import argparse,concurrent.futures,datetime,hashlib,json,re,time
from pathlib import Path
from urllib.parse import urlsplit
import requests,fitz
CDX="https://wayback.padicat.cat/cdx"
ROOT="https://www.edubcn.cat/rcs_gene/seleccio/"
COUPLES={"507":re.compile(r"507\s*[-–:]?\s*inform[aà]tica",re.I),
 "627":re.compile(r"627\s*[-–:]?\s*sistemes\s+i\s+aplicacions\s+inform[aà]tiques",re.I),
 "F57":re.compile(r"(?<!\w)F57(?!\w)",re.I),
 "F87":re.compile(r"(?<!\w)F87(?!\w)",re.I)}
LABEL=re.compile(r"(?:codi\s+d[’']especialitat|especialitat|perfil\s+professional|especialitat\s+docent)[^\n]{0,70}?\b(507|627|F57|F87)\b",re.I)
BEFORE=re.compile(r"\b(507|627|F57|F87)\b[^\n]{0,60}(?:codi\s+d[’']especialitat|especialitat|perfil)",re.I)
COURSE=re.compile(r"2025\s*[-/–]\s*2026|curs\s+2025",re.I)
DATES=re.compile(r"\b[0-3]?\d[/.-][01]?\d[/.-]20(?:25|26)\b")
def get_index():
 r=requests.get(CDX,params={"url":ROOT,"matchType":"prefix","from":"20251101","to":"20260305","limit":"500","output":"json"},
       timeout=(14,40),headers={"User-Agent":"Mozilla/5.0 (public Catalan historic education archive)"})
 if r.status_code!=200:raise RuntimeError("PADICAT archive index HTTP "+str(r.status_code))
 return [json.loads(s) for s in r.text.splitlines() if s.lstrip().startswith("{")]
def entries(raw):
 unique={};excluded=re.compile(r"GENSEC|GESEC",re.I)
 for item in raw:
  url=str(item.get("url",""))
  if not url.lower().startswith(ROOT.lower()) or not url.lower().endswith(".pdf") or item.get("status")!="200":continue
  basename=url.rsplit("/",1)[-1]
  if excluded.search(basename):continue
  if re.search(r"resultat|resultad|proposta|admes|excl[oò]s|nomenament|tribunal|acta_|resoluci[oó]",basename,re.I):continue
  unique[url]={"url":url,"ts":str(item.get("timestamp",""))}
 return list(unique.values())
def inspect(item):
 url,ts=item["url"],item["ts"]
 out={"capture_time":ts,"status":None,"pdf_valid":False,"pages":0,"page_text_available":False,
      "matches":[],"course_hint":False,"dates_in_docs":[],"sha256":None,
      "public_url":None}
 if not re.fullmatch(r"\d{14}",ts):return {**out,"error":"invalid_capture_timestamp"}
 captured=f"https://wayback.padicat.cat/{ts}id_/{url}"
 try:
  r=requests.get(captured,timeout=(12,45),headers={"User-Agent":"Mozilla/5.0 (public archival PDF educational research)"})
  out["status"]=r.status_code;b=r.content
  if r.status_code!=200 or not b.startswith(b"%PDF") or len(b)>10_000_000:return out
  out["pdf_valid"]=True;out["sha256"]=hashlib.sha256(b).hexdigest()
  d=fitz.open(stream=b,filetype="pdf");out["pages"]=len(d)
  pages=[d[i].get_text("text",sort=True) for i in range(min(len(d),7))]
  d.close()
  raw="\n".join(pages);out["page_text_available"]=len(raw.strip())>=60
  labels={x.upper() for x in LABEL.findall(raw)+BEFORE.findall(raw)}
  for key,pat in COUPLES.items():
   if pat.search(raw):labels.add(key)
  out["matches"]=sorted(labels)
  out["course_hint"]=bool(COURSE.search(raw))
  out["dates_in_docs"]=sorted(set(DATES.findall(raw)))[:16] if labels else []
  if labels:
   out["public_url"]=url
   out["archive_url"]=captured
 except Exception as e:out["error_type"]=type(e).__name__
 return out
def main(path):
 raw=get_index();selected=entries(raw)
 print("Original non-GENSEC PDFs to inspect:",len(selected),flush=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  reports=list(pool.map(inspect,selected))
 relevant=[x for x in reports if x["matches"]]
 report={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "source":"PADICAT authentic public PDF replays, not live current snapshots",
  "index_records":len(raw),"documents_considered":len(selected),
  "archives_pdf_recovered":sum(x["pdf_valid"] for x in reports),
  "pdf_text_available":sum(x["page_text_available"] for x in reports),
  "documents_with_matching_specialty":len(relevant),
  "candidate_pdfs":relevant,
  "non_candidate_error_types":{
    k:sum(x.get("error_type")==k for x in reports) for k in sorted(set(x.get("error_type") for x in reports if x.get("error_type")))},
  "non_candidate_http_counts":{str(code):sum(x["status"]==code for x in reports) for code in sorted({x["status"] for x in reports if x["status"] is not None})},
  "limitations":["A PDF mentioning 507/627 may not itself be a difficult-coverage posting.",
    "Result/list files excluded by name can contain a useful source ID but aren't original offers.",
    "Only first seven pages extracted per document; scanned-image PDFs without OCR could be missed.",
    "Date of archive capture is not the date of original vacancy publication.",
    "Candidate files require manual validation before adding to census.",
    "No applicants names, contact information, or document text exported."]}
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({k:report[k] for k in ("documents_considered","archives_pdf_recovered","pdf_text_available","documents_with_matching_specialty","candidate_pdfs")},ensure_ascii=False),flush=True)
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--output",required=True);main(p.parse_args().output)
