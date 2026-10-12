#!/usr/bin/env python3
"""PADICAT historical EDUBCN capture replay variants, public metadata only.
Raw and rewritten URL shapes from webrecorder/public-web-archives cat_wa.yaml.
"""
import argparse,datetime,hashlib,json,re
from pathlib import Path
from urllib.parse import urlsplit
import requests
HOST="https://wayback.padicat.cat"
URL="https://www.edubcn.cat/ca/professorat_i_pas/seleccio_rrhh/dificil_cobertura"
STAMP="20260129224629"
UA={"User-Agent":"Mozilla/5.0 (public historical Catalan education archive research)","Accept":"text/html,application/pdf,*/*"}
def forms():
 return [
  ("documented_rewritten",f"{HOST}/wayback/{STAMP}/{URL}"),
  ("documented_raw",f"{HOST}/wayback/{STAMP}id_/{URL}"),
  ("historic_external_raw",f"{HOST}/{STAMP}id_/{URL}"),
  ("localized_rewritten",f"{HOST}/ca/wayback/{STAMP}/{URL}"),
  ("localized_raw",f"{HOST}/ca/wayback/{STAMP}id_/{URL}")
 ]
def inspect(tag,url):
 result={"type":tag,"url":url}
 try:
  r=requests.get(url,headers=UA,timeout=(12,30),stream=True,allow_redirects=True)
  result["http"]=r.status_code
  result["content_type"]=r.headers.get("Content-Type","")[:100]
  result["redirects"]=len(r.history)
  result["final_host"]=urlsplit(r.url).netloc
  b=bytearray()
  for chunk in r.iter_content(8192):
   b.extend(chunk)
   if len(b)>4_000_000:break
  r.close()
  b=bytes(b[:4_000_000])
  result["bytes"]=len(b)
  if r.status_code==200 and b:
   result["sha256"]=hashlib.sha256(b).hexdigest()
  result["pdf_magic"]=b.startswith(b"%PDF")
  s=b.decode("utf-8","replace") if b[:100].lstrip().startswith((b"<!",b"<html",b"<HTML")) else ""
  result["is_html"]=bool(s)
  if s:
   result["source_flags"]={
    "mentions_507":bool(re.search(r"(?<!\d)507(?!\d)",s)),
    "mentions_627":bool(re.search(r"(?<!\d)627(?!\d)",s)),
    "mentions_F57":bool(re.search(r"(?<!\w)F57(?!\w)",s,re.I)),
    "mentions_F87":bool(re.search(r"(?<!\w)F87(?!\w)",s,re.I)),
    "mentions_GENSEC2526":"GENSEC_2526" in s,
    "mentions_DC":bool(re.search(r"dif[ií]cil[\s-]+cobertura",s,re.I)),
    "mentions_Angular":bool(re.search(r"angular|ng-app",s,re.I)),
    "mentions_2025_26":bool(re.search(r"2025\s*[-/–]\s*2026",s)),
    "script_count":len(re.findall(r"<script\b",s,re.I))}
 except Exception as e:result["error"]=type(e).__name__+": "+str(e)[:140]
 return result
def main(out):
 rows=[]
 for tag,url in forms():
  v=inspect(tag,url);rows.append(v)
  print(tag,v.get("http"),v.get("bytes"),v.get("error"),flush=True)
 report={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "capture_at":"2026-01-29T22:46:29Z",
  "capture_date_is_not_publication_date":True,
  "original":URL,"attempts":rows,
  "genuine_historic_html_copies":sum(x.get("http")==200 and x.get("is_html") for x in rows),
  "archive_metadata_is_not_offer":True,
  "technical_reference":"https://github.com/webrecorder/public-web-archives/blob/main/webarchives/cat_wa.yaml",
  "warnings":["A 404 replay may indicate archive access limitations, not absent capture.",
  "Even if the 2026-01-29 HTML is recovered, the JavaScript frontend may fetch 2026 current API data.",
  "No applicant names, PDF bodies or personal data are stored."]}
 p=Path(out);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--output",required=True);main(a.parse_args().output)
