#!/usr/bin/env python3
"""Inspect the exact three public PADICAT EDUBCN DC HTML captures, no personal data.

Capture timestamps are not publication dates; archived Angular shells may load
live API records. Never call live API and label it historical.
"""
import argparse,datetime,hashlib,json,re
from pathlib import Path
from urllib.parse import urlsplit
import requests
CDX="https://wayback.padicat.cat/cdx"
URL="https://www.edubcn.cat/ca/professorat_i_pas/seleccio_rrhh/dificil_cobertura"
HEADERS={"User-Agent":"Mozilla/5.0 (noncommercial historic Catalan education vacancies audit)"}
def load_metadata():
 r=requests.get(CDX,params={"url":URL,"matchType":"prefix","from":"20251001","to":"20261012","limit":"40"},
                 headers=HEADERS,timeout=(10,27))
 result={"http":r.status_code,"bytes":len(r.content),"items":[]}
 if r.status_code!=200:return result
 for line in r.text.splitlines():
  try:
   obj=json.loads(line) if line.lstrip().startswith("{") else json.loads("{"+line.split(" {",1)[1]) if " {" in line else None
   if isinstance(obj,dict):
    # The key names are safe, all values are archival metadata; no page content.
    result["items"].append(obj)
  except (ValueError,TypeError,IndexError):pass
 return result
def fetch_one(c):
 ts=c.get("timestamp") or c.get("ts") or c.get("datetime") or c.get("date") or ""
 u=c.get("url") or c.get("original") or URL
 out={"original":u,"capture_timestamp":str(ts),"metadata_keys":list(c)}
 if not re.fullmatch(r"\d{14}",str(ts)):
  return {**out,"reason":"No exact 14-digit timestamp in parsed CDX record"}
 for path in (f"https://wayback.padicat.cat/wayback/{ts}id_/{u}",):
  try:
   r=requests.get(path,headers=HEADERS,timeout=(12,28),allow_redirects=True)
   data=r.content[:3500000]
   html=data.decode("utf-8","replace") if "html" in r.headers.get("Content-Type","").lower() else ""
   out["replay"]={"http":r.status_code,"bytes":len(data),"mime":r.headers.get("Content-Type","")[:90],
     "sha256":hashlib.sha256(data).hexdigest() if r.status_code==200 else "",
     "gensec_2526_literal_in_archived_html":"GENSEC_2526" in html,
     "has_507":bool(re.search(r"(?<!\d)507(?!\d)",html)),
     "has_627":bool(re.search(r"(?<!\d)627(?!\d)",html)),
     "has_F57":"F57" in html,"has_F87":"F87" in html,
     "has_2025_2026_course":any(x in html for x in ("2025/2026","2025-2026","2025–2026")),
     "has_angular":any(x in html.lower() for x in ("angular","ng-app","angularjs")),
     "script_tags":len(re.findall(r"<script\b",html,re.I)),
     "contains_dynamic_api_endpoint":("/pdc_rest/" in html),
     "redirect_same_host":urlsplit(r.url).netloc==urlsplit(path).netloc}
   break
  except Exception as e:out["error"]=type(e).__name__+": "+str(e)[:170]
 return out
def main(output):
 meta=load_metadata()
 docs=[fetch_one(x) for x in meta.get("items",[])[:8]]
 report={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "original_url":URL,"metadata_http":meta["http"],"metadata_records":len(meta.get("items",[])),
  "record_schemas":[{"keys":list(v),"capture_timestamp":v.get("timestamp",None),
    "datetime":v.get("datetime",None),"date":v.get("date",None),
    "url":v.get("url") or v.get("original")} for v in meta.get("items",[])],
  "replays":docs,
  "limitations":["The archive may preserve the public page shell but not historical API responses.",
   "Timestamp (if known) is a capture time, NOT original DC announcement publication time.",
   "No names, document body, or private identifiers recorded.","No historical offer has been authenticated by metadata alone."]}
 p=Path(output);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({k:report[k] for k in ("metadata_http","metadata_records")},ensure_ascii=False),flush=True)
 for d in docs:print(json.dumps({"capture":d.get("capture_timestamp"),"replay":d.get("replay"),"reason":d.get("reason"),"error":d.get("error")},ensure_ascii=False),flush=True)
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--output",required=True)
 main(a.parse_args().output)
