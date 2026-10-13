#!/usr/bin/env python3
"""V47 audit original archived PDF bodies in EDUBCN selection folder (Jan 29 2026).

Only public original PDF metadata, code and specialization flags are retained.
Apparent code references MUST be checked row-by-row before adding to census.
"""
import argparse,datetime,hashlib,io,json,re,time
from pathlib import Path
from urllib.parse import urlsplit
import requests,fitz
CDX="https://wayback.padicat.cat/cdx"
BASE="https://www.edubcn.cat/rcs_gene/seleccio/"
UA={"User-Agent":"Mozilla/5.0 (noncommercial Catalan education historical PDF research)"}
ADMIT=re.compile(r"(?:GENSEC|GESEC|MUNSEC|F57|F87|PFI|2526|507|627|informatic|sistemes)",re.I)
SPECIALTY=re.compile(r"(?:^|\s)(507|627|F57|F87)\s*[-:.)]?\s*(?:Inform.tica|Sistemes|Aplicacions|Professor|Especialitat)|\b(?:Inform.tica|Sistemes\s+i\s+aplicacions\s+inform.tiques)\s*\(?\s*(507|627|F57|F87)",re.I)
# In highly formatted PDFs, explicit adjacent "507"/"627" can be found with or without a title.
CODE=re.compile(r"(?<!\w)(507|627|F57|F87)(?!\w)",re.I)
def cdx():
 r=requests.get(CDX,params={"url":BASE,"matchType":"prefix","from":"20260129","to":"20260130","output":"json","limit":"900"},
                headers=UA,timeout=(12,40))
 if r.status_code!=200:raise RuntimeError(f"PADICAT index http {r.status_code}")
 return [json.loads(l) for l in r.text.splitlines() if l.startswith("{")]
def inspect(item):
 u=item["url"];stamp=item.get("timestamp","")
 result={"archive_capture":stamp,"original_url":u,"http":None,
         "pdf_valid":False,"pages":None,"sha256":None,
         "matching_specialty_codes":[],"raw_code_tokens":[]}
 try:
  archive="https://wayback.padicat.cat/"+stamp+"id_/"+u
  r=requests.get(archive,headers=UA,timeout=(12,35),stream=True)
  result["http"]=r.status_code
  if r.status_code!=200:return result
  raw=bytearray()
  for block in r.iter_content(16384):
   raw.extend(block)
   if len(raw)>5500000:break
  r.close()
  blob=bytes(raw)
  result["pdf_valid"]=blob.startswith(b"%PDF-")
  if not result["pdf_valid"]:return result
  result["sha256"]=hashlib.sha256(blob).hexdigest()
  doc=fitz.open(stream=blob,filetype="pdf")
  result["pages"]=len(doc)
  text="\n".join(doc[i].get_text(sort=True) for i in range(min(14,len(doc))))
  doc.close()
  codes=sorted(set(m.group(1) or m.group(2) for m in SPECIALTY.finditer(text)))
  result["matching_specialty_codes"]=codes
  result["raw_code_tokens"]=sorted(set(CODE.findall(text)))
  result["mentions_2025_26"]=bool(re.search(r"2025\s*[-/–]\s*2026|curs\s+2025\s*[-/–]\s*2026",text,re.I))
 except Exception as e:result["error"]=type(e).__name__+": "+str(e)[:100]
 return result
def main(output):
 all_rows=cdx()
 pdf=[x for x in all_rows if str(x.get("status"))=="200" and
       ".pdf" in (x.get("url") or "").lower() and
       (x.get("mime")=="application/pdf" or "pdf" in (x.get("mime") or ""))]
 seen=set();selected=[]
 for x in pdf:
  url=x.get("url") or ""
  filename=urlsplit(url).path.rsplit("/",1)[-1]
  if "RESULTAT" in filename.upper():continue
  if not ADMIT.search(filename):continue
  if url in seen:continue
  seen.add(url);selected.append(x)
 if len(selected)>120: selected=selected[:120];incomplete=True
 else:incomplete=False
 results=[]
 for i,x in enumerate(selected):
  a=inspect(x);results.append(a)
  if (i+1)%15==0:print(f"processed {i+1}/{len(selected)}",flush=True)
  time.sleep(.13)
 hints=[x for x in results if x.get("matching_specialty_codes") or
         (x.get("raw_code_tokens") and re.search(r"(?:507|627|F57|F87)",x["original_url"],re.I))]
 report={"at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "scope":"Captured EDUBCN 2026-01-29 archive original PDF body scan",
    "cdx_total_records":len(all_rows),"cdx_200_pdf_records":len(pdf),
    "eligible_filename_candidates":len(selected),
    "selection_truncated":incomplete,
    "original_archived_pdfs_downloaded":sum(x.get("pdf_valid") for x in results),
    "pdfs_with_specialty_adjacent_labels":sum(bool(x["matching_specialty_codes"]) for x in results),
    "potential_target_documents":hints,
    "audit_records":results,
    "cautions":["A raw 507/627/F57/F87 token without adjacent specialty label is not proof of vacancy.",
      "The archival capture time is not original announcement publication date.",
      "Only publicly indexed original documents, excludes result PDF based on filename.",
      "No original PDF text, applicant identities or contacts saved."]}
 dest=Path(output);dest.parent.mkdir(parents=True,exist_ok=True)
 dest.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({k:report[k] for k in ("cdx_total_records","cdx_200_pdf_records",
   "eligible_filename_candidates","original_archived_pdfs_downloaded","pdfs_with_specialty_adjacent_labels")},ensure_ascii=False))
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--output",required=True);main(p.parse_args().output)
