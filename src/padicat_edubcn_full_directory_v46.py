#!/usr/bin/env python3
"""V46: Classify PADICAT Jan-2026 EDUBCN /rcs_gene/seleccio/ archive listing.

Metadata only: collect counts of archived original PDFs, results, filenames with
historic 2025/26 clues, anonymized document labels; source PDFs not downloaded.
"""
import argparse,datetime,json,re,collections
from pathlib import Path
import requests
URL="https://www.edubcn.cat/rcs_gene/seleccio/"
API="https://wayback.padicat.cat/cdx"
MIME={"application/pdf","application/x-pdf"}
PUBLIC_COURSE=re.compile(r"(?:2526|2025[-_/]?2026|2026[-_/]?2025|2025|2026)",re.I)
TARGET=re.compile(r"(?<!\d)(?:507|627|F57|F87)(?!\d)|inform[aà]tica|ciber|sistemes\s+i\s+aplicacions|pfi",re.I)
CODE=re.compile(r"(?:GENSEC|GESEC)[_-]?(?:2526)?[_-]?\d+",re.I)
def load():
 r=requests.get(API,params={"url":URL,"matchType":"prefix","output":"json","from":"20251101","to":"20260305","limit":"500"},
     timeout=(12,45),headers={"User-Agent":"Mozilla/5.0 (public archive indexed vacancy inventory)"})
 if r.status_code!=200:raise RuntimeError("CDX HTTP "+str(r.status_code))
 return [json.loads(x) for x in r.text.splitlines() if x.lstrip().startswith("{")]
def main(file):
 rows=load()
 good=[]
 for x in rows:
  u=str(x.get("url") or "")
  if ".pdf" not in u.lower() or str(x.get("status"))!="200":continue
  if not u.lower().startswith("https://www.edubcn.cat/rcs_gene/seleccio/"):continue
  base=u.rsplit("/",1)[-1]
  result=bool(re.search(r"(?:_res(?:ultat|ultats?)|[-_]adjudic|resultat)",base,re.I))
  good.append({"original_url":u,"captured":str(x.get("timestamp","")),"is_result":result,
     "has_2025_26_year_text":bool(PUBLIC_COURSE.search(base)),"target_filename":bool(TARGET.search(base)),
     "has_GENSEC":bool(CODE.search(base)),
     "code":(CODE.search(base).group(0) if CODE.search(base) else "")})
 unique={(x["original_url"],x["captured"]):x for x in good}
 good=list(unique.values())
 offered=[x for x in good if not x["is_result"]]
 non_gensec=[x for x in offered if not x["has_GENSEC"]]
 # File list is an internal input. Results json includes URL only for potentially
 # relevant non-GENSEC courses, no broad collection of file names possibly containing names.
 output={"audited_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
   "capture_interval":"2025-11-01..2026-03-05",
   "cdx_rows":len(rows),"unique_200_pdf_captures":len(good),
   "original_pdf_count":len(offered),"results_pdf_count":len(good)-len(offered),
   "gensec_original_pdf_count":sum(x["has_GENSEC"] for x in offered),
   "other_original_pdf_count":len(non_gensec),
   "year_hint_non_gensec_count":sum(x["has_2025_26_year_text"] for x in non_gensec),
   "target_hint_non_gensec_count":sum(x["target_filename"] for x in non_gensec),
   "year_or_target_hint_non_gensec":[x for x in non_gensec if x["has_2025_26_year_text"] or x["target_filename"]][:120],
   "warning":["Capture date does not certify posting date.",
      "Archived URL can refer to other education jobs or old courses.",
      "Filename hints are only candidates; retrieve PDF and verify actual specialty and publication period.",
      "Do not count _RESULTAT documents as original vacancies."]}
 p=Path(file);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({k:output[k] for k in ("cdx_rows","unique_200_pdf_captures","original_pdf_count","results_pdf_count","gensec_original_pdf_count","other_original_pdf_count","year_hint_non_gensec_count","target_hint_non_gensec_count")},ensure_ascii=False))
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--output",required=True);main(a.parse_args().output)
