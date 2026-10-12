#!/usr/bin/env python3
"""Gentle 2025–26 Wayback CDX tests; metadata only, no private data.

CDX can take 40-60 seconds even for one URL. Previous attempts timed out at 18s.
Non-200 responses and failed queries are inconclusive.
"""
import argparse,datetime,json,time,urllib.parse,requests
from pathlib import Path
ROOT="https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/"
CASES=[
 ("Barcelonès","barcelones/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/Barcelones-SEC-dificil-cobertura-oferta-vacants_07112025.pdf"),
 ("Vallès Occidental","valles-occidental/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/VOC-SEC-dificil-cobertura-oferta-vacants.pdf"),
 ("Maresme–Vallès Oriental","maresme-valles-oriental/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/MVO-SEC-dificil-cobertura-oferta-vacants.pdf"),
]
def try_case(name,suffix):
 url=ROOT+suffix
 params={"url":url,"output":"json","filter":"statuscode:200","fl":"timestamp,original,statuscode,mimetype,length",
 "from":"20251101","to":"20260301","collapse":"digest","limit":"8"}
 q="https://web.archive.org/cdx/search/cdx?"+urllib.parse.urlencode(params)
 result={"territori":name,"original_url":url,"checked_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"query_url":q}
 try:
  start=time.monotonic()
  r=requests.get(q,headers={"User-Agent":"Mozilla/5.0 (compatible; academic historical vacancy audit; metadata only)"},
          timeout=(15,65))
  result["status"]=r.status_code
  result["elapsed_sec"]=round(time.monotonic()-start,1)
  result["response_bytes"]=len(r.content)
  if r.status_code==200:
   j=r.json()
   result["matches"]=[dict(zip(j[0],line)) for line in j[1:] if isinstance(line,list) and len(line)==len(j[0])]
  else:result["message"]="HTTP non-200. Not evidence of absence."
 except Exception as e:result["error"]=str(e)[:240]
 return result
def main(out):
 p=Path(out);p.parent.mkdir(parents=True,exist_ok=True)
 results=[]
 for i,c in enumerate(CASES):
  if i:time.sleep(2.0)
  x=try_case(*c);results.append(x)
  print(f"{x['territori']}: status={x.get('status','ERR')} matches={len(x.get('matches',[]))} time={x.get('elapsed_sec',0)}",flush=True)
 summary={"timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat(),
   "reason":"Retest with 65sec CDX timeout rather than previous 18sec; 3 representative original source URLs",
   "cases":results,
   "found_capture_count":sum(len(x.get("matches",[])) for x in results),
   "verdict":"CAPTURES_ONLY_IF_VERIFIED; absence and HTTP errors are INCONCLUSIVE"}
 p.write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
if __name__=="__main__":
 parser=argparse.ArgumentParser();parser.add_argument("--output",required=True);a=parser.parse_args();main(a.output)
