#!/usr/bin/env python3
"""V75: PDF creation metadata vs dated EDUBCN listing of old Jan 2026 PDFs.

Analyze four original public PDF notices only, no candidates or personal
content stored. Creation/modification metadata may predate Jan portal listing:
this is file history, NOT legal proof of publication.
"""
import argparse,datetime,hashlib,json,re,time
from pathlib import Path
from urllib.parse import quote
import requests,fitz
BASE=Path(__file__).resolve().parents[1]
API=BASE/"exports_padicat/EDUBCN_20260129_V41_TARGET_OFFERS.json"
UA={"User-Agent":"Mozilla/5.0 (noncommercial public historical PDF metadata research)"}
def pull(url,limit=6000000):
    o={"http":None,"size_bytes":None,"sha256":None,"is_pdf":False,"error":None}
    data=b""
    try:
        r=requests.get(url,headers=UA,timeout=(10,32),stream=True)
        o["http"]=r.status_code
        if r.status_code==200:
            b=bytearray()
            for piece in r.iter_content(32768):
                b+=piece
                if len(b)>limit:o["error"]="limit";break
            data=bytes(b)
            o["size_bytes"]=len(data)
            o["is_pdf"]=data.startswith(b"%PDF-") and not o["error"]
            if o["is_pdf"]:o["sha256"]=hashlib.sha256(data).hexdigest()
        r.close()
    except Exception as e:o["error"]=type(e).__name__+": "+str(e)[:110]
    return o,data
def cdx(url):
    p={"url":url,"matchType":"exact","from":"20260129","to":"20260130","output":"json","limit":"6"}
    out={"http":None,"captures":[],"error":None}
    try:
        r=requests.get("https://wayback.padicat.cat/cdx",params=p,headers=UA,timeout=(10,30))
        out["http"]=r.status_code
        if r.status_code==200:
            for l in r.text.splitlines():
                try:x=json.loads(l)
                except ValueError:continue
                if isinstance(x,dict) and re.fullmatch(r"\d{14}",str(x.get("timestamp") or "")):
                    out["captures"].append({k:x.get(k) for k in ("timestamp","url","status","digest","mime")})
    except Exception as e:out["error"]=type(e).__name__+": "+str(e)[:110]
    return out
def safe_meta(blob):
    if not blob.startswith(b"%PDF-"):return {"valid":False}
    try:
        with fitz.open(stream=blob,filetype="pdf") as doc:
            meta=doc.metadata or {}
            fields={k:meta.get(k) for k in ("creationDate","modDate")}
            return {"valid":True,"pages":len(doc),**fields}
    except Exception as e:return {"valid":False,"error":type(e).__name__+": "+str(e)[:100]}
def main(output):
    original=json.loads(API.read_text(encoding="utf-8"))
    expected={x["code"]:x for x in original["original_pdf_checks"]}
    results=[]
    for row in original["target_rows"]:
        code=row["CODI"];url=row["DOC_CONVOCATORIA"]
        live,bytes_live=pull(url)
        meta=safe_meta(bytes_live) if live["is_pdf"] else None
        index=cdx(url)
        old=[]
        for item in index["captures"][:3]:
            if str(item.get("status"))!="200":continue
            archived_url="https://wayback.padicat.cat/"+str(item["timestamp"])+"id_/"+url
            got,raw=pull(archived_url)
            old.append({"stamp":item["timestamp"],"archive_request":got,
                        "metadata":safe_meta(raw) if got["is_pdf"] else None})
        known=expected[code]
        results.append({"id":code,"specialty":row["PERFIL"].split(" ")[0],
                        "portal_pubdate":row["DATA"],"original_url":url,
                        "expected_original_sha_from_V41":known["pdf_sha256"],
                        "live":live,"live_sha_matches_V41":live["sha256"]==known["pdf_sha256"],
                        "live_metadata":meta,"archive_index":index,
                        "replayed_historical_versions":old})
        print(code,"live",live["http"],"matched",live["sha256"]==known["pdf_sha256"],
              "capture_count",len(index["captures"]),flush=True)
        time.sleep(.6)
    data={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "source":"EDUBCN four 2025-26 original PDFs already authenticated at V41, V52 and V73",
       "documents":len(results),
       "pdfs_valid":sum(bool(x["live"]["is_pdf"]) for x in results),
       "sha_matches_V41":sum(bool(x["live_sha_matches_V41"]) for x in results),
       "jan2026_pdf_capture_records":sum(len(x["archive_index"]["captures"]) for x in results),
       "jan2026_pdf_versions_replayed":sum(len(x["replayed_historical_versions"]) for x in results),
       "results":results,
       "warnings":["Metadata creationDate/modDate may be blank, forged, stale or rewritten and is not public posting date.",
                   "Historical PDF snapshot timestamps are capture dates, not original announcement dates.",
                   "A PDF deadline in December 2025 and an API listing date in Jan 2026 may signal old publication, republication or inconsistent metadata.",
                   "No PDF text, author field, staff names, applications or identifying data persisted."]}
    p=Path(output);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:data[k] for k in ("documents","pdfs_valid","sha_matches_V41",
       "jan2026_pdf_capture_records","jan2026_pdf_versions_replayed")}))
if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("--output",required=True);main(a.parse_args().output)
