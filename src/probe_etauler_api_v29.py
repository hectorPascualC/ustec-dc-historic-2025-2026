#!/usr/bin/env python3
"""Public e-Tauler historical API metadata, never edict body or applicant details."""
import argparse,datetime,json,time
from pathlib import Path
import requests
API="https://tauler.seu-e.cat/api/edictes?idEns=1"
TERMS=["personal docent","nomenaments","informàtica","difícil cobertura","professorat","substitucions","vacants","borsa docent"]
def get(q):
  result={"query":q,"state":"2"}
  try:
    h={"Accept":"application/json","Content-Type":"application/json","Referer":"https://tauler.seu-e.cat/inici?idEns=1","Origin":"https://tauler.seu-e.cat","User-Agent":"Mozilla/5.0"}
    r=requests.post(API,json={"conceptes":[],"cerca":q,"destacat":None,"state":"2"},headers=h,timeout=20)
    result.update(http=r.status_code,bytes=len(r.content))
    if r.status_code==200:
      v=r.json()
      result["type"]=type(v).__name__
      if isinstance(v,dict):
        result["keys"]=list(v)
        for k,x in v.items():
          if isinstance(x,(int,float,bool)) or x is None:result["scalar_"+k]=x
          elif isinstance(x,list):
            result["size_"+k]=len(x)
            if x and isinstance(x[0],dict):result["fields_"+k]=list(x[0])[:22]
          elif isinstance(x,dict):result["fields_"+k]=list(x)[:20]
      elif isinstance(v,list):
        result["count"]=len(v)
        if v and isinstance(v[0],dict):result["fields"]=list(v[0])[:22]
  except Exception as e:result["error"]=type(e).__name__+": "+str(e)[:120]
  return result
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--output",required=True);a=p.parse_args()
 rows=[]
 for q in TERMS:
   item=get(q);rows.append(item);print(q,item.get("http"),item.get("keys"),flush=True);time.sleep(.3)
 out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
 out.write_text(json.dumps({"at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"endpoint":API,"queries":rows,"warning":"Search API schemas only; never original notice content; not a historical census"},ensure_ascii=False,indent=2),encoding="utf-8")
