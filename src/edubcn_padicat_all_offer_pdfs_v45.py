#!/usr/bin/env python3
"""V45: Validate every Jan 2026 archived EDUBCN GENSEC/GESEC offer PDF.

Download archived PDF from PADICAT (not modern live copy), compare SHA256,
extract only specialty classification and controlled dates. No PDF text,
applicant names or personal details are published.
"""
import argparse,concurrent.futures,datetime,hashlib,json,re,requests
from pathlib import Path
import fitz
SOURCE="exports_padicat/PADICAT_EDUBCN_V44_PDF_DIRECTORY.json"
CONSENSUS="cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V42_36IDS.csv"
PREFIX="https://wayback.padicat.cat/"
SPECIALTIES=re.compile(r"(?<![A-Z0-9])(507|627|F57|F87)(?![A-Z0-9])",re.I)
CLOSE=re.compile(r"(?:especialitat|perfil(?:\s+professional)?|codi(?:\s+d[’']especialitat)?)\s*[:\-]?\s*(?:\n|\s){0,25}(507|627|F57|F87)",re.I)
DATE=re.compile(r"\b(?:[0-3]?\d)[/.-](?:[01]?\d)[/.-]20(?:25|26)\b")
FOOTER=re.compile(r"(?:507\s*[-–]\s*inform[aà]tica|627\s*[-–]\s*sistemes\s+i\s+aplicacions\s+inform[aà]tiques|F57|F87)",re.I)
SESSION=requests.Session()
SESSION.headers.update({"User-Agent":"Mozilla/5.0 (public academic PDF archive audit)"})
def load_ids():
 import csv
 with open(CONSENSUS,encoding="utf-8-sig",newline="") as f:
  return {row["id"] for row in csv.DictReader(f)}
def expected_records():
 o=json.loads(Path(SOURCE).read_text(encoding="utf-8"))
 seen=set();rows=[]
 for p in o["archived_offer_urls"]:
  path=p["url"].lower()
  if any(x in path for x in ("_resultat","-resultat","__resultat","_result.pdf","_resultat_.pdf")):continue
  if not path.endswith(".pdf"):continue
  key=p["url"]
  if key in seen:continue
  seen.add(key);rows.append(p)
 return rows
def content(url,timeout):
 r=SESSION.get(url,timeout=(12,timeout),allow_redirects=True)
 return r.status_code,r.headers.get("Content-Type",""),r.content[:12_000_000]
def inspect(row):
 original=row["url"];stamp=row["captured"];code=row["code_fragment"]
 archive=f"{PREFIX}{stamp}id_/{original}"
 item={"code_fragment":code,"original_url":original,"captured":stamp,
       "archive_url":archive,"source":"archive","http":None,"valid_pdf":False,
       "actual_pdf_sha256":"","pages":0,"has_507":False,"has_627":False,
       "has_F57":False,"has_F87":False,"has_specialty_label":False,
       "specialty_label_values":[],"date_candidates":[],"probable_target":False}
 for kind,url in [("PADICAT_replay",archive),("live_pdf_fallback",original)]:
  try:
   status,typ,payload=content(url,33)
   item["http"]=status
   if status==200 and payload.startswith(b"%PDF-"):
    item["source"]=kind
    item["actual_pdf_sha256"]=hashlib.sha256(payload).hexdigest()
    doc=fitz.open(stream=payload,filetype="pdf")
    item["pages"]=len(doc)
    pages=[doc[i].get_text("text",sort=True) for i in range(min(len(doc),14))]
    doc.close()
    s="\n".join(pages)
    specs={x.upper() for x in SPECIALTIES.findall(s)}
    for c in ("507","627","F57","F87"):item["has_"+c]=c in specs
    labelled={x.upper() for x in CLOSE.findall(s)}
    # The literal specialty+name phrase is also strong, row-specific evidence.
    if re.search(r"507\s*[-–]\s*inform[aà]tica",s,re.I):labelled.add("507")
    if re.search(r"627\s*[-–]\s*sistemes\s+i\s+aplicacions\s+inform[aà]tiques",s,re.I):labelled.add("627")
    item["specialty_label_values"]=sorted(labelled)
    item["has_specialty_label"]=bool(labelled)
    item["date_candidates"]=sorted(set(DATE.findall(s)))[:30]
    item["probable_target"]=bool(labelled & {"507","627","F57","F87"})
    item["valid_pdf"]=True
    break
  except Exception as exc:
   item[kind+"_error"]=type(exc).__name__+": "+str(exc)[:100]
 return item
def main(output):
 old=load_ids();items=expected_records()
 print(f"Candidates: {len(items)} distinct non-result original official PDF URLs",flush=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
  result=list(ex.map(inspect,items))
 for r in result:
  print(r["code_fragment"],r["source"],r["http"],
        "target",r["specialty_label_values"],flush=True)
 targets=[x for x in result if x["probable_target"]]
 unique_target_codes=sorted(set(x["code_fragment"] for x in targets))
 new=[x for x in targets if all(x["code_fragment"].replace("_","") not in y.replace("_","") for y in old)]
 summary={"audited_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "originals_scanned":len(items),"archived_replay_pdf_ok":sum(x["source"]=="PADICAT_replay" for x in result),
  "current_live_fallback_pdf_ok":sum(x["source"]=="live_pdf_fallback" for x in result),
  "no_pdf":sum(not x["valid_pdf"] for x in result),
  "target_specialty_label_pdf_count":len(targets),
  "target_codes":unique_target_codes,
  "possible_new_codes":[{"code":x["code_fragment"],"url":x["original_url"],
      "pdf_sha256":x["actual_pdf_sha256"],"source":x["source"],
      "specialty":x["specialty_label_values"],
      "dates":x["date_candidates"]} for x in new],
  "results":result,
  "limitations":["Target labels found in PDF must be manually confirmed at row level before addition to census.",
    "Historic archive PDF is stronger evidence than a live URL that might be replaced.",
    "Code appearance is not same as publication date. PADICAT captures stamped 2026-01-29.",
    "No offer PDF should be confused with its RESULTAT file.",
    "Only original official PDF metadata and anonymous specialty flags published."]}
 path=Path(output);path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({k:summary[k] for k in
  ("originals_scanned","archived_replay_pdf_ok","current_live_fallback_pdf_ok","no_pdf",
   "target_specialty_label_pdf_count","target_codes","possible_new_codes")},ensure_ascii=False))
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--output",required=True)
 main(p.parse_args().output)
