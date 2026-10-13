#!/usr/bin/env python3
"""V67. Tight Common Crawl filename-prefix probes for six SSTT with no IDs.

Unlike V66's broad directories, each wildcard is anchored to an existing
official PDF document name prefix from verified V24 source. Limit to two
contemporary collections, round-robin territory, log HTTP errors explicitly.
Never presume a missing index row means zero vacancies.
"""
import argparse,csv,datetime,json,re,time
from pathlib import Path
from urllib.parse import urlsplit
import requests
SOURCES=Path("exports_territorial/SSTT_PDFS.csv")
TARGETS=["Alt Pirineu i Aran","Catalunya Central","Girona","Maresme–Vallès Oriental","Tarragona","Terres de l'Ebre"]
COLLECTIONS=["CC-MAIN-2025-51","CC-MAIN-2026-08"]
UA={"User-Agent":"Mozilla/5.0 (public historical teaching archive research; limited indexed URL probes)"}
def get():
    with SOURCES.open(encoding="utf-8-sig",newline="") as f:
        allrows=list(csv.DictReader(f))
    data=[]
    for territory in TARGETS:
        r=next((x for x in allrows if x["territori"]==territory
                and x["tipus"]=="secundaria" and
                re.search(r"-oferta-vacants\.pdf$",x["url"])),None)
        if not r: raise ValueError("No original verified file for "+territory)
        base=r["url"].rsplit(".pdf",1)[0]
        if "-oferta-vacants" not in base:raise ValueError("not a valid prefix")
        prefix=base.split("-oferta-vacants")[0]
        data.append({"territory":territory,"document_url_from_V24":r["url"],
                     "filename_prefix":prefix})
    return data
def check(src,coll):
    obs={"territory":src["territory"],"pdf_filename_prefix":src["filename_prefix"],
         "collection":coll,"http_status":None,"index_hits":0,"candidates":[],"error":None}
    try:
        r=requests.get("https://index.commoncrawl.org/"+coll+"-index",
            params={"url":src["filename_prefix"]+"*","output":"json","pageSize":12},
            headers=UA,timeout=(8,22))
        obs["http_status"]=r.status_code
        if r.status_code==200:
            entries=[]
            for line in r.text.splitlines()[:15]:
                try:entry=json.loads(line)
                except Exception:continue
                if isinstance(entry,dict):entries.append(entry)
            obs["index_hits"]=len(entries)
            for x in entries:
                u=str(x.get("url") or "")
                if (u.startswith(src["filename_prefix"]) and
                    urlsplit(u).path.lower().endswith(".pdf") and
                    not re.search(r"(?i)(curriculum|sol.licitud|dni|nom_cognom)",u)):
                    obs["candidates"].append({k:x.get(k) for k in
                    ("url","timestamp","status","mime","digest","filename","offset","length")})
        elif r.status_code!=404:obs["error"]="HTTP_"+str(r.status_code)
    except Exception as e:obs["error"]=type(e).__name__+": "+str(e)[:150]
    return obs
def main(output):
    src=get()
    attempts=[];streak=0;stop=False
    for coll in COLLECTIONS:
        for x in src:
            a=check(x,coll)
            attempts.append(a)
            print(coll,x["territory"],a["http_status"],a["index_hits"],flush=True)
            streak=streak+1 if a["http_status"] in (429,502,503,504) else 0
            if streak>=4:
                stop=True
                break
            time.sleep(.95)
        if stop:break
    d={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "approach":"Narrow official filename prefixes vs wide directory prefixes V66",
       "source":"exports_territorial/SSTT_PDFS.csv verified V24 official URLs",
       "territories":len(src),"collections":COLLECTIONS,
       "planned_queries":len(src)*len(COLLECTIONS),"executed_queries":len(attempts),
       "stopped_due_to_four_5xx":stop,
       "successful_queries_200":sum(x["http_status"]==200 for x in attempts),
       "no_capture_404":sum(x["http_status"]==404 for x in attempts),
       "blocked":sum(x["http_status"] not in (200,404) for x in attempts),
       "generic_historical_pdf_url_candidates":sum(len(x["candidates"]) for x in attempts),
       "validated_pdf_binaries":0,"queries":attempts,
       "warnings":["Results scoped to precise authenticated original filename prefixes; no evidence of exhaustive months",
          "HTTP 502/504/429 are not no-capture evidence.",
          "Index hits require retrieving and validating actual WARC PDF bytes before inclusion.",
          "No personal applicant information included."]}
    p=Path(output);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:d[k] for k in ("executed_queries","no_capture_404","blocked","generic_historical_pdf_url_candidates")}))
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",required=True)
    main(p.parse_args().output)
