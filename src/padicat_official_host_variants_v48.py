#!/usr/bin/env python3
"""V48: Check alternative, historically real Generalitat PDF hosts in PADICAT CDX.

A search of one URL spelling is not an exhaustive survey of a public archive.
This checker tests actual known official hosts/paths and does not conflate
capture timestamps with announcement publication dates.
"""
import argparse,datetime,json,re,time
from pathlib import Path
import requests
CDX="https://wayback.padicat.cat/cdx"
HOSTS=[
 ("educacio_website","https://educacio.gencat.cat/"),
 ("educacio_http","http://educacio.gencat.cat/"),
 ("educacio_www","https://www.educacio.gencat.cat/"),
 ("educacio_pdf_tree","https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/"),
 ("educacio_pdf_tree_http","http://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/"),
 ("ensenyament_old","https://ensenyament.gencat.cat/"),
 ("documents_espai","https://documents.espai.educacio.gencat.cat/"),
 ("documents_espai_http","http://documents.espai.educacio.gencat.cat/"),
 ("documents_espai_www","https://www.documents.espai.educacio.gencat.cat/")
]
def query(name,u):
 a={"name":name,"url":u,"status":None,"indexed":None,"suspected_dc":[],"truncated":False}
 try:
  r=requests.get(CDX,params={"url":u,"matchType":"prefix","from":"20251001","to":"20260305","limit":"180","output":"json"},
        timeout=(12,30),headers={"User-Agent":"Mozilla/5.0 (public educational archival source research)"})
  a["status"]=r.status_code
  if r.status_code!=200:return a
  rows=[json.loads(x) for x in r.text.splitlines() if x.lstrip().startswith("{")]
  a["indexed"]=len(rows);a["truncated"]=len(rows)>=180
  for x in rows:
   url=str(x.get("url",""))
   if not re.search(r"dificil[-_]cobertura|vacants[-_](?:cobertes|oferta)|nomenaments[-_]telematics",url,re.I):continue
   a["suspected_dc"].append({"url":url,"at":x.get("timestamp"),"mime":x.get("mime"),"status":x.get("status")})
 except Exception as ex:a["error"]=type(ex).__name__+": "+str(ex)[:130]
 return a
def main(dest):
 out=[]
 for name,u in HOSTS:
  row=query(name,u);out.append(row)
  print(name,row["status"],row["indexed"],len(row["suspected_dc"]),flush=True)
  time.sleep(.45)
 j={"checked_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "scope":"historic public PDF hosts October2025-March2026","queries":out,
    "archive_dc_url_hits":sum(len(r["suspected_dc"]) for r in out),
    "limitations":["CDX prefix listings can be truncated and can normalize http to https.",
      "No public PDF body is recovered merely by seeing CDX URL metadata.",
      "2025-26 archive capture and original publication time are different.",
      "Zero in one archive is not a zero of real administrative vacancy publications."]}
 p=Path(dest);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding="utf-8")
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--output",required=True);main(a.parse_args().output)
