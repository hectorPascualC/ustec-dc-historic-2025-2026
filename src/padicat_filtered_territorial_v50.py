#!/usr/bin/env python3
"""V50: Server-side PADICAT CDX filters for difficult-coverage URLs at official hosts.

The first 180 records on the general educacio domain were truncated in V48.
Test CDX filter validity using a broad control, then search filtered index.
"""
import argparse,datetime,json,re,time
from pathlib import Path
import requests
API="https://wayback.padicat.cat/cdx"
SOURCES=[("educacio","https://educacio.gencat.cat/"),
         ("ensenyament","https://ensenyament.gencat.cat/"),
         ("documents_espai","https://documents.espai.educacio.gencat.cat/")]
FILTERS=[("control_any","~url:.*"),("dificil","~url:.*dificil.*"),
         ("nomenaments","~url:.*nomenaments.*"),("vacants","~url:.*vacants.*")]
def find(name,url,filtername,expression):
 out={"host":name,"filter":filtername,"expression":expression,"http":None,"rows":[],"count":0,"truncated":False}
 try:
  r=requests.get(API,params={"url":url,"matchType":"prefix","from":"20251001","to":"20260305",
           "output":"json","limit":"300","filter":expression},
    timeout=(10,35),headers={"User-Agent":"Mozilla/5.0 (historical public Generalitat vacancy archival research)"})
  out["http"]=r.status_code
  if r.status_code!=200:return out
  items=[json.loads(line) for line in r.text.splitlines() if line.lstrip().startswith("{")]
  out["count"]=len(items);out["truncated"]=len(items)>=300
  for x in items:
   u=str(x.get("url") or "")
   if not re.search(r"(?:dificil[-_]cobertura|vacants[-_](?:cobertes|oferta)|nomenaments[-_]telematics)",u,re.I):continue
   out["rows"].append({"url":u,"captured":x.get("timestamp"),"status":x.get("status"),"mime":x.get("mime")})
 except Exception as exc:out["error"]=type(exc).__name__+": "+str(exc)[:130]
 return out
def main(dest):
 all=[]
 for name,url in SOURCES:
  for term,expr in FILTERS:
   row=find(name,url,term,expr);all.append(row)
   print(name,term,row["http"],row["count"],"actual_dc",len(row["rows"]),flush=True)
   time.sleep(.35)
 report={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "queries":all,
  "backend_filter_control_positive":{x["host"]:x["count"]>0 for x in all if x["filter"]=="control_any"},
  "new_exact_dc_capture_count":sum(len(x["rows"]) for x in all),
  "warnings":["A positive control helps validate the filter backend but no results is still an archive-limited outcome.",
    "Date of snapshot is not date the original offer was posted.",
    "A truncated result needs pagination and is not exhaustive.",
    "No personal data stored, only public source URL metadata."]}
 p=Path(dest);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--output",required=True)
 main(p.parse_args().output)
