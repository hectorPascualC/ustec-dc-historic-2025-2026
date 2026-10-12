#!/usr/bin/env python3
"""Inspect PADICAT for EDUBCN historic DC JSON API responses and real public PDF folder.

Only archive metadata, no personnel or notice content. URL patterns were observed
in official sources; time of capture is not announcement publication time.
"""
import argparse,datetime,json,re,time
from pathlib import Path
import requests
API="https://wayback.padicat.cat/cdx"
ROOT="https://www.edubcn.cat"
PDC="/pdc_rest/convocatories/ca"
PDF="/rcs_gene/extra/03_nomenaments_dificil_cobertura/"
CASES=[
 ("EDUBCN API","exact",ROOT+PDC),
 ("EDUBCN API","exact","http://www.edubcn.cat"+PDC),
 ("EDUBCN API","prefix",ROOT+"/pdc_rest/"),
 ("EDUBCN PDFs","prefix",ROOT+PDF),
 ("EDUBCN PDFs","prefix","http://www.edubcn.cat"+PDF),
 ("EDUBCN PDFs secundària","prefix",ROOT+PDF+"secundaria/"),
 ("EDUBCN DC page","exact",ROOT+"/ca/professorat_i_pas/seleccio_rrhh/dificil_cobertura"),
 ("EDUBCN control archive","exact","https://efes.cat")]
def scan(area,mode,url):
 out={"area":area,"mode":mode,"url":url,"http":None,"records":[],"truncated":False}
 try:
  r=requests.get(API,params={"url":url,"matchType":mode,"from":"20251001","to":"20261012","limit":"80","output":"json"},
       timeout=(11,31),headers={"User-Agent":"Mozilla/5.0 (historic public teacher vacancy research)"})
  out["http"]=r.status_code
  out["response_bytes"]=len(r.content)
  if r.status_code==200:
   for line in r.text.splitlines():
    try:
     x=json.loads(line)
     if isinstance(x,dict):
      out["records"].append({k:x.get(k) for k in ("timestamp","url","status","mime","digest","length")})
    except Exception:pass
   out["truncated"]=len(out["records"])>=80
 except Exception as e:out["error"]=type(e).__name__+": "+str(e)[:160]
 return out
def main(path):
 results=[]
 for a,m,u in CASES:
  r=scan(a,m,u);results.append(r)
  print(f'{a:23s} {m:6s} HTTP={r["http"]} captures={len(r["records"])}',flush=True)
  time.sleep(.5)
 hits=[{"area":r["area"],**x} for r in results for x in r["records"] if r["area"]!="EDUBCN control archive"]
 pdfs=[x for x in hits if ".pdf" in (x.get("url") or "").lower()]
 api=[x for x in hits if "/pdc_rest/" in (x.get("url") or "").lower()]
 report={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
   "cases":results,"indexed_education_records":len(hits),
   "pdf_capture_records":len(pdfs),"api_capture_records":len(api),
   "pdf_capture_sample":pdfs[:50],"api_capture_sample":api[:50],
   "verified_original_2025_26_offers":0,
   "warnings":["This is an index query only, not a recovered historical PDF or API JSON body.",
    "Captured API URL metadata does not prove historical API response content.",
    "A date in the index represents crawler capture, not publication of a specific vacancy.",
    "A 200 response with 0 CDX rows does not prove that no vacancies were published."]}
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
if __name__=="__main__":
 pa=argparse.ArgumentParser();pa.add_argument("--output",required=True);a=pa.parse_args();main(a.output)
