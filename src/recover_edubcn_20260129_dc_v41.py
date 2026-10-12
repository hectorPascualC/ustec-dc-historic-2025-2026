#!/usr/bin/env python3
"""Recover actual PADICAT 2026-01-29 EDUBCN DC JSON, identify 507/627/F57/F87.

The archive contains a public historic API response (not a current-state query).
The original PDF links are checked separately. No personal data, candidate names,
telephone numbers or CVs are saved. Publication date field is labelled DATA from
original API, not asserted as verified timestamp without original PDF.
"""
import argparse,csv,datetime,hashlib,json,re,time
from pathlib import Path
from urllib.parse import urlsplit
import requests
import fitz
SNAPSHOT="https://wayback.padicat.cat/20260129224630id_/https://www.edubcn.cat/pdc_rest/convocatories/ca"
CAPTURED_AT="2026-01-29T22:46:30Z"
START="2025-11-01";END="2026-02-28"
UA={"User-Agent":"Mozilla/5.0 (public academic historical EDUBCN DC vacancy audit)"}
PATTERN=re.compile(r"(?<!\w)(507|627|F57|F87)(?!\w)|inform.tica|sistemes\s+i\s+aplicacions\s+inform.tiques",re.I)
def txt(x):return str(x or "").strip()
def is_target(row):
 return bool(PATTERN.search(" ".join(txt(row.get(k)) for k in ("PERFIL","CODI","DOC_CONVOCATORIA"))))
def digest_source():
 r=requests.get(SNAPSHOT,headers=UA,timeout=(14,40))
 if r.status_code!=200:raise RuntimeError("historic PADICAT JSON replay returned HTTP "+str(r.status_code))
 if len(r.content)>1_200_000:raise ValueError("Unexpectedly large JSON")
 rows=r.json()
 if not isinstance(rows,list):raise ValueError("Archive response is not a JSON array")
 return r,rows
def examine_pdf(url,codigo):
 v={"url":url,"code":codigo,"http":None,"is_pdf":False,
    "pdf_sha256":"","pages":0,"has_code":False,"has_target_sp":False,"has_course_2526":False}
 host=urlsplit(url).hostname or ""
 if host not in ("www.edubcn.cat","edubcn.cat"):return {**v,"error":"untrusted host"}
 try:
  r=requests.get(url,headers=UA,timeout=(12,27),stream=True)
  v["http"]=r.status_code
  if r.status_code!=200:return v
  blob=bytearray()
  for piece in r.iter_content(16384):
   blob.extend(piece)
   if len(blob)>12_000_000:raise ValueError("Large PDF refused")
  r.close()
  b=bytes(blob)
  v["is_pdf"]=b.startswith(b"%PDF-")
  if not v["is_pdf"]:return v
  v["pdf_sha256"]=hashlib.sha256(b).hexdigest()
  doc=fitz.open(stream=b,filetype="pdf")
  v["pages"]=len(doc)
  text="\n".join(doc[i].get_text("text") for i in range(min(24,len(doc))))
  doc.close()
  v["has_code"]=txt(codigo).replace("_","").lower() in text.replace("_","").replace(" ","").lower()
  v["has_target_sp"]=bool(PATTERN.search(text))
  v["has_course_2526"]=bool(re.search(r"2025\s*[-/–]\s*2026|CURS\s+2025",text,re.I))
 except Exception as e:v["error"]=type(e).__name__+": "+str(e)[:140]
 return v
def main(output):
 r,rows=digest_source()
 cols=sorted({k for x in rows if isinstance(x,dict) for k in x})
 selected=[]
 for x in rows:
  if not isinstance(x,dict):continue
  if not is_target(x):continue
  out={k:txt(x.get(k)) for k in ("ID","CODI","DATA","TITULARITAT","ENSENYAMENT",
                                  "PERFIL","CENTRE","CENTRE_ALTRES","INFO_TERMINI",
                                  "INCORPORACIO","DOC_CONVOCATORIA","DOC_RESULTAT")}
  out["data_in_interval"]=START<=out["DATA"]<=END
  selected.append(out)
 # Preserve even out-of-period matches as background, but never treat them as period vacancies.
 todo=[];seen=set()
 for x in selected:
  if not x["data_in_interval"]:continue
  url=x["DOC_CONVOCATORIA"]
  if url and url not in seen:todo.append((url,x["CODI"]));seen.add(url)
 checked=[examine_pdf(url,code) for url,code in todo[:12]]
 report={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "archive_url":SNAPSHOT,"capture_at":CAPTURED_AT,
  "source_http":r.status_code,"source_json_sha256":hashlib.sha256(r.content).hexdigest(),
  "source_json_bytes":len(r.content),"all_public_dc_records":len(rows),
  "source_fields":cols,
  "rows_with_target_507_627_F57_F87_or_equivalent":len(selected),
  "target_rows_in_date_field_interval":sum(x["data_in_interval"] for x in selected),
  "source_date_field":"DATA (appears in historical API; precise semantics require offer PDF verification)",
  "target_rows":selected,
  "original_pdf_checks":checked,"original_pdfs_verified":sum(x["is_pdf"] for x in checked),
  "checks":"Records in archived JSON proved present by capture time; do not infer missing subsequent offers.",
  "warnings":["No candidate name, number, email or full PDF text saved.",
  "Historical API snapshot date differs from date in DATA field.",
  "A PDF and actual specialty/centre/date must be corroborated before adding a new census item.",
  "A record absent at 2026-01-29 could have appeared after that date."]}
 dest=Path(output);dest.parent.mkdir(parents=True,exist_ok=True)
 dest.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({k:report[k] for k in ("source_http","all_public_dc_records",
     "rows_with_target_507_627_F57_F87_or_equivalent","target_rows_in_date_field_interval",
     "original_pdfs_verified")},ensure_ascii=False))
 for x in selected:print(json.dumps({"code":x["CODI"],"date":x["DATA"],"profile":x["PERFIL"],"centre":x["CENTRE"] or x["CENTRE_ALTRES"],"in_scope":x["data_in_interval"]},ensure_ascii=False),flush=True)
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--output",required=True)
 main(p.parse_args().output)
