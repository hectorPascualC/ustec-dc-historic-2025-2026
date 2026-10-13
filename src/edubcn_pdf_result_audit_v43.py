#!/usr/bin/env python3
"""Audit 4 original 2025-26 public EDUBCN DC offer PDFs and 2 result PDFs.

Never export source body, applicant names, contacts, telephone numbers, email or
identities. Extract only vacancy code, dates/jornada evidence flags and hashes.
"""
import argparse,datetime,hashlib,json,re
from pathlib import Path
import requests,fitz
SOURCE="exports_padicat/EDUBCN_20260129_V41_TARGET_OFFERS.json"
UA={"User-Agent":"Mozilla/5.0 (Public historical DC appointment vacancy documentary audit)"}
DATES=r"\b(?:[0123]?\d[/-][01]?\d[/-]20(?:25|26))\b"
def download(url):
 if not url.startswith("https://www.edubcn.cat/rcs_gene/seleccio/"):return None,{"error":"Untrusted file URL"}
 try:
  r=requests.get(url,timeout=(12,35),headers=UA,stream=True)
  data=b""
  for chunk in r.iter_content(16384):
   data+=chunk
   if len(data)>12000000:return None,{"error":"PDF above cap"}
  r.close()
  if r.status_code!=200 or not data.startswith(b"%PDF-"):
   return None,{"http":r.status_code,"error":"Unusable source PDF"}
  return data,{"http":r.status_code,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}
 except Exception as ex:return None,{"error":type(ex).__name__+": "+str(ex)[:160]}
def inspect(url,code,kind):
 b,stats=download(url)
 out={"code":code,"kind":kind,"url":url,**stats,"evidence":{}}
 if b is None:return out
 try:
  doc=fitz.open(stream=b,filetype="pdf");out["pages"]=len(doc)
  text="\n".join(doc[i].get_text(sort=True) for i in range(min(20,len(doc))))
  out["evidence"]={
   "dates_mentioned":sorted(set(re.findall(DATES,text)))[:25],
   "mentions_full_time":bool(re.search(r"jornada[\s\S]{0,45}\b(sencera|completa)\b|\b(sencera|completa)[\s\S]{0,30}jornada",text,re.I)),
   "mentions_half_time":bool(re.search(r"jornada[\s\S]{0,45}\b(mitja|parcial|0[,\.]5)\b|\bmitja\s+jornada",text,re.I)),
   "mentions_100_pct":bool(re.search(r"\b100\s*%|\b1[,\.]0+\s+jornada",text,re.I)),
   "mentions_50_pct":bool(re.search(r"\b50\s*%|\b0[,\.]5\s+jornada",text,re.I)),
   "mentions_full_word":bool(re.search(r"\b(sencera|completa)\b",text,re.I)),
   "mentions_part_word":bool(re.search(r"\b(mitja|parcial)\b",text,re.I)),
   "has_inici":bool(re.search(r"\b(data d.inici|incorporaci[oó]|inici)\b",text,re.I)),
   "has_final":bool(re.search(r"\b(finalitzaci[oó]|data fi|fins al)\b",text,re.I)),
   "mentions_no_expiry":bool(re.search(r"fins que es cobreixi|fins a la cobertura",text,re.I)),
   "mentions_result":bool(re.search(r"\bresultat\b",text,re.I)),
   "mentions_outside_pool":bool(re.search(r"fora\s+(?:de\s+la\s+)?borsa",text,re.I)),
   "code_matches":code.replace("_","") in text.replace("_","").replace(" ",""),
   "pdf_moddate_literal": sorted(set(re.findall(r"(?:D:20(?:25|26)\d{10})",repr(doc.metadata))))[:5]
  }
  doc.close()
 except Exception as ex:out["error"]=type(ex).__name__+": "+str(ex)[:150]
 return out
def main(path):
 src=json.loads(Path(SOURCE).read_text(encoding="utf-8"))
 results=[]
 for row in src["target_rows"]:
  code=row["CODI"]
  for kind,url in (("convocatoria",row["DOC_CONVOCATORIA"]),("resultat",row["DOC_RESULTAT"])):
   if url:results.append(inspect(url,code,kind))
 print(json.dumps({"originals":sum(x["kind"]=="convocatoria" for x in results),
 "pdfs_downloaded":sum(bool(x.get("sha256")) for x in results),
 "res":sum(x["kind"]=="resultat" for x in results),"results":results},ensure_ascii=False),flush=True)
 audit={"asof":datetime.datetime.now(datetime.timezone.utc).isoformat(),"source_json":SOURCE,
 "documents":results,
 "warning":"Date mentions are not proof of beginning/end or posting date. Jornada flags are document-level and require manual matching; no personal names stored."}
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding="utf-8")
if __name__=="__main__":
 parser=argparse.ArgumentParser();parser.add_argument("--output",required=True);a=parser.parse_args();main(a.output)
