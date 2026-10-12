#!/usr/bin/env python3
"""V36 PADICAT historical PDF lookup: exact, http/https, per-SSTT path prefixes.

Queries documented public pywb CDX. Archive captures != original publication.
Only public educational vacancy metadata and aggregate counts published.
"""
import argparse,datetime,hashlib,json,re,time
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit
import requests

API="https://wayback.padicat.cat/cdx"
BASE="https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/"
AREAS=[
 ("Alt Pirineu i Aran","alt-pirineu-aran"),("Baix Llobregat","baix-llobregat"),
 ("Barcelonès","barcelones"),("Catalunya Central","catalunya-central"),
 ("Girona","girona"),("Lleida","lleida"),
 ("Maresme–Vallès Oriental","maresme-valles-oriental"),("Penedès","penedes"),
 ("Tarragona","tarragona"),("Terres de l'Ebre","terres-ebre"),
 ("Vallès Occidental","valles-occidental")]
EXACT=[
 ("Barcelonès","Barcelones-SEC-dificil-cobertura-oferta-vacants_07112025.pdf"),
 ("Barcelonès","BCO-SEC-dificil-cobertura-oferta-vacants06022026.pdf"),
 ("Vallès Occidental","VOC-SEC-dificil-cobertura-oferta-vacants.pdf"),
 ("Girona","GIR-SEC-dificil-cobertura-oferta-vacants.pdf"),
 ("Lleida","LLE-SEC-dificil-cobertura-oferta-vacants.pdf")
]
SESSION=requests.Session()
SESSION.headers.update({"User-Agent":"Mozilla/5.0 (research of public PDF announcements; noncommercial)", "Accept":"application/x-ndjson,application/json,text/plain,*/*"})
def variants(url):
 p=urlsplit(url)
 return [urlunsplit((scheme,p.netloc,p.path,p.query,p.fragment)) for scheme in ("https","http")]
def suffix(area):
 slug=dict(AREAS)[area]
 return BASE+slug+"/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/"
def tasks():
 # Exact names originate from previously verified original public listings.
 out=[]
 for area,name in EXACT:
  for u in variants(suffix(area)+name):
   out.append({"area":area,"match":"exact","url":u})
 # Eleven area prefixes plus EDUBCN, broader discovery without inventing PDF filenames.
 for area,slug in AREAS:
  u=BASE+slug+"/personal-docent/nomenaments-telematics/dificil-cobertura/"
  out.append({"area":area,"match":"prefix","url":u})
 # Index old http version for two priority territorial scopes to check URL normalization.
 for area in ("Barcelonès","Vallès Occidental"):
  u=BASE+dict(AREAS)[area]+"/personal-docent/nomenaments-telematics/dificil-cobertura/"
  out.append({"area":area,"match":"prefix","url":variants(u)[1]})
 out.append({"area":"EDUBCN","match":"prefix","url":"https://www.edubcn.cat/ca/professorat_i_pas/seleccio_rrhh/dificil_cobertura"})
 out.append({"area":"Control-PADICAT","match":"exact","url":"https://efes.cat"})
 return out
def parse(body):
 rows=[]
 try:
  data=json.loads(body)
  if isinstance(data,list):
   if data and isinstance(data[0],list):
    return [dict(zip(data[0],v)) for v in data[1:] if isinstance(v,list)]
   return [x for x in data if isinstance(x,dict)]
 except Exception:pass
 for line in body.splitlines():
  try:
   if line.lstrip().startswith("{"):x=json.loads(line)
   elif " {" in line:x=json.loads("{"+line.split(" {",1)[1])
   else:continue
   if isinstance(x,dict):rows.append(x)
  except Exception:pass
 return rows
def request(task):
 record={**task,"http":None,"matches":0,"bytes":0,"truncated":False,"records":[]}
 try:
  r=SESSION.get(API,params={"url":task["url"],"matchType":task["match"],
   "from":"20251001","to":"20261012","limit":"60"},timeout=(11,28))
  record["http"]=r.status_code;record["bytes"]=len(r.content)
  record["content_type"]=r.headers.get("Content-Type","")[:60]
  if r.status_code==200:
   parsed=parse(r.text)
   record["matches"]=len(parsed)
   record["truncated"]=len(parsed)>=60
   for x in parsed:
    orig=x.get("original") or x.get("url") or ""
    record["records"].append({
     "original_url":orig,
     "timestamp":x.get("timestamp") or x.get("ts") or "",
     "status":x.get("status") or x.get("statuscode") or "",
     "mime":x.get("mime") or x.get("mimetype") or "",
     "digest":x.get("digest") or "",
     "length":x.get("length") or ""
    })
 except Exception as e:record["error"]=type(e).__name__+": "+str(e)[:150]
 return record
def run(outname):
 rows=[]
 for i,t in enumerate(tasks()):
  v=request(t);rows.append(v)
  print(f'{i+1:02d} {v["area"]} {v["match"]} {urlsplit(v["url"]).scheme}: HTTP {v["http"]}, hits {v["matches"]}',flush=True)
  time.sleep(.65)
 hits=[{"area":v["area"],"query_url":v["url"],**x} for v in rows for x in v["records"]]
 dc=[h for h in hits if "dificil-cobertura" in h["original_url"].lower() or "dificil_cobertura" in h["original_url"].lower()]
 pdfs=[h for h in dc if ".pdf" in h["original_url"].lower()]
 result={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "source":"PADICAT official public CDX","endpoint":API,
 "scope":"2025-10-01 to 2026-10-12, historic original DC announcements 507/627/F57/F87",
 "query_count":len(rows),"http_200":sum(x["http"]==200 for x in rows),
 "total_capture_records":len(hits),"dc_path_capture_records":len(dc),
 "dc_pdf_capture_records":len(pdfs),"areas_with_dc_hits":sorted(set(x["area"] for x in dc)),
 "queries":[{k:x[k] for k in ("area","match","url","http","matches","bytes","truncated") if k in x}|
            {"error":x.get("error","")} for x in rows],
 "dc_records":dc[:100],
 "negative_cannot_prove_absence":True,
 "warnings":["The CDX index can be incomplete or omit a URL variant.",
  "2025-26 archive timestamp is not proof of original publication date.",
  "Prefix query may truncate after 60 rows and must then be paginated.",
  "Only metadata published, not full PDF or candidate personal data."]}
 path=Path(outname);path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({k:result[k] for k in ("query_count","http_200","total_capture_records","dc_pdf_capture_records","areas_with_dc_hits")},ensure_ascii=False),flush=True)
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--output",required=True);args=p.parse_args()
 run(args.output)
