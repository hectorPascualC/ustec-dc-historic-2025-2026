#!/usr/bin/env python3
"""V76: independently compare two *actual PADICAT* archived EDUBCN API JSON bodies.

Jan 29 and Oct 4 2026 are two archive captures of public convocation listings.
Can expose missing Feb 2026 target 507/627/F57/F87 or earlier Dec postings.
No candidate personal info, email/phone, or raw API bodies persisted.
"""
import argparse,datetime,hashlib,json,re,time
from pathlib import Path
import requests
URL="https://www.edubcn.cat/pdc_rest/convocatories/ca"
ARCH="https://wayback.padicat.cat/"
CAPTURES={
 "2026-01-29":("20260129224630","Jan29 known baseline"),
 "2026-10-04":("20261004093514","Oct04 later archive")
}
WINDOW_START="2025-11-01";WINDOW_END="2026-02-28"
UA={"User-Agent":"Mozilla/5.0 (public Catalan teacher vacancy archive; capped download)"}
TARGET=re.compile(r"(?<!\d)(?:507|627|F57|F87)(?!\d)|inform[aà]tica|sistemes\s+i\s+aplicacions\s+inform[aà]tiques",re.I)
def pull(date,ts):
    u=ARCH+ts+"id_/"+URL
    result={"capture":date,"archive_timestamp":ts,"archive_url":u,
        "http":None,"length":0,"sha256":None,"parse_ok":False,
        "all_public_records":None,"range_records":0,"target_range":0,
        "target_all_dates":0,"error":None}
    data=[]
    try:
        r=requests.get(u,headers=UA,timeout=(12,42),stream=True)
        result["http"]=r.status_code
        if r.status_code!=200:return result,data
        b=bytearray()
        for chunk in r.iter_content(32768):
            b.extend(chunk)
            if len(b)>1800000:result["error"]="api_body_exceeds_size_limit";return result,data
        raw=bytes(b);result["length"]=len(raw)
        result["sha256"]=hashlib.sha256(raw).hexdigest()
        content=json.loads(raw)
        if isinstance(content,list): data=content
        elif isinstance(content,dict):
            for k,v in content.items():
                if isinstance(v,list) and v and isinstance(v[0],dict): data=v;break
        if not isinstance(data,list) or (data and not isinstance(data[0],dict)):
            result["error"]="no-list-of-records";return result,[]
        result["parse_ok"]=True;result["all_public_records"]=len(data)
        result["range_records"]=sum(WINDOW_START<=str(x.get("DATA") or "")[:10]<=WINDOW_END for x in data)
        result["target_range"]=sum(WINDOW_START<=str(x.get("DATA") or "")[:10]<=WINDOW_END
            and TARGET.search(str(x.get("PERFIL") or "")) is not None for x in data)
        result["target_all_dates"]=sum(TARGET.search(str(x.get("PERFIL") or "")) is not None for x in data)
    except Exception as e:result["error"]=type(e).__name__+": "+str(e)[:150]
    return result,data
def strip(row,which):
    return {
        "capture":which,
        "code":str(row.get("CODI") or "").strip(),
        "posting_date_field":str(row.get("DATA") or "")[:10],
        "specialty":str(row.get("PERFIL") or "")[:115],
        "centre":str(row.get("CENTRE") or "")[:105],
        "public_doc_pdf":str(row.get("DOC_CONVOCATORIA") or ""),
        "public_result_pdf":str(row.get("DOC_RESULTAT") or ""),
        "term_description":str(row.get("INFO_TERMINI") or "")[:90],
        "incorporation":str(row.get("INCORPORACIO") or "")[:80],
    }
def main(output):
    results={};captures={}
    for name,(ts,desc) in CAPTURES.items():
        stat,body=pull(name,ts);results[name]=stat;captures[name]=body
        print(name,"http",stat["http"],"records",stat["all_public_records"],
                "target_months",stat["target_range"],flush=True)
        time.sleep(.6)
    if any(not x["parse_ok"] for x in results.values()):
        # Preserve technical error details without treating failed capture as zero.
        result={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "status":"BLOCKED_INCOMPLETE_ARCHIVE_API","captured_metadata":results,
                "new_offer_candidate_count":None,
                "limitations":["Archive capture parse failed; no null count should become zero."]}
    else:
        jan=[strip(row,"2026-01-29") for row in captures["2026-01-29"] if
             WINDOW_START<=str(row.get("DATA") or "")[:10]<=WINDOW_END
             and TARGET.search(str(row.get("PERFIL") or ""))]
        octr=[strip(row,"2026-10-04") for row in captures["2026-10-04"] if
             WINDOW_START<=str(row.get("DATA") or "")[:10]<=WINDOW_END
             and TARGET.search(str(row.get("PERFIL") or ""))]
        known={r["code"] for r in jan}
        newly=[r for r in octr if r["code"] not in known]
        result={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "status":"COMPARED_TWO_ARCHIVED_JSON_BODIES",
          "historical_target":"507 / 627 / F57 / F87",
          "posting_date_field_interval":"2025-11-01..2026-02-28",
          "captures":results,
          "jan_target_count":len(jan),"oct_target_count":len(octr),
          "oct_in_window_not_in_jan":len(newly),
          "jan_target_rows":jan,
          "oct_target_rows":octr,
          "new_oct_target_candidates":newly,
          "jan_only_ids":sorted(known-{x["code"] for x in octr}),
          "notes":["The two API snapshots cannot identify all temporary posts absent from both archive dates.",
            "A new Oct row with DATA in historic interval still needs original PDF specialty and publication provenance checks.",
            "A changed ID or updated portal DATA may be a republication, not an additional teaching vacancy.",
            "Captured API.DATA is labeled Data de publicació by archived Jan app JS (V72).",
            "Only public vacancy metadata retained; no applicant names or personal data."]}
    path=Path(output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:result.get(k) for k in ("status","jan_target_count","oct_target_count","oct_in_window_not_in_jan")},ensure_ascii=False),flush=True)
if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("--output",required=True)
    main(a.parse_args().output)
