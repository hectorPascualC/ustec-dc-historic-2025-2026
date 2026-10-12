#!/usr/bin/env python3
"""Try PADICAT's *documented* public CDX endpoint from a runner.
URL, timestamps and capture metadata only; no private payloads.
"""
import argparse,datetime,json,requests,time
from pathlib import Path
API="https://wayback.padicat.cat/cdx"
BASE="https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/"
PDFS=[
("BARCELONES_2025_11","https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/barcelones/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/Barcelones-SEC-dificil-cobertura-oferta-vacants_07112025.pdf"),
("VOC_2025_11",BASE+"valles-occidental/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/VOC-SEC-dificil-cobertura-oferta-vacants.pdf"),
("GIR_2025",BASE+"girona/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/GIR-SEC-dificil-cobertura-oferta-vacants.pdf"),
("PADICAT_CONTROL","https://efes.cat"),
("EDUCACIO_DOMAIN","https://educacio.gencat.cat")]
def query(name,url):
 out={"name":name,"original_url":url,"endpoint":API,"http":None,"capture_count":None,"captures":[]}
 try:
  r=requests.get(API,params={"url":url,"output":"json","from":"20251101","to":"20261012",
                             "fl":"timestamp,original,statuscode,mimetype,digest,length",
                             "limit":"80"},
             timeout=(12,26),headers={"User-Agent":"Mozilla/5.0 (Public Catalan archive historical-research)"})
  out["http"]=r.status_code
  out["content_type"]=r.headers.get("Content-Type","")[:90]
  out["bytes"]=len(r.content)
  if r.status_code==200:
   try:
    j=r.json()
    if isinstance(j,list) and j and isinstance(j[0],list):
     header=j[0]
     out["captures"]=[dict(zip(header,x)) for x in j[1:] if isinstance(x,list)]
    elif isinstance(j,list) and all(isinstance(x,dict) for x in j):
     out["captures"]=j[:80]
    else:out["response_shape"]=type(j).__name__
   except ValueError:
    # CDXJ lines with capture metadata are also common in PyWb archives.
    for line in r.text.splitlines():
     if " {" not in line:continue
     try:
      j=json.loads(line.split(" {",1)[1].join(["{",""]))
      if isinstance(j,dict):out["captures"].append({k:j.get(k) for k in ("url","timestamp","status","mime","digest","length")})
     except (ValueError,TypeError):pass
   out["capture_count"]=len(out["captures"])
 except Exception as e:out["error"]=type(e).__name__+": "+str(e)[:140]
 return out
def main(path):
 out=[]
 for name,url in PDFS:
  x=query(name,url);out.append(x)
  print(name,x.get("http"),x.get("capture_count"),x.get("error"),flush=True)
  time.sleep(.8)
 result={"at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "source":"PADICAT public CDX (endpoint externally documented; not invented)",
    "cases":out,"num_cases":len(out),"verified_historical_pdf_payloads":0,
    "warning":"CDX metadata is not the PDF body; no result or error is not proof that there were no teacher vacancy postings."}
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--output",required=True);a=p.parse_args();main(a.output)
