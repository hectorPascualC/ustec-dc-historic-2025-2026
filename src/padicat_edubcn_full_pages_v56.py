#!/usr/bin/env python3
"""V56: Re-audit all pages of V47's 87 EDUBCN noncoded PDF documents.

V47 read at most seven pages, so no absence claim was complete for long PDFs.
The shared V53 contextual classifier reads all extractable pages. Reports no PII.
"""
import argparse,concurrent.futures,datetime,json
from pathlib import Path
from padicat_edubcn_remaining_pdfs_v53 import load_index,check,ROOT,OLD_GENSEC,OLD_EXCLUSIONS

def main(dest):
    raw=load_index()
    items={}
    for row in raw:
        url=str(row.get("url") or "")
        if not url.lower().startswith(ROOT.lower()) or not url.lower().endswith(".pdf") or str(row.get("status"))!="200":
            continue
        filename=url.rsplit("/",1)[-1]
        if OLD_GENSEC.search(filename) or OLD_EXCLUSIONS.search(filename):
            continue
        items[url]={"url":url,"ts":str(row.get("timestamp") or "")}
    selected=sorted(items.values(),key=lambda x:x["url"])
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        results=list(pool.map(check,selected))
    matches=[{k:r[k] for k in ["original_url","capture_time","sha256","codes","pages_read"] if k in r}
        for r in results if r.get("codes")]
    report={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "scope":"Repeat V47 archive documents but read all extractable pages rather than 7",
        "expected_v47_count":87,"selected":len(selected),
        "valid_pdf":sum(r.get("valid_pdf",False) for r in results),
        "text_available":sum(r.get("text_extracted",False) for r in results),
        "total_pages_read":sum(r.get("pages_read",0) for r in results),
        "documents_longer_than_7_pages":sum(r.get("pages_read",0)>7 for r in results),
        "max_pages_in_document":max((r.get("pages_read",0) for r in results),default=0),
        "contextual_candidates":matches,
        "candidate_count":len(matches),
        "errors":[{"url_hash":r["url_hash"],"error_type":r.get("error_type",r.get("error",""))}
            for r in results if r.get("error") or r.get("error_type")],
        "cautions":["No visual OCR for image-only pages","PDF result is not evidence of a new offer",
            "The archive index is one-day snapshot, not complete original publication history",
            "No personal names or original PDF contents persisted."]}
    if len(selected)!=87:
        report["coverage_warning"]="V47 expected 87, current selection differs; do not call complete."
    path=Path(dest);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps({k:report[k] for k in ["selected","valid_pdf","text_available",
        "total_pages_read","documents_longer_than_7_pages","max_pages_in_document","candidate_count"]},ensure_ascii=False))
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",required=True)
    main(p.parse_args().output)
