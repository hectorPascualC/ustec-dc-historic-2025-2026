#!/usr/bin/env python3
"""V72: EDUBCN historical bundle provenance and public API route discovery.

Check if the Jan 2026 HTML's actual JS application bundle survives in PADICAT,
and compare static endpoint patterns with current bundle (not historical proof).
No app source text or secrets persisted, only bounded route and keyword counts.
"""
import argparse,datetime,hashlib,json,re,time
from pathlib import Path
import requests
API="https://wayback.padicat.cat/cdx"
JS="https://www.edubcn.cat/pdc/js/app.bundle-v05.js"
UA={"User-Agent":"Mozilla/5.0 (bounded public archival JS metadata inspection)"}
KEYS=["pdc_rest","convocatories","convocat","curs","filter","resultat","ofert","api/","http","rest/","pag"]
def fetch(url):
    result={"url":url,"status":None,"len":0,"sha256":None,"error":None}
    blob=b""
    try:
        r=requests.get(url,headers=UA,timeout=(9,30),stream=True)
        result["status"]=r.status_code
        if r.status_code==200:
            b=bytearray()
            for chunk in r.iter_content(32768):
                b+=chunk
                if len(b)>1600000:result["error"]="limit";break
            blob=bytes(b)
            result["len"]=len(blob)
            if not result["error"]:result["sha256"]=hashlib.sha256(blob).hexdigest()
        r.close()
    except Exception as e:result["error"]=type(e).__name__+": "+str(e)[:100]
    return result,blob
def cdx():
    r,body=fetch(API+"?url="+requests.utils.quote(JS,safe="")+
       "&matchType=exact&output=json&from=20251201&to=20260301&limit=80")
    rows=[]
    if r["status"]==200:
        for line in body.decode("utf-8","replace").splitlines():
            if not line.lstrip().startswith("{"):continue
            try:x=json.loads(line)
            except ValueError:continue
            if isinstance(x,dict) and re.fullmatch(r"\d{14}",str(x.get("timestamp") or "")):
                rows.append({k:x.get(k) for k in
                    ("url","timestamp","mime","status","digest","length")})
    return r,rows
def fingerprint(source,label):
    stat,blob=fetch(source)
    txt=blob.decode("utf-8","replace")
    strings=[]
    for m in re.finditer(r"['\"]([^'\"]{4,180})['\"]",txt):
        token=m.group(1)
        if any(k in token.lower() for k in ("convocat","pdc_rest","/rest/","/api/","/pdc/","curs","resultat","filtr")):
            if not re.search(r"(?i)(password|passwd|api[_-]?key|authorization|bearer|token=)",token):
                strings.append(token[:130])
    strings=sorted(set(strings))[:85]
    indicators={k:len(list(re.finditer(re.escape(k),txt,re.I))) for k in KEYS}
    return {"type":label,"download":stat,"keyword_counts":indicators,
            "public_route_string_candidates":strings}
def main(path):
    meta,captures=cdx()
    probe=[fingerprint(JS,"LIVE_JAVASCRIPT_NOT_HISTORICAL")]
    for cap in captures[:3]:
        if str(cap.get("status"))=="200":
            u="https://wayback.padicat.cat/"+str(cap["timestamp"])+"id_/"+JS
            probe.append(fingerprint(u,"PADICAT_ARCHIVED_"+str(cap["timestamp"])))
    report={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "historical_html_source":"https://wayback.padicat.cat/20260129224629id_/https://www.edubcn.cat/ca/professorat_i_pas/seleccio_rrhh/dificil_cobertura",
            "known_js_bundle":JS,"padicat_index_request":meta,
            "padicat_js_captures":captures,"versions":probe,
            "warnings":["Live JS is current and must not be called a January 2026 bundle.",
                "Potential strings are public JS metadata only, not proof of API data retained or historic offers.",
                "Never store credentials, names, staff data, script bodies, or applicant details.",
                "Capture date is not publication date."]}
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"capture_metadata":len(captures),
        "version_checks":len(probe),"status":[x["download"]["status"] for x in probe],
        "strings":[len(x["public_route_string_candidates"]) for x in probe]},ensure_ascii=False),flush=True)
if __name__=="__main__":
    x=argparse.ArgumentParser();x.add_argument("--output",required=True);main(x.parse_args().output)
