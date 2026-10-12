#!/usr/bin/env python3
"""Investigate public EDUBCN frontend AJAX URLs; no applicant/personal data."""
import argparse,urllib.request,json,re,datetime,hashlib
from pathlib import Path
URL="https://www.edubcn.cat/pdc/js/app.bundle-v05.js"
def main(path):
 out={"checked_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"url":URL}
 try:
  with urllib.request.urlopen(urllib.request.Request(URL,headers={"User-Agent":"Mozilla/5.0"}),timeout=30) as r:
   b=r.read(12_000_000)
   text=b.decode("utf-8","replace")
   out["status"]=r.status;out["bytes"]=len(b);out["sha256"]=hashlib.sha256(b).hexdigest()
   for q in ["pdc_rest","convocatories","archive","historic","data","index","ca/","/resultat","limit","offset","query","rest"]:
    entries=[]
    for m in list(re.finditer(re.escape(q),text,re.I))[:15]:
     entries.append(text[max(0,m.start()-180):m.end()+240])
    out[q+"_occurrences"]=len(list(re.finditer(re.escape(q),text,re.I)))
    out[q+"_snippets"]=entries
 except Exception as e:out["error"]=str(e)
 f=Path(path);f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({k:v for k,v in out.items() if k in ("status","bytes","error","pdc_rest_occurrences","convocatories_occurrences","historic_occurrences","archive_occurrences")},ensure_ascii=False))
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--output",required=True);a=p.parse_args();main(a.output)
