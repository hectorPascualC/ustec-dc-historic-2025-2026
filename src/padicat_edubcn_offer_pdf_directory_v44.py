#!/usr/bin/env python3
"""V44: Index 2025-26 public EDUBCN original offer PDF URL directory in PADICAT.

Report only public job/vacancy identifiers, URL, response status, capture timestamp.
This is a URL index, *not* original offer text, and does not prove publication dates.
"""
import argparse,datetime,json,re,time
from pathlib import Path
from urllib.parse import urlparse
import requests
API="https://wayback.padicat.cat/cdx"
PREFIXES=[
 ("root_https","https://www.edubcn.cat/rcs_gene/seleccio/"),
 ("root_http","http://www.edubcn.cat/rcs_gene/seleccio/"),
 ("no_www","https://edubcn.cat/rcs_gene/seleccio/"),
 ("GESEC","https://www.edubcn.cat/rcs_gene/seleccio/GESEC"),
 ("GENSEC","https://www.edubcn.cat/rcs_gene/seleccio/GENSEC"),
 ("2526","https://www.edubcn.cat/rcs_gene/seleccio/GENSEC_2526"),
 ("alt_2526","https://www.edubcn.cat/rcs_gene/seleccio/GESEC2526"),
]
FIRST="20251101";LAST="20260305"
PAT=re.compile(r"(?:GENSEC|GESEC)[_-]?(?:2526)?[_-]?\d{1,4}(?=[_.-]|$)",re.I)
TERM=re.compile(r"(?<!\d)(?:507|627|F57|F87)(?!\d)|inform[aà]tica|sistemes|ciberseguretat|PFI",re.I)
def query(name,url):
 record={"name":name,"target_url":url,"http":None,"rows":[],"truncated":False}
 try:
  r=requests.get(API,params={"url":url,"matchType":"prefix","from":FIRST,"to":LAST,
                             "limit":"500","output":"json"},timeout=(13,37),
       headers={"User-Agent":"Mozilla/5.0 (public academic archive vacancy source audit)"})
  record["http"]=r.status_code
  record["response_bytes"]=len(r.content)
  if r.status_code!=200:return record
  lines=r.text.splitlines()
  data=[]
  for line in lines:
   try:
    o=json.loads(line)
    if isinstance(o,dict):data.append(o)
   except ValueError:pass
  record["returned_total"]=len(data)
  record["first_public_record_field_keys"]=list(data[0].keys()) if data else []
  record["public_code_url_samples"]=[{"url":str(x.get("url") or x.get("original") or "")[:250],
          "mime":str(x.get("mime") or x.get("mimetype") or "")[:60],
          "status":str(x.get("status") or "")[:10],
          "timestamp":str(x.get("timestamp") or "")[:20]} for x in data if
          re.search(r"(?:GENSEC|GESEC)",str(x.get("url") or x.get("original") or ""),re.I)][:12]
  record["truncated"]=len(data)>=500
  for x in data:
   u=str(x.get("url") or x.get("original") or "")
   if not u.lower().endswith(".pdf"):continue
   # Very conservative: keep only public official GENSEC/GESEC 2025-26 identifiers.
   v=PAT.search(u)
   if not v:continue
   record["rows"].append({
      "code_fragment":v.group(0),
      "url":u,
      "captured":x.get("timestamp",""),
      "status":x.get("status",x.get("statuscode","")),
      "mime":x.get("mime",x.get("mimetype","")),
      "url_has_target_specialty":bool(TERM.search(u))
   })
 except Exception as ex:record["error"]=type(ex).__name__+": "+str(ex)[:140]
 return record
def main(file):
 all=[]
 for name,u in PREFIXES:
  x=query(name,u);all.append(x)
  print(name,x["http"],"returned",x.get("returned_total"),"GENSEC_PDF",len(x["rows"]),flush=True)
  time.sleep(.45)
 seen=set();data=[]
 for area in all:
  for row in area["rows"]:
   key=(row["url"],row["captured"])
   if key not in seen:
    seen.add(key);data.append(row)
 target=[x for x in data if x["url_has_target_specialty"]]
 j={"at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "interval":"2025-11-01..2026-03-05",
    "prefix_queries":[{k:v for k,v in x.items() if k!="rows"} for x in all],
    "unique_archived_candidate_offers":len(data),
    "urls_with_specialty_in_filename":len(target),
    "archived_offer_urls":data[:300],
    "truncated":any(x["truncated"] for x in all),
    "limits":["A PDF URL without 507/627 in the filename can still be relevant.",
      "Public archive URL indexed does not imply full PDF bytes preserved.",
      "Snapshot date is not date of posting.",
      "Only official public recruitment PDF URLs, not personnel or application details, are stored."]}
 p=Path(file);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({"indexed":len(data),"spec_filename":len(target)},ensure_ascii=False),flush=True)
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--output",required=True)
 main(p.parse_args().output)
