#!/usr/bin/env python3
"""Compare PADICAT archived public EDUBCN DC JSON snapshots.

Jan 29 vs Oct 4, 2026; check 507/627/F57/F87 post-January old rows
and original offer PDF where available. No candidate personal data.
"""
import argparse,datetime,hashlib,json,re
from pathlib import Path
from urllib.parse import urlsplit
import requests
import fitz
from recover_edubcn_20260129_dc_v41 import is_target,examine_pdf
BASE="https://www.edubcn.cat/pdc_rest/convocatories/"
SOURCES=[
 ("CA_JAN29","20260129224630","ca"),
 ("ES_JAN29","20260129230101","es"),
 ("CA_OCT4","20261004093514","ca")]
def get(label,stamp,lang):
 source="https://wayback.padicat.cat/"+stamp+"id_/"+BASE+lang
 d={"label":label,"capture":stamp,"source":source}
 try:
  r=requests.get(source,timeout=(11,45),headers={"User-Agent":"Mozilla/5.0 (archival public DC education research)"})
  d["http"]=r.status_code
  if r.status_code!=200:return d
  raw=r.json()
  if not isinstance(raw,list):return {**d,"error":"historic JSON was not an array"}
  d["sha256"]=hashlib.sha256(r.content).hexdigest()
  d["total_records"]=len(raw)
  d["data_min"]=min((str(x.get("DATA","")) for x in raw if isinstance(x,dict)),default="")
  d["data_max"]=max((str(x.get("DATA","")) for x in raw if isinstance(x,dict)),default="")
  selected=[]
  for x in raw:
   if not isinstance(x,dict) or not is_target(x):continue
   if not "2025-11-01"<=str(x.get("DATA",""))<="2026-02-28":continue
   selected.append({"code":str(x.get("CODI","")),"id":str(x.get("ID","")),
    "date":str(x.get("DATA","")),"profile":str(x.get("PERFIL","")),
    "centre":str(x.get("CENTRE") or x.get("CENTRE_ALTRES") or ""),
    "convocatoria_url":str(x.get("DOC_CONVOCATORIA") or ""),
    "result_url":str(x.get("DOC_RESULTAT") or "")})
  d["in_scope_target_rows"]=selected
 except Exception as e:d["error"]=type(e).__name__+": "+str(e)[:190]
 return d
def main(out):
 source=[get(*x) for x in SOURCES]
 ca_jan=next((x for x in source if x["label"]=="CA_JAN29"),{})
 ca_oct=next((x for x in source if x["label"]=="CA_OCT4"),{})
 jan_codes={x["code"] for x in ca_jan.get("in_scope_target_rows",[])}
 oct_rows=ca_oct.get("in_scope_target_rows",[])
 extra=[x for x in oct_rows if x["code"] not in jan_codes]
 checks=[]
 for x in extra[:12]:
  if x["convocatoria_url"]:
   v=examine_pdf(x["convocatoria_url"],x["code"])
   checks.append(v)
 output_data={"at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
   "scope_dates":["2025-11-01","2026-02-28"],
   "sources":source,"codes_jan":sorted(jan_codes),
   "codes_oct_in_period":sorted({x["code"] for x in oct_rows}),
   "additional_oct_in_period":extra,
   "additional_original_pdf_checks":checks,
   "additional_original_pdfs":sum(x.get("is_pdf",False) for x in checks),
   "warnings":["October snapshot presence doesn't prove a particular earlier publication time; crosscheck DATA in PDF.",
    "Absence from October snapshot doesn't mean an earlier vacancy never existed.",
    "No candidate names or applicant details are retained."]}
 p=Path(out);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(output_data,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({x["label"]:{k:x.get(k) for k in ("http","total_records","data_min","data_max","error")}
      for x in source},ensure_ascii=False),flush=True)
 print(json.dumps({"in_scope_after_jan":len(extra),"pdf_verified":output_data["additional_original_pdfs"]},ensure_ascii=False),flush=True)
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--output",required=True);a=p.parse_args();main(a.output)
