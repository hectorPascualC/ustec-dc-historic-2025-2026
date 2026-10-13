#!/usr/bin/env python3
"""V63. Retry only four server-failed V62 Common Crawl exact URL queries.

Read the actual recorded HTTP 502/504 cases from V62. Failures must never
be recorded as no capture. Low impact: at most two tries per URL, backoff.
No names, credentials, or original PDF contents saved.
"""
import argparse,datetime,json,time
from pathlib import Path
import requests

INPUT=Path("exports_commoncrawl/COMMONCRAWL_V62_BCO_DATED_PDFS.json")
UA={"User-Agent":"Mozilla/5.0 (historical public archive research, Catalunya, limited retry)"}
def query(item,attempt):
    params={"url":item["original_url"],"output":"json"}
    result={"attempt":attempt,"http":None,"records":[],"error":None}
    try:
        r=requests.get("https://index.commoncrawl.org/"+item["collection"]+"-index",
            params=params,headers=UA,timeout=(10,25))
        result["http"]=r.status_code
        if r.status_code==200:
            for line in r.text.splitlines()[:15]:
                try:
                    x=json.loads(line)
                except ValueError:
                    continue
                if isinstance(x,dict):
                    result["records"].append({k:x.get(k) for k in
                        ("url","timestamp","status","mime","filename","offset","length","digest")})
        elif r.status_code==404:
            result["no_captures_in_this_index"]=True
        else:
            result["error"]="index_http_"+str(r.status_code)
    except Exception as exc:
        result["error"]=type(exc).__name__+": "+str(exc)[:120]
    return result

def main(output):
    original=json.loads(INPUT.read_text(encoding="utf-8"))
    blocked=[{"collection":r["collection"],"original_url":r["original_url"],
              "date_nominal":r["date_nominal"],"filename":r["filename"],
              "v62_http":r["status"]}
             for r in original["queries"] if r.get("status") in (502,504)]
    assert len(blocked)==4, "expected four specific failed index lookups; verify upstream report"
    trials=[]
    for item in blocked:
        answers=[]
        for attempt in (1,2):
            x=query(item,attempt);answers.append(x)
            print(item["filename"],"try",attempt,"HTTP",x["http"],flush=True)
            if x["http"] in (200,404): break
            time.sleep(3)
        trials.append({**item,"attempts":answers,"resolution":
            "FOUND_CDX_RECORDS" if any(a["records"] for a in answers)
            else "NO_CAPTURE_THIS_INDEX" if any(a["http"]==404 for a in answers)
            else "HTTP_200_NO_RECORDS" if any(a["http"]==200 for a in answers)
            else "BLOCKED_TECHNICALLY"})
        time.sleep(1)
    report={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "scope":"Four exact URL Common Crawl 502/504 errors recorded by V62",
        "requested_v62_failures":len(blocked),
        "resolved":sum(x["resolution"]!="BLOCKED_TECHNICALLY" for x in trials),
        "unresolved":sum(x["resolution"]=="BLOCKED_TECHNICALLY" for x in trials),
        "new_index_records":sum(len(a["records"]) for x in trials for a in x["attempts"]),
        "verified_pdf_bodies":0,
        "trials":trials,
        "caveat":"An index hit must be followed by a real WARC HTTP Range + PDF signature/hash validation; 404 cannot certify 0 historical offers; capture date is not publication date."}
    target=Path(output);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:report[k] for k in ("requested_v62_failures","resolved","unresolved","new_index_records")}),flush=True)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",required=True);a=p.parse_args();main(a.output)
