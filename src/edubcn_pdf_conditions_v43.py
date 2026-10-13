#!/usr/bin/env python3
"""V43: Audit documentary conditions in the four recovered original EDUBCN PDFs.

All original official PDF files are read into memory, never republished.
Only closed-category facts about workload, target-period dates, ID, and SHA256
are persisted; no applicant identities, personal names, contact data, or text.
"""
import argparse,datetime,hashlib,json,re,requests
from pathlib import Path
import fitz
BASE="exports_padicat/EDUBCN_20260129_V41_TARGET_OFFERS.json"
DATES=re.compile(r"(?<!\d)([0-3]?\d[/.-][01]?\d[/.-]20(?:25|26))(?!\d)")
JFULL=re.compile(r"\b(?:jornada\s+(?:sencera|completa)|(?:sencera|completa)\s+jornada|100\s*%\s*(?:de\s+)?jornada)\b",re.I)
JPART=re.compile(r"\b(?:jornada\s+(?:parcial|redu[iï]da|mitja)|mitja\s+jornada|50\s*%\s*(?:de\s+)?jornada|0[,.]5\s*jornada)\b",re.I)
HOURS=re.compile(r"\b(\d{1,2})(?:[,.]\d+)?\s*(?:hores|h)\s*(?:setmanals|/setmana)\b",re.I)
SPEC=re.compile(r"(?<!\w)(507|627|F57|F87)(?!\w)",re.I)
DATECUES=("data d'inici","data de finalització","data final","data de fi","finalització prevista","durada de la substitució","fi de la substitució","fins al","fins el","jornada","horari")
def process(pdf,code,profile):
 out={"code":code,"original_pdf":pdf,"http":None,"pdf_sha256":None,"is_pdf":False,"pages":0,
      "has_code":False,"has_profile_specialty":False,"full_jornada_literal":False,
      "partial_jornada_literal":False,"workload_class":"not_resolved",
      "weekly_hours_candidates":[],"dates_near_conditions":[],"page_condition_flags":[]}
 try:
  r=requests.get(pdf,timeout=(15,29),headers={"User-Agent":"Mozilla/5.0 (public historic teacher vacancy audit)"})
  out["http"]=r.status_code;b=r.content
  if r.status_code!=200 or not b.startswith(b"%PDF") or len(b)>13_000_000:return out
  out["is_pdf"]=True;out["pdf_sha256"]=hashlib.sha256(b).hexdigest()
  doc=fitz.open(stream=b,filetype="pdf")
  out["pages"]=len(doc)
  lines=[]
  for p in range(len(doc)):
   t=doc[p].get_text("text",sort=True)
   ls=[z.strip() for z in t.splitlines() if z.strip()]
   lines+=ls
   candidate=[(i,line) for i,line in enumerate(ls) if any(w in line.lower() for w in DATECUES)]
   flags=[]
   for idx,line in candidate[:40]:
    around=" ".join(ls[max(0,idx-2):min(len(ls),idx+3)])
    flags.append({"line":idx+1,"has_full":bool(JFULL.search(around)),"has_partial":bool(JPART.search(around)),
      "has_hour_cue":bool(HOURS.search(around)),
      "has_end_cue":bool(re.search("data de (?:finalitzaci[oó]|fi)|finalitzaci[oó] prevista|fins al",around,re.I))})
    for d in DATES.findall(around):
     if d not in out["dates_near_conditions"]:out["dates_near_conditions"].append(d)
    for h in HOURS.findall(around):
     if h not in out["weekly_hours_candidates"]:out["weekly_hours_candidates"].append(h)
   out["page_condition_flags"].append({"page":p+1,"condition_segments":len(candidate),"flags":flags[:25]})
  fulltext="\n".join(lines)
  out["has_code"]=code.replace("_","").lower() in fulltext.replace("_","").replace(" ","").lower()
  out["has_profile_specialty"]=bool(SPEC.search(fulltext))
  out["full_jornada_literal"]=bool(JFULL.search(fulltext))
  out["partial_jornada_literal"]=bool(JPART.search(fulltext))
  out["workload_class"]="full_literal" if out["full_jornada_literal"] and not out["partial_jornada_literal"] else "partial_literal" if out["partial_jornada_literal"] and not out["full_jornada_literal"] else "conflicting_literals" if out["partial_jornada_literal"] and out["full_jornada_literal"] else "not_resolved"
  doc.close()
 except Exception as exc:out["error"]=type(exc).__name__+": "+str(exc)[:120]
 return out
def main(dest):
 src=json.loads(Path(BASE).read_text(encoding="utf-8"))
 results=[process(row["DOC_CONVOCATORIA"],row["CODI"],row["PERFIL"]) for row in src["target_rows"] if row["data_in_interval"]]
 obj={"audited_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "baseline":BASE,"documents_verified":sum(x["http"]==200 and x["is_pdf"] and x["has_code"] for x in results),
      "pdfs":results,
      "cautions":["A full/part-time mention anywhere in PDF is insufficient to prove the advertised actual post's jornada if it is a generic instruction.",
        "Dates nearby a condition keyword may be application deadlines, not assignment end dates.",
        "The original PDF and public historic JSON establish the offer, not automatic course duration.",
        "No PDF texts or personal names published; specific details need manual verification."]}
 p=Path(dest);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({"verified":obj["documents_verified"],"workload":[{"code":x["code"],"class":x["workload_class"],"dates":x["dates_near_conditions"]} for x in results]},ensure_ascii=False),flush=True)
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--output",required=True);args=ap.parse_args();main(args.output)
