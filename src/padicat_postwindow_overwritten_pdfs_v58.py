#!/usr/bin/env python3
"""V58: Extended capture-window retrieval of overwritten 2025-26 official DC PDFs.

Follow Library protocol: authentic original URL -> archive metadata -> replay -> actual
PDF bytes -> SHA256 and non-personal specialty/course flags. No raw PDF files or personal
text may be pushed to the public repository. This is a bounded, single-pass probe.
"""
import argparse,datetime,hashlib,json,re,time
from pathlib import Path
import requests,fitz
API="https://wayback.padicat.cat/cdx"
BASE="https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/"
ROOT="personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/"
TARGETS=[
 ("Lleida","resultats",BASE+"lleida/"+ROOT+"LLE-SEC-dificil-cobertura-vacants-cobertes.pdf"),
 ("Lleida","ofertes",BASE+"lleida/"+ROOT+"LLE-SEC-dificil-cobertura-oferta-vacants.pdf"),
 ("Girona","resultats",BASE+"girona/"+ROOT+"GIR-SEC-dificil-cobertura-vacants-cobertes.pdf"),
 ("Girona","ofertes",BASE+"girona/"+ROOT+"GIR-SEC-dificil-cobertura-oferta-vacants.pdf"),
 ("Maresme-Valles Oriental","resultats",BASE+"maresme-valles-oriental/"+ROOT+"MVO-SEC-dificil-cobertura-vacants-cobertes.pdf"),
 ("Barcelones","ofertes_datades",BASE+"barcelones/"+ROOT+"BCO-SEC-dificil-cobertura-oferta-vacants_27022026.pdf"),
]
COURSE25=re.compile(r"(?:curs\s*)?2025\s*[-/–]\s*2026|curs\s*25\s*[-/–]\s*26",re.I)
COURSE26=re.compile(r"(?:curs\s*)?2026\s*[-/–]\s*2027|curs\s*26\s*[-/–]\s*27",re.I)
CODE=re.compile(r"(?<!\w)(?:507|627|F57|F87)(?!\w)",re.I)
UA={"User-Agent":"Mozilla/5.0 (public Catalan archive metadata archival research, rate limited)"}

def index_for(url):
    out={"http_status":None,"index_records":0,"captures":[],"index_error":None}
    try:
        r=requests.get(API,params={"url":url,"output":"json","from":"20260301","to":"20261013","limit":"80"},
            headers=UA,timeout=(10,28))
        out["http_status"]=r.status_code
        if r.status_code!=200:
            out["index_error"]="HTTP_"+str(r.status_code)
            return out
        for line in r.text.splitlines():
            line=line.strip()
            if not line:
                continue
            if not line.startswith("{") and " {" in line:
                line=line.split(" {",1)[1]
                line="{"+line
            if not line.startswith("{"):
                continue
            try:
                row=json.loads(line)
            except ValueError:
                continue
            if not isinstance(row,dict):
                continue
            ts=str(row.get("timestamp") or "")
            if not re.fullmatch(r"\d{14}",ts):
                continue
            out["captures"].append({"timestamp":ts,"status":str(row.get("status") or ""),
                "mime":str(row.get("mime") or ""),"digest":str(row.get("digest") or ""),
                "original":str(row.get("url") or "")})
        out["index_records"]=len(out["captures"])
    except Exception as e:
        out["index_error"]=type(e).__name__+": "+str(e)[:130]
    return out

def replay(cap):
    res={"timestamp":cap["timestamp"],"http_status":None,"pdf_valid":False,
        "course_2025_26":False,"course_2026_27":False,"specialty_tokens":[],
        "size_bytes":0,"sha256":None,"pages":None,"error":None}
    url=cap["original"]
    ts=cap["timestamp"]
    if not url.startswith(("http://","https://")):
        res["error"]="Original URL missing HTTP(S) scheme";return res
    try:
        r=requests.get(f"https://wayback.padicat.cat/{ts}id_/{url}",timeout=(10,32),headers=UA)
        res["http_status"]=r.status_code
        if r.status_code!=200:return res
        blob=r.content
        res["size_bytes"]=len(blob)
        if not blob.startswith(b"%PDF-") or len(blob)>15000000:return res
        res["pdf_valid"]=True
        res["sha256"]=hashlib.sha256(blob).hexdigest()
        with fitz.open(stream=blob,filetype="pdf") as doc:
            res["pages"]=len(doc)
            # All pages: no applicant identities or text persisted.
            text="\n".join(doc[i].get_text("text",sort=True) for i in range(len(doc)))
        res["course_2025_26"]=bool(COURSE25.search(text))
        res["course_2026_27"]=bool(COURSE26.search(text))
        res["specialty_tokens"]=sorted({m.upper() for m in CODE.findall(text)})
    except Exception as e:
        res["error"]=type(e).__name__+": "+str(e)[:120]
    return res

def main(output):
    rows=[]
    for territory,kind,url in TARGETS:
        idx=index_for(url)
        snapshots=[replay(cap) for cap in idx["captures"] if cap["status"]=="200" and "pdf" in cap["mime"].lower()]
        rows.append({"territory":territory,"document_type":kind,"original_url":url,
            "index":idx,"retrieved_pdf_captures":snapshots})
        print(f"{territory}/{kind}: index={idx['index_records']} replay_valid={sum(x['pdf_valid'] for x in snapshots)}",flush=True)
        time.sleep(.65)
    found=[{"territory":r["territory"],"document_type":r["document_type"],
          "url":r["original_url"],**x} for r in rows for x in r["retrieved_pdf_captures"] if x["pdf_valid"]]
    report={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "protocol":"REFERENCIA_RECUPERACIO_HISTORICA_PDF_DC_507_627_F57_F87.md v1.0",
        "archive_provider":"PADICAT public CDX with actual replay",
        "capture_window":"2026-03-01..2026-10-13",
        "original_official_urls_checked":len(rows),
        "indexed_snapshots":sum(x["index"]["index_records"] for x in rows),
        "recovered_pdf_binaries":len(found),
        "recovered_course_2025_26_pdfs":sum(x["course_2025_26"] for x in found),
        "results":rows,
        "warnings":["A zero in an archive is not absence of an offer or of captures elsewhere.",
          "Capture dates are not publication dates. Search date may be after the original PDF was replaced.",
          "Do not add any vacancy to census automatically. Distinguish offer/result and read original proof.",
          "No original PDF body or any teacher/applicant names stored in public output."]}
    dest=Path(output);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({k:report[k] for k in ["original_official_urls_checked","indexed_snapshots",
        "recovered_pdf_binaries","recovered_course_2025_26_pdfs"]},ensure_ascii=False))

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",required=True)
    main(p.parse_args().output)
