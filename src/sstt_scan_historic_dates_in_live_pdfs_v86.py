#!/usr/bin/env python3
"""V86 — Scan ALL currently linked SSTT PDFs for overlooked 2025-11..2026-02
dates (D/M/YYYY etc) adjacent to 507/627/F57/F87. Not only 'curs 25-26'.

The 2026 live PDF can retain a 2026 date despite missing '2025-2026' text.
Never infer date of original PUBLICATION from date of incorporation/deadline.
Keep SHA/page/date/specialty provenance; no candidate personal info or text.
"""
import argparse,csv,datetime,hashlib,json,re,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
import requests,fitz
SRC=Path("exports_territorial/SSTT_PDFS.csv")
DATES=re.compile(r"(?<!\d)([0123]?\d)[/.-]([01]?\d)[/.-](20(?:25|26))(?!\d)|(?<!\d)(20(?:25|26))[/.-]([01]?\d)[/.-]([0123]?\d)(?!\d)")
TARGET=re.compile(r"(?<![A-Za-z0-9])(507|627|F57|F87)(?![A-Za-z0-9])",re.I)
SEMANTIC=re.compile(r"(?i)(?:especialitat|especialidad|perfil)[\s:|\-–]{0,20}(507|627|F57|F87)\b|(?:^|\n)\s*(507|627|F57|F87)\s+\S")
HEAD={"User-Agent":"Mozilla/5.0 (public historical teaching vacancies transparency archive audit)"}
def fmt(match):
    p=match.groups()
    try:
        if p[0] is not None:day,month,year=int(p[0]),int(p[1]),int(p[2])
        else:day,month,year=int(p[5]),int(p[4]),int(p[3])
        d=datetime.date(year,month,day)
    except (ValueError,TypeError):return None
    return d.isoformat() if datetime.date(2025,11,1)<=d<=datetime.date(2026,2,28) else None
def scan(row):
    out={"area":row["territori"],"type":row["tipus"],
      "original_url":row["url"],"http":None,"is_pdf":False,
      "pages":0,"sha256":None,
      "pages_with_historical_date":0,"pages_with_specialty_any":0,
      "pages_with_both_target_and_historic_date":0,
      "possible_blocks":[],"all_historic_dates":[],"error":None}
    try:
        r=requests.get(row["url"],headers=HEAD,timeout=(12,40),stream=True)
        out["http"]=r.status_code
        if r.status_code!=200:return out
        data=bytearray()
        for part in r.iter_content(65536):
            data+=part
            if len(data)>14000000:out["error"]="large_file";return out
        raw=bytes(data)
        if not raw.startswith(b"%PDF-"):return out
        out["is_pdf"]=True;out["sha256"]=hashlib.sha256(raw).hexdigest()
        found=set()
        with fitz.open(stream=raw,filetype="pdf") as pdf:
            out["pages"]=len(pdf)
            for pageno,page in enumerate(pdf):
                txt=page.get_text(sort=True)
                ds=sorted(set(filter(None,(fmt(m) for m in DATES.finditer(txt)))))
                codes=sorted(set(x.upper() for x in TARGET.findall(txt)))
                semantic=sorted(set((m.group(1) or m.group(2)).upper() for m in SEMANTIC.finditer(txt)))
                if ds:out["pages_with_historical_date"]+=1;found.update(ds)
                if codes:out["pages_with_specialty_any"]+=1
                if ds and codes:
                    out["pages_with_both_target_and_historic_date"]+=1
                    # Only count same-page as weak lead, not unique offer/true date.
                    for date in ds:
                        for code in codes:
                            positions=[m.start() for m in TARGET.finditer(txt) if m.group(1).upper()==code]
                            date_positions=[m.start() for m in DATES.finditer(txt) if fmt(m)==date]
                            minimum=min((abs(a-b) for a in positions for b in date_positions),default=100000)
                            if minimum>700:continue
                            out["possible_blocks"].append({"page":pageno+1,
                                "date":date,"code":code,
                                "distance_chars":minimum,
                                "explicit_specialty_header":code in semantic,
                                "evidence_grade":"LEAD_ONLY_DATE_NOT_PUBLICATION"})
        out["all_historic_dates"]=sorted(found)
    except Exception as e:out["error"]=type(e).__name__+": "+str(e)[:150]
    return out
def main(output):
    with SRC.open(encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
    areas=set(x["territori"] for x in rows)
    assert len(rows)==30 and len(areas)==11, "Expected 30 official PDF links/11 SSTT V24"
    checks=[]
    with ThreadPoolExecutor(max_workers=5) as pool:
        future={pool.submit(scan,row):row for row in rows}
        for ft in as_completed(future):
            x=ft.result();checks.append(x)
            print(x["area"],x["type"],x["http"],x["pages"],
                  "in_window",len(x["all_historic_dates"]),
                  "weak_leads",len(x["possible_blocks"]),flush=True)
    checks.sort(key=lambda x:(x["area"],x["type"],x["original_url"]))
    by_territory=[]
    for area in sorted(areas):
        a=[x for x in checks if x["area"]==area]
        by_territory.append({"area":area,"pdf_urls_checked":len(a),
          "valid_pdf":sum(x["is_pdf"] for x in a),
          "date_mentions":sum(len(x["all_historic_dates"]) for x in a),
          "same_page_weak_target_date_leads":sum(len(x["possible_blocks"]) for x in a)})
    report={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "purpose":"Independent V24 PDF recheck for overlooked D/M/YYYY Nov 2025-Feb 2026 next to exact specialty codes",
      "reference":"exports_territorial/SSTT_PDFS.csv",
      "distinct_territories":len(areas),
      "pdfs_checked":len(checks),"valid_pdfs":sum(x["is_pdf"] for x in checks),
      "pdfs_with_target_and_date_on_same_page":sum(x["pages_with_both_target_and_historic_date"]>0 for x in checks),
      "weak_date_specialty_leads":sum(len(x["possible_blocks"]) for x in checks),
      "total_pdf_http_errors":sum(x["http"]!=200 for x in checks),
      "areas":by_territory,"documents":checks,
      "warnings":["A date D/M/YYYY on an official PDF may be incorporation, end/deadline or background text, NOT the original publication date.",
        "Same page may list multiple different staff posts: specialty + date near each other does not verify a single vacancy.",
        "Live PDF may already have been overwritten since the 2025-26 period.",
        "No original applicant names, full text, personal identifiers, rankings or contacts exported.",
        "Only source-derived true 507/627/F57/F87 opportunities with publication evidence can be added to the census."]}
    out=Path(output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:report[k] for k in ("distinct_territories","pdfs_checked",
         "valid_pdfs","pdfs_with_target_and_date_on_same_page","weak_date_specialty_leads",
         "total_pdf_http_errors")}),flush=True)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",required=True);main(p.parse_args().output)
