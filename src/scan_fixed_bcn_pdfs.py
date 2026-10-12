#!/usr/bin/env python3
"""Audited inspection of actual dated, publicly published DC PDFs (Barcelones).

Each date in the URL is a documentary filename observation, NOT a certified
publication timestamp. Never publish applicant names, emails or phone numbers.
"""
from __future__ import annotations
import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import re
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
import fitz

ROOT="https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/barcelones/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/"
BASELINE="cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V20_31IDS.csv"
FILENAME_PATTERNS=[
 "Barcelones-SEC-dificil-cobertura-oferta-vacants_{date}.pdf",
 "BCO-SEC-dificil-cobertura-oferta-vacants{date}.pdf",
 "BCO-SEC-dificil-cobertura-oferta-vacants_{date}.pdf",
 "Barcelones-SEC-dificil-cobertura-oferta-vacants{date}.pdf",
]
FIELDS=["id","especialitat","centre","municipi","jornada","data_nom_fitxer","data_termini","data_inici","data_fi","pag_pdf","url_font","sha256","prova"]
RECORD=re.compile(r"\b(\d{8})\s+(507|627|F57|F87)\s*[-–—]\s*(?:Inform.tica|Sistemes|P\.\s*Esp\.|.*?)\b",re.I|re.S)
SIMPLE=re.compile(r"(?m)^\s*(\d{8})\s+(507|627|F57|F87)\s*[-–—]",re.I)
DATE=re.compile(r"\b(\d{1,2}/\d{1,2}/20\d\d)\b")
SCHOOL=re.compile(r"(?mi)^\s*((?:Institut(?: Escola)?|EOI|Centre|Escola|PFI|ZER)\b[^\n]{2,125})")

def dates():
 d=dt.date(2025,11,7)
 while d<=dt.date(2026,2,27):
  yield d
  d+=dt.timedelta(days=7)

def extract_page(page_text,pageidx,filedate,url,sha):
 lines=[x.strip() for x in page_text.splitlines() if x.strip()]
 hit=SIMPLE.search(page_text)
 if not hit:
  # Different PDF renderers may split the identifier and the specialty.
  hit=re.search(r"\b(\d{8})\s*\n\s*(507|627|F57|F87)\s*[-–—]",page_text,re.I)
 if not hit:return None
 sid,code=hit.group(1),hit.group(2).upper()
 c=SCHOOL.search(page_text)
 centre=c.group(1).strip() if c else ""
 municipio=""
 for label in ("L'Hospitalet de Llobregat","Badalona","Santa Coloma de Gramenet","Sant Adrià de Besòs","Barcelona"):
  if label in page_text:municipio=label;break
 # On the standard form the line for Jornada has one of the following.
 m=re.search(r"(?mi)^\s*(Sencera|0[.,]50|1(?:[.,]0+)?)\s+(\d{1,2}/\d{1,2}/20\d\d)\s*$",page_text)
 jornada=m.group(1) if m else ""
 fi=m.group(2) if m else ""
 deadline=""
 mo=re.search(r"Fins\s+a\s+les\s+[^\n]*?dia\s+(\d{1,2}/\d{1,2}/20\d\d)",page_text,re.I)
 if mo:deadline=mo.group(1)
 start=""
 for i,ln in enumerate(lines):
  if "Jornada" in ln and "Data Inici" in ln and i+1<len(lines):
   nxt=DATE.search(lines[i+1]); start=nxt.group(1) if nxt else ""
 if not start:
  # Most indexable versions have the start date directly after the row heading.
  ms=re.findall(r"(?m)^\s*(\d{1,2}/\d{1,2}/20\d\d)\s*$",page_text)
  if ms:start=ms[0]
 return dict(id=sid,especialitat=code,centre=centre,municipi=municipio,
  jornada=jornada,data_nom_fitxer=filedate,data_termini=deadline,
  data_inici=start,data_fi=fi,pag_pdf=pageidx+1,url_font=url,sha256=sha,
  prova="document PDF oficial recuperat; data publicacio exacta NO certificada")

def unit_test():
 sample="""Identificador de la plaça Especialitat Presentació de sol·licituds
19365399 507 - Informàtica Fins a les 23:59:00 del dia 1/3/2026
Institut La Pineda
Nom del centre Adreça
Municipi
Badalona
Telèfon
Sencera 30/6/2026
Jornada Data Inici Data de finalització prevista
3/3/2026
"""
 row=extract_page(sample,5,"2026-02-27","https://example.invalid", "abc")
 assert row["id"]=="19365399" and row["especialitat"]=="507",row
 assert row["centre"]=="Institut La Pineda" and row["data_termini"]=="1/3/2026",row
 assert row["jornada"]=="Sencera" and row["pag_pdf"]==6,row
 assert len(list(dates()))==17
 print("PASS: parser, school, deadline, jornada, 17 date candidates")

def load_old_ids():
 p=Path(BASELINE)
 if not p.exists():return set()
 with p.open(encoding="utf-8-sig",newline="") as f:
  return {row["id"].strip() for row in csv.DictReader(f) if row.get("id")}

def get_bytes(url,retries=2):
 headers={"User-Agent":"Mozilla/5.0 (compatible; DC-Historical-Audit/1.0; public-document-reading)"}
 for i in range(retries):
  try:
   req=urllib.request.Request(url,headers=headers)
   with urllib.request.urlopen(req,timeout=17) as resp:
    buf=resp.read(14_000_000)
    ct=resp.headers.get("Content-Type","")
    if not buf.startswith(b"%PDF"):return None,{"status":"not_pdf","http":resp.status,"type":ct}
    return buf,{"status":"ok","http":resp.status,"type":ct,"bytes":len(buf)}
  except urllib.error.HTTPError as e:
   if e.code in (403,404,410):return None,{"status":"http_error","http":e.code}
   err={"status":"http_error","http":e.code}
  except Exception as e:err={"status":"error","error":str(e)[:190]}
  if i+1<retries:time.sleep(0.4)
 return None,err

def main(outdir):
 out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
 old=load_old_ids(); obs=[]; docs=[]; requests=[]
 # The exact historical spellings changed during the course.
 for day in dates():
  stamp=day.strftime("%d%m%Y")
  for pat in FILENAME_PATTERNS:
   name=pat.format(date=stamp);url=ROOT+name
   pdf,meta=get_bytes(url)
   requests.append({"date":str(day),"filename":name,"url":url,**meta})
   if not pdf:continue
   sha=hashlib.sha256(pdf).hexdigest()
   try:
    doc=fitz.open(stream=pdf,filetype="pdf")
    matches=0
    for i in range(len(doc)):
     txt=doc[i].get_text(sort=True)
     row=extract_page(txt,i,str(day),url,sha)
     if row:obs.append(row);matches+=1
    docs.append({"date":str(day),"filename":name,"sha256":sha,"pages":len(doc),"matching_page_count":matches,"url":url})
    doc.close()
   except Exception as ex:
    docs.append({"date":str(day),"filename":name,"error":str(ex)[:200],"url":url})
   # Once a dated file resolves, don't re-fetch alternative spellings.
   break
  print(f"{day}: documents={sum(x['date']==str(day) for x in docs)} matches={sum(x['data_nom_fitxer']==str(day) for x in obs)}",flush=True)
 # Deduplicate repeated copies of exact page occurrences.
 seen=set();uniq=[]
 for r in obs:
  k=(r["id"],r["data_nom_fitxer"],r["sha256"])
  if k not in seen:seen.add(k);uniq.append(r)
 best={}
 for item in uniq:
  best.setdefault(item["id"],item)
 new=[x for k,x in best.items() if k not in old]
 with (out/"BCO_APARICIONS_TOTES.csv").open("w",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(uniq)
 with (out/"BCO_IDENTIFICADORS_NOUS.csv").open("w",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(new)
 with (out/"BCO_CONSULTES.csv").open("w",newline="",encoding="utf-8") as f:
  ks=["date","filename","url","status","http","type","bytes","error"]
  w=csv.DictWriter(f,fieldnames=ks,extrasaction="ignore");w.writeheader();w.writerows(requests)
 audit={"as_of":dt.datetime.now(dt.timezone.utc).isoformat(),
    "search":"Barcelones official, 17 Fridays 2025-11-07..2026-02-27, 4 spelling variants",
    "baseline_file":BASELINE,"baseline_ids":len(old),
    "attempts":len(requests),"downloaded_official_pdfs":len(docs),
    "documents":docs,"sightings":len(uniq),
    "distinct_target_ids":len(best),"new_ids":[{"id":x["id"],"especialitat":x["especialitat"],"centre":x["centre"],"date_first_observed":x["data_nom_fitxer"],"source":x["url_font"],"pdf_page":x["pag_pdf"]} for x in new],
    "distinct_new_ids":len(new),"current_coverage_certified":False,
    "cautions":["Only dated nominal PDFs directly downloaded from an official web host were counted.",
       "Date in PDF filename does NOT certify timestamp of web publication.",
       "The PDF archive can lack all vacancies for a week; 404 does not mean none.",
       "Other territories require independent audit.",
       "No applicant details are retained."]
    }
 (out/"BCO_AUDITORIA.json").write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({"pdfs":len(docs),"total_sightings":len(uniq),"distinct_ids":len(best),"new_ids":len(new),"names":[x["id"] for x in new]},ensure_ascii=False))
 # Fail only if we did not obtain ANY source PDFs; do not hide incompleteness.
 return 0 if docs else 3

if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--test",action="store_true");ap.add_argument("--output",default="exports_bco");arg=ap.parse_args()
 if arg.test:unit_test()
 else:raise SystemExit(main(arg.output))
