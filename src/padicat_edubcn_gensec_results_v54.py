#!/usr/bin/env python3
"""V54: Read final 15 GENSEC/GESEC RESULTAT PDFs in PADICAT Jan 2026 snapshot.

No original text or personal identities persisted. Reuse V53 all-page contextual
specialty detection. Results never constitute an additional vacancy by themselves.
"""
import argparse,datetime,json,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from padicat_edubcn_remaining_pdfs_v53 import load_index,check,ROOT

def main(dest):
    rows=load_index()
    targets={}
    for x in rows:
        u=x.get("url") or ""
        name=u.rsplit("/",1)[-1]
        if not u.lower().startswith(ROOT.lower()) or str(x.get("status"))!="200" or not name.lower().endswith(".pdf"):
            continue
        if not re.search(r"GENSEC|GESEC",name,re.I) or not re.search(r"RESULTAT",name,re.I):
            continue
        targets[u]={"url":u,"ts":str(x.get("timestamp") or "")}
    candidates=[]
    counts={"valid_pdf":0,"text_extracted":0,"total_pages":0}
    for row in sorted(targets.values(),key=lambda x:x["url"]):
        a=check(row)
        counts["valid_pdf"]+=int(a.get("valid_pdf",False))
        counts["text_extracted"]+=int(a.get("text_extracted",False))
        counts["total_pages"]+=a.get("pages_read",0)
        if a.get("codes"):
            # Store only previously known or candidate specialty & source URL,
            # never teacher names from result documents.
            candidates.append({k:a[k] for k in ["original_url","capture_time","sha256","codes","pages_read"] if k in a})
    summary={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source":"PADICAT authentic 2026-01-29 PDF archive, GENSEC/GESEC results",
        "total_index_records":len(rows),"result_pdf_count":len(targets),
        **counts,"contextual_specialty_result_candidates":candidates,
        "new_offers_authenticated":0,
        "limits":["Result documents cannot independently certify original publication date or additional unique offer.",
        "Manual comparison with the four known EDUBCN offer IDs required for any target candidate.",
        "Only extractable text, no OCR, all pages checked.",
        "No names, DNI, phone numbers, emails or applicant data saved."]}
    out=Path(dest);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps({k:summary[k] for k in ["result_pdf_count","valid_pdf","text_extracted","total_pages","contextual_specialty_result_candidates"]},ensure_ascii=False))
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",required=True)
    main(p.parse_args().output)
