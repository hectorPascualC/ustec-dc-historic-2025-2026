#!/usr/bin/env python3
"""V84 — Independent row-level QA of all Oct PADICAT PDFs mentioning 2025-26.

V82 read 309 real October delta PDFs and detected 15 with course text.
Re-read ALL of those 15 with a corrected explicit specialty parser that
must not record empty specialty strings. Do not export names/full source.
"""
import argparse,datetime,hashlib,json,re,time
from pathlib import Path
import requests,fitz
INPUT=Path("exports_padicat/EDUBCN_V82_FULL_OCT_DELTA_2025_26.json")
HEAD={"User-Agent":"Mozilla/5.0 (public archived education PDF re-audit, non-commercial)"}
CODES=re.compile(r"(?<![A-Za-z0-9])(507|627|F57|F87)(?![A-Za-z0-9])",re.I)
CONTEXT=re.compile(r"(?i)(?:especialitat|especialidad|perfil|especialitats|codi\s*especialitat|F57|F87|inform[aàá]tic|sistemes\s+i\s+aplicacions|sistemas\s+y\s+aplicaciones)")
DOC_KIND=re.compile(r"(?i)(?:dif[ií]cil\s+cobertura|dif[ií]cil\s+provisi[oó]|convocat[oò]ria|oferta\s+de\s+vacants|selecci[oó]\s+de\s+personal)")
def parse(row):
    out={"url":row["original_url"],"stamp":row["capture_timestamp"],"status":None,
         "valid_pdf":False,"sha256":None,"expected_sha_matches":False,
         "pages":None,"token_count":{"507":0,"627":0,"F57":0,"F87":0},
         "specialty_context_codes":[],"possible_target":False,
         "has_recruitment_wording":False,"file_2025_26_name":False,
         "pdf_2025_26_mention":False,"error":None}
    u="https://wayback.padicat.cat/"+row["capture_timestamp"]+"id_/"+row["original_url"]
    try:
        r=requests.get(u,headers=HEAD,timeout=(11,35),stream=True)
        out["status"]=r.status_code
        if r.status_code!=200:return out
        body=bytearray()
        for c in r.iter_content(32768):
            body.extend(c)
            if len(body)>10000000:out["error"]="exceeds_10MB";return out
        blob=bytes(body)
        if not blob.startswith(b"%PDF-"):return out
        with fitz.open(stream=blob,filetype="pdf") as doc:
            out["pages"]=len(doc)
            txt="\n".join(doc[i].get_text(sort=True) for i in range(len(doc)))
        out["valid_pdf"]=True
        out["sha256"]=hashlib.sha256(blob).hexdigest()
        out["expected_sha_matches"]=out["sha256"]==row["sha256"]
        out["has_recruitment_wording"]=bool(DOC_KIND.search(txt))
        out["file_2025_26_name"]=bool(re.search(r"2526|25[-_]26|2025",row["original_url"],re.I))
        out["pdf_2025_26_mention"]=bool(re.search(r"2025\s*[-/–]\s*2026|\b2526\b|curs\s*2025.2026",txt,re.I))
        matches=CODES.findall(txt)
        for code in matches:out["token_count"][code.upper()]+=1
        explicit=[]
        for line in txt.splitlines():
            if not CONTEXT.search(line):continue
            for code in CODES.findall(line):
                explicit.append(code.upper())
        out["specialty_context_codes"]=sorted(set(explicit))
        out["possible_target"]=bool(explicit and out["has_recruitment_wording"])
    except Exception as e:out["error"]=type(e).__name__+": "+str(e)[:160]
    return out
def main(destination):
    data=json.loads(INPUT.read_text(encoding="utf-8"))
    candidates=[x for x in data["delta_checks"] if x["has_period_2025_26"]]
    assert len(candidates)==15, "V82 expected 15 course 2025-26 candidate docs; check input revision"
    checked=[]
    for x in candidates:
        result=parse(x);checked.append(result)
        print(result["url"].rsplit("/",1)[-1][:95],result["status"],
              result["specialty_context_codes"],flush=True)
        time.sleep(.4)
    result={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source_file":str(INPUT),"candidate_2025_26_pdf_count":len(candidates),
        "checked_pdf_count":len(checked),
        "valid_pdf":sum(x["valid_pdf"] for x in checked),
        "hashes_equal_v82":sum(x["expected_sha_matches"] for x in checked),
        "with_any_target_code_token":sum(any(v>0 for v in x["token_count"].values()) for x in checked),
        "with_specialty_context":sum(len(x["specialty_context_codes"])>0 for x in checked),
        "potential_official_2025_26_target":sum(x["possible_target"] for x in checked),
        "positive_candidates":[x for x in checked if x["possible_target"]],
        "checks":checked,
        "warnings":["Course mention in an administrative PDF is not proof that the PDF is a difficult-coverage vacancy in that academic year.",
            "Specialty code in any administrative document is not proof of a single open vacancy.",
            "A positive hit requires reading dates and original public offer before census insertion.",
            "No candidate names/contacts/text stored; no OCR for image-based PDF pages."]}
    p=Path(destination);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in ("checked_pdf_count","valid_pdf","hashes_equal_v82",
         "with_any_target_code_token","with_specialty_context","potential_official_2025_26_target")}),flush=True)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",required=True);main(p.parse_args().output)
