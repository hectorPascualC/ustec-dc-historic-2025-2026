#!/usr/bin/env python3
"""V77: audit temporal gaps in the BCO sequence of original dated official PDFs.

Generate ONLY candidate URL names, not assumed actual documents, from known
original official dated weekly files V22. Probe 6 missing Fridays with 3
historically observed filename styles. Only HTTP200+PDF signature+valid body
can certify an original file. Do not add any vacancy from a guessed URL.
"""
import argparse,csv,datetime,hashlib,json,re,time
from pathlib import Path
from urllib.parse import urlparse
import requests
import fitz
SOURCE=Path("cens/INDEX_PDFS_BCO_V22_11_LOTS.csv")
BASE="https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/barcelones/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/"
MISSING=[
 "2025-11-21","2025-12-12","2025-12-19",
 "2025-12-26","2026-01-02","2026-01-09"]
TARGET=re.compile(r"(?<!\w)(?:507|627|F57|F87)(?!\w)",re.I)
UA={"User-Agent":"Mozilla/5.0 (public historical education archive gap audit; research)"}
def known():
    with SOURCE.open(encoding="utf-8-sig",newline="") as f: data=list(csv.DictReader(f))
    assert len(data)==11,"Bco known weekly corpus changed"
    return {x["data_nom_fitxer"] for x in data}
def variants(date):
    compact=date.replace("-","")
    dmy=date[8:10]+date[5:7]+date[:4]
    return [
        BASE+"Barcelones-SEC-dificil-cobertura-oferta-vacants_"+dmy+".pdf",
        BASE+"BCO-SEC-dificil-cobertura-oferta-vacants"+dmy+".pdf",
        BASE+"BCO-SEC-dificil-cobertura-oferta-vacants_"+dmy+".pdf",
    ]
def fetch(url):
    result={"url":url,"http":None,"final_url":None,"content_type":None,
        "bytes":None,"pdf_verified":False,"sha256":None,"pages":None,
        "specialty_code_tokens":[],"date_markers":[],"error":None}
    try:
        r=requests.get(url,headers=UA,timeout=(9,18),stream=True,allow_redirects=True)
        result["http"]=r.status_code
        result["final_url"]=r.url
        result["content_type"]=r.headers.get("content-type","")
        if r.status_code!=200:return result
        b=bytearray()
        for chunk in r.iter_content(32768):
            b.extend(chunk)
            if len(b)>8000000:
                result["error"]="content_size_limit";return result
        raw=bytes(b);result["bytes"]=len(raw)
        if not raw.startswith(b"%PDF-"):return result
        with fitz.open(stream=raw,filetype="pdf") as doc:
            result["pages"]=len(doc)
            txt="\n".join(doc[i].get_text(sort=True) for i in range(len(doc)))
        result["pdf_verified"]=True
        result["sha256"]=hashlib.sha256(raw).hexdigest()
        result["specialty_code_tokens"]=sorted(set(TARGET.findall(txt)))
        result["date_markers"]=sorted(set(re.findall(r"\b(?:2025|2026)[-/]\d\d[-/]\d\d\b",txt)))[:25]
    except Exception as ex:result["error"]=type(ex).__name__+": "+str(ex)[:110]
    return result
def main(path):
    known_dates=known()
    for date in MISSING:
        assert date not in known_dates,"Unexpectedly date already in source inventory"
    checks=[]
    for date in MISSING:
        for url in variants(date):
            x=fetch(url);x["candidate_date"]=date;checks.append(x)
            print(date,urlparse(url).path.rsplit("/",1)[-1],x["http"],x["pdf_verified"],flush=True)
            time.sleep(.45)
    report={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "known_dated_lots":len(known_dates),
        "missing_weekly_nominal_dates":MISSING,
        "candidate_url_patterns":3,
        "candidate_urls_tested":len(checks),
        "http_200":sum(x["http"]==200 for x in checks),
        "http_404":sum(x["http"]==404 for x in checks),
        "other_http_or_technical":sum(x["http"] not in (200,404) for x in checks),
        "verified_pdf_bodies":sum(x["pdf_verified"] for x in checks),
        "candidate_records":checks,
        "warnings":["Names were guessed solely as candidates from empirically observed templates, not verified publication.",
            "A 404 now can result from later deletion, not proof of no 2025-26 weekly publication.",
            "Dates of known PDF names are not proof of release dates; omitted weekly date may be holiday or no new notice.",
            "Only valid original PDF body and specialty/date evidence can create an offer candidate.",
            "No names, application forms, applicant identifiers, contacts or raw body text saved."]}
    dest=Path(path);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:report[k] for k in
        ("candidate_urls_tested","http_200","http_404","other_http_or_technical","verified_pdf_bodies")}),flush=True)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",required=True);main(p.parse_args().output)
