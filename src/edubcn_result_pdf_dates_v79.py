#!/usr/bin/env python3
"""V79: verify chronology of two genuine EDUBCN original result PDFs.

Compare PDF internal creation date and bounded date tokens against official
archived portal DATA without exposing any persons. The presence of a result
does not alone establish time of first offer publication.
"""
import argparse,datetime,hashlib,json,re
from pathlib import Path
import requests
import fitz
BASE=Path("exports_padicat/EDUBCN_20260129_V41_TARGET_OFFERS.json")
UA={"User-Agent":"Mozilla/5.0 (public archival result notice temporal audit)"}
PAT_DATE=re.compile(r"(?<!\d)(?:[0-3]?\d[/.-][01]?\d[/.-]20(?:25|26)|20(?:25|26)[/.-][01]?\d[/.-][0-3]?\d)(?!\d)")
STATUS=re.compile(r"alta\s+(?:del\s+)?titular|adjudicad[oa]|adjudicaci[oó]|ren[uú]ncia|desert[ao]|sense adjudicar",re.I)
def get(url):
    meta={"url":url,"http":None,"pdf":False,"bytes":None,"sha256":None,
         "pages":None,"creation_date":None,"mod_date":None,
         "date_tokens":[],"status_indicators":[],"errors":None}
    try:
        r=requests.get(url,headers=UA,timeout=(10,34))
        meta["http"]=r.status_code
        if r.status_code!=200:return meta
        body=r.content
        meta["bytes"]=len(body)
        if not body.startswith(b"%PDF-") or len(body)>7000000:return meta
        meta["sha256"]=hashlib.sha256(body).hexdigest()
        with fitz.open(stream=body,filetype="pdf") as doc:
            meta["pdf"]=True
            meta["pages"]=len(doc)
            extra=doc.metadata or {}
            meta["creation_date"]=extra.get("creationDate")
            meta["mod_date"]=extra.get("modDate")
            words="\n".join(doc[i].get_text("text",sort=True) for i in range(len(doc)))
        meta["date_tokens"]=sorted(set(PAT_DATE.findall(words)))[:40]
        meta["status_indicators"]=sorted(set(x.group(0) for x in STATUS.finditer(words)))[:15]
    except Exception as e:meta["errors"]=type(e).__name__+": "+str(e)[:140]
    return meta
def main(dest):
    source=json.loads(BASE.read_text(encoding="utf-8"))
    tests=[]
    for record in source["target_rows"]:
        if not record.get("DOC_RESULTAT"):continue
        url=record["DOC_RESULTAT"]
        live=get(url)
        tests.append({"code":record["CODI"],"portal_date":record["DATA"],"current_result_pdf":live})
        print(record["CODI"],live["http"],live["creation_date"],live["date_tokens"],flush=True)
    out={"timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "sources":"V41 PADICAT Jan 2026 API, only existing official result PDF URL links",
         "result_pdf_urls":len(tests),
         "valid_pdfs":sum(bool(x["current_result_pdf"]["pdf"]) for x in tests),
         "tests":tests,
         "warnings":["Result PDFs are checked as currently served and may be updated since January. Do not claim immutable archival provenance without confirming PADICAT snapshot.",
              "Document creation date is not posting date, decision date, or date when titular returned.",
              "Only date tokens and categorical status phrases from public PDF are retained, never names or scores.",
              "A matching or older decision date does not by itself certify first-ever publication of the vacancy."]}
    path=Path(dest);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"checked":out["result_pdf_urls"],"valid":out["valid_pdfs"]}),flush=True)
if __name__=="__main__":
    x=argparse.ArgumentParser();x.add_argument("--output",required=True);main(x.parse_args().output)
