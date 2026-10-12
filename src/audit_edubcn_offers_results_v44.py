#!/usr/bin/env python3
"""Audit original January/December 2025-26 EDUBCN DC PDFs and official result PDFs.

Only vacancy/document metadata, source URLs, SHA256, not full text/personnel.
"""
import argparse,hashlib,datetime,json,re
from pathlib import Path
from urllib.parse import urlsplit
import requests,fitz
DATA="exports_padicat/EDUBCN_20260129_V41_TARGET_OFFERS.json"
UA={"User-Agent":"Mozilla/5.0 (public Generalitat difficult coverage historical research)"}
def evidence(url,code,kind):
 o={"type":kind,"code":code,"url":url,"http":None,"pdf_valid":False,
    "page_count":0,"pdf_sha256":"","has_code":False,"has_2025_26":False,
    "jornada_detectada":"No determinada"}
 if not url:return {**o,"error":"no PDF source link"}
 if urlsplit(url).hostname not in ("www.edubcn.cat","edubcn.cat"):return {**o,"error":"not official public EDUBCN"}
 try:
  r=requests.get(url,headers=UA,timeout=(12,25),stream=True)
  o["http"]=r.status_code
  if r.status_code!=200:
   r.close();return o
  data=bytearray()
  for chunk in r.iter_content(16384):
   data.extend(chunk)
   if len(data)>12_000_000:raise ValueError("PDF too large")
  r.close();data=bytes(data)
  o["pdf_valid"]=data.startswith(b"%PDF-")
  if not o["pdf_valid"]:return o
  o["pdf_sha256"]=hashlib.sha256(data).hexdigest()
  doc=fitz.open(stream=data,filetype="pdf")
  o["page_count"]=len(doc)
  text="\n".join(doc[i].get_text("text") for i in range(min(20,len(doc))))
  doc.close()
  normalized=lambda s:re.sub(r"[\s_]+","",s).lower()
  o["has_code"]=normalized(code) in normalized(text)
  o["has_2025_26"]=bool(re.search(r"2025\s*[-/–]\s*2026|2025[-_]26|CURS 2025",text,re.I))
  # Only label jornada if near literal jornada header; don't infer from page body.
  for m in re.finditer(r"\bJORNADA\b[:\s]*([^\n]{0,60}\n[^\n]{0,60})",text,re.I):
   raw=m.group(1).lower()
   if re.search(r"\bsencera\b|\bcompleta\b|\b100\s*%",raw):
    o["jornada_detectada"]="Sencera";break
   if re.search(r"\bmitja\b|\bparcial\b|\b0[,\.]50?\b|\b50\s*%",raw):
    o["jornada_detectada"]="Mitja/Parcial";break
  if kind=="resultat":
   o["conté_resultat"]=bool(re.search(r"\bresultat\b|\badjudicaci[oó]\b",text,re.I))
   o["conté_deserta"]=bool(re.search(r"\bdeserta\b|\bdesert\b|\bsense\s+candidat",text,re.I))
   # Do NOT read/store identity of appointee or infer outside-pool from any number.
 except Exception as e:o["error"]=type(e).__name__+": "+str(e)[:150]
 return o
def main(output):
 original=json.loads(Path(DATA).read_text(encoding="utf-8"))
 if len(original["target_rows"])!=4:raise ValueError("Unexpected target corpus, stop")
 docs=[]
 for x in original["target_rows"]:
  code=x["CODI"]
  docs.append(evidence(x["DOC_CONVOCATORIA"],code,"oferta"))
  if x.get("DOC_RESULTAT"):docs.append(evidence(x["DOC_RESULTAT"],code,"resultat"))
 report={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
   "original_json_sha256":original["source_json_sha256"],
   "docs":docs,"checked":len(docs),"original_offers_verified":sum(x["pdf_valid"] and x["type"]=="oferta" for x in docs),
   "official_results_verified":sum(x["pdf_valid"] and x["type"]=="resultat" for x in docs),
   "warnings":["Result existence does not independently prove that a job was filled or when.",
    "Jornada is only used when explicitly extracted close to the jornada header.",
    "No PDF content or personal identity is retained.",
    "API DATA is an archived listing date; no exact publication timestamp claimed."]}
 p=Path(output);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({k:report[k] for k in ("checked","original_offers_verified","official_results_verified")},ensure_ascii=False),flush=True)
 for d in docs:print(json.dumps({"code":d["code"],"kind":d["type"],"valid":d["pdf_valid"],"jornada":d["jornada_detectada"],"resultat":d.get("conté_resultat")},ensure_ascii=False),flush=True)
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--output",required=True);a=p.parse_args();main(a.output)
