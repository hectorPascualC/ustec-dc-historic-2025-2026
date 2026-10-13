#!/usr/bin/env python3
"""V78: validate Jan29 and Oct04 2026 EDUBCN API snapshots in both ca and es.

Two languages are independently archived a few minutes apart. Detect actual
records not present in the ca variant, 507/627/F57/F87 target in Nov-Feb,
and month-level listing retention. No candidate names or private data saved.
"""
import argparse,collections,datetime,hashlib,json,re,time
from pathlib import Path
import requests
HOST="https://wayback.padicat.cat/"
BASE="https://www.edubcn.cat/pdc_rest/convocatories/"
CAPTURES={
 "jan_ca":"20260129224630",
 "jan_es":"20260129230101",
 "oct_ca":"20261004093514",
 "oct_es":"20261004094857"
}
RE=re.compile(r"(?<!\w)(?:507|627|F57|F87)(?!\w)|inform[aáà]tica|sistemes\s+i\s+aplicacions\s+inform[aà]tiques|sistemas\s+y\s+aplicaciones\s+inform[aá]ticas",re.I)
UA={"User-Agent":"Mozilla/5.0 (public archived teacher vacancy API; bounded, non-commercial)"}
def get(key,stamp):
    lang=key[-2:]
    url=HOST+stamp+"id_/"+BASE+lang
    meta={"capture":key,"archived_at":stamp,"url":url,"http":None,
        "response_bytes":None,"sha256":None,"parse_ok":False,"records":None,"error":None}
    rows=[]
    try:
        r=requests.get(url,headers=UA,timeout=(10,33))
        meta["http"]=r.status_code
        if r.status_code!=200:return meta,rows
        raw=r.content
        if len(raw)>2500000:
            meta["error"]="oversized_api";return meta,rows
        meta["response_bytes"]=len(raw)
        meta["sha256"]=hashlib.sha256(raw).hexdigest()
        body=json.loads(raw)
        if isinstance(body,list):rows=body
        elif isinstance(body,dict):
            rows=next((value for value in body.values()
               if isinstance(value,list) and (not value or isinstance(value[0],dict))),[])
        if not isinstance(rows,list):meta["error"]="non-list";return meta,[]
        meta["parse_ok"]=True;meta["records"]=len(rows)
    except Exception as e:meta["error"]=type(e).__name__+": "+str(e)[:135]
    return meta,rows
def short(r,which):
    return {"snapshot":which,"id":str(r.get("CODI") or ""),
      "date":str(r.get("DATA") or "")[:10],"centre":str(r.get("CENTRE") or "")[:110],
      "specialty":str(r.get("PERFIL") or "")[:115],
      "offer_pdf":str(r.get("DOC_CONVOCATORIA") or ""),
      "result_pdf":str(r.get("DOC_RESULTAT") or "")}
def main(target):
    stat,items={},{}
    for k,ts in CAPTURES.items():
        m,rows=get(k,ts);stat[k]=m;items[k]=rows
        print(k,m["http"],m["records"],flush=True)
        time.sleep(.5)
    valid=all(x["parse_ok"] for x in stat.values())
    sets={}
    month_stats={}
    for k,rows in items.items():
        groups=collections.Counter(str(row.get("DATA") or "")[:7] for row in rows)
        month_stats[k]=dict(sorted(groups.items()))
        sets[k]={str(row.get("CODI") or ""):row for row in rows if str(row.get("CODI") or "")}
    diff={}
    for a,b in (("jan_ca","jan_es"),("oct_ca","oct_es")):
        ca,es=sets[a],sets[b]
        diff[a[:3]]={
           "ca_ids":len(ca),"es_ids":len(es),
           "only_in_ca":[short(ca[k],a) for k in sorted(ca.keys()-es.keys())],
           "only_in_es":[short(es[k],b) for k in sorted(es.keys()-ca.keys())]}
    candidate=[]
    for k,rows in items.items():
        for row in rows:
            d=str(row.get("DATA") or "")[:10]
            if "2025-11-01"<=d<="2026-02-28" and RE.search(str(row.get("PERFIL") or "")):
                candidate.append(short(row,k))
    by_id={}
    for x in candidate:by_id.setdefault(x["id"],[]).append(x)
    result={"at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "method":"Four genuine PADICAT captures, ca/es snapshots at 2026-01-29 and 2026-10-04",
         "verified_all_four":valid,"stats":stat,"monthly_posting_date_histograms":month_stats,
         "language_ID_differences":diff,
         "target_in_window_unique_codes":len(by_id),
         "target_in_window_rows":[{"id":code,"versions":rows} for code,rows in sorted(by_id.items())],
         "limitations":["ca and es lists can be taken minutes apart, possible small genuine time change.",
            "Data is the portal's publication date, not first-ever posting if republished.",
            "A month not present in an Oct year-switched archive doesn't establish no historical postings in that month.",
            "No applicant or adjudicatari names, emails, phone numbers or raw API body stored."]}
    p=Path(target);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"all_valid":valid,"jan":diff["jan"]["ca_ids"],
      "jan_difference":len(diff["jan"]["only_in_ca"])+len(diff["jan"]["only_in_es"]),
      "oct_difference":len(diff["oct"]["only_in_ca"])+len(diff["oct"]["only_in_es"]),
      "target_unique":len(by_id)}),flush=True)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",required=True)
    main(p.parse_args().output)
