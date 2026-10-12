#!/usr/bin/env python3
"""Territorial public-source inventory; does not claim historical completeness.
Only vacancy metadata; NEVER publish personal names, emails, telephones or PDF body.
"""
import argparse, concurrent.futures, csv, datetime, hashlib, io, json, re, time
from urllib.parse import urljoin, urlparse
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import fitz

ROOT="https://educacio.gencat.cat/ca/departament/serveis-territorials"
TERRITORIES=[
 ("Alt Pirineu i Aran","alt-pirineu-aran"),
 ("Baix Llobregat","baix-llobregat"),
 ("Barcelonès","barcelones"),
 ("Catalunya Central","catalunya-central"),
 ("Girona","girona"),
 ("Lleida","lleida"),
 ("Maresme–Vallès Oriental","maresme-valles-oriental"),
 ("Penedès","penedes"),
 ("Tarragona","tarragona"),
 ("Terres de l'Ebre","terres-ebre"),
 ("Vallès Occidental","valles-occidental")
]
URL_SUFFIX="/personal-docent/nomenaments-telematics/dificil-cobertura"
EXTRA=[("Consorci d'Educació de Barcelona","EDUBCN","https://www.edubcn.cat/ca/professorat_i_pas/seleccio_rrhh/dificil_cobertura")]
UA="Mozilla/5.0 (compatible; HistoricalDC-Research/1.0; educational public records)"
DATE_RE=re.compile(r"\b(?:(?:0?[1-9]|[12]\d|3[01])[/.-](?:0?[1-9]|1[012])[/.-]20(?:25|26))\b")
CODES_RE=re.compile(r"(?<!\d)(?:507|627|F57|F87)(?!\d)",re.I)
RE_COURSE_OLD=re.compile(r"2025\s*[-/]\s*2026")
RE_COURSE_NEW=re.compile(r"2026\s*[-/]\s*2027")
def http(url,limit=6_500_000):
 try:
  response=requests.get(url,timeout=15,headers={"User-Agent":UA},allow_redirects=True)
  b=response.content[:limit]
  return response.status_code,response.url,b,response.headers.get("Content-Type","")
 except Exception as e:return 0,url,b"",type(e).__name__+": "+str(e)[:130]
def relevant_date(s):
 try:
  d,m,y=[int(x) for x in re.split(r"[/.-]",s)]
  date=datetime.date(y,m,d)
  return datetime.date(2025,11,1)<=date<=datetime.date(2026,2,28)
 except Exception:return False
def task(item):
 place,slug,kind,url=item
 code,final,blob,ctype=http(url)
 rec={"territori":place,"tipus_pagina":kind,"url_pagina":url,"status":code,"final_url":final,
  "html_bytes":len(blob),"error":ctype if code==0 else "","links":[]}
 if code!=200 or not blob or b"<html" not in blob[:2000].lower():return rec
 soup=BeautifulSoup(blob,"html.parser")
 text=soup.get_text(" ",strip=True)
 up=re.search(r"Data d[’']actualitzaci[oó]\s*:?\s*([^\n]{0,30})",text,re.I)
 rec["data_actualitzacio"]=up.group(1)[:24] if up else ""
 items=[]
 for a in soup.find_all("a",href=True):
  href=urljoin(final,a["href"])
  label=a.get_text(" ",strip=True) or a.get("title","") or ""
  if not href.startswith(("https://educacio.gencat.cat/","https://www.edubcn.cat/","https://documents.espai.educacio.gencat.cat/")):continue
  if any(k in href.lower() for k in [".pdf","dificil-cobertura","pfi","convocatories"]) or any(k in label.lower() for k in ["vacant","substituci","adjudic","resultat","pfi","dificil cobertura","difícil cobertura"]):
   if any(k in label.lower() for k in ["model de sol","formulari","imprès"]):continue
   items.append({"text":label[:115],"url":href})
 urls=set();rec["links"]=[]
 for a in items:
  if a["url"] not in urls:rec["links"].append(a);urls.add(a["url"])
 return rec

def pdf_task(row):
 place,typ,label,url=row
 code,final,blob,ctype=http(url,limit=10_000_000)
 rec={"territori":place,"tipus":typ,"text_enllac":label,"url":url,"http":code,
   "bytes":len(blob),"error":ctype if code==0 else "","binari_pdf":blob.startswith(b"%PDF"),
   "pdf_sha256":hashlib.sha256(blob).hexdigest() if blob.startswith(b"%PDF") else "",
   "pagines":0,"indicis_codis":[],"indicis_dates_periode":[],"any_2526":False,"any_2627":False}
 if not blob.startswith(b"%PDF"):return rec
 try:
  doc=fitz.open(stream=blob,filetype="pdf")
  rec["pagines"]=len(doc)
  # Only counts/keywords. Do not leak applicant names from results PDFs.
  texts=[doc[i].get_text("text",sort=True) for i in range(min(len(doc),100))]
  combined="\n".join(texts)
  rec["any_2526"]=bool(RE_COURSE_OLD.search(combined))
  rec["any_2627"]=bool(RE_COURSE_NEW.search(combined))
  rec["indicis_codis"]=sorted(set(x.upper() for x in CODES_RE.findall(combined)))
  rec["indicis_dates_periode"]=sorted({x for x in DATE_RE.findall(combined) if relevant_date(x)})[:18]
  # Cannot infer offer date from dates in a different row or course year.
  rec["candidat_revisar"]=bool(rec["indicis_codis"] and rec["indicis_dates_periode"])
  doc.close()
 except Exception as e:rec["error"]=str(e)[:140]
 return rec

def test():
 assert relevant_date("27/2/2026") and relevant_date("21/11/2025")
 assert not relevant_date("01/09/2025") and not relevant_date("10/10/2026")
 assert sorted(set(CODES_RE.findall("627 F57 507 F87 15071")))==["507","627","F57","F87"]
 assert len(TERRITORIES)+len(EXTRA)==12
 print("PASS territorial count, dates and specialty parsing",flush=True)

def run(outdir):
 out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
 todo=[]
 for place,slug in TERRITORIES:
  base=ROOT+"/"+slug+URL_SUFFIX
  todo.extend([(place,slug,"secundaria",base+"/secundaria/"),(place,slug,"arrel_dc",base+"/")])
 for place,slug,url in EXTRA:todo.append((place,slug,"EDUBCN",url))
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
  pages=list(pool.map(task,todo))
 # Dynamically follow PFI subpages linked from the territorial source (avoid guesses).
 pfi=[]
 slugs=dict(TERRITORIES)
 for p in pages:
  if p["tipus_pagina"] not in ("arrel_dc",):continue
  for l in p.get("links",[]):
   if any(k in (l["text"]+" "+l["url"]).lower() for k in ["pfi","ptt","ife"]):
    u=l["url"]
    if any(u.lower().endswith(x) for x in [".pdf",".docx"]):continue
    if u not in [x[3] for x in pfi]:pfi.append((p["territori"],slugs.get(p["territori"],""),"pfi_discover",u))
 pfi=pfi[:30]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:pages+=list(pool.map(task,pfi))
 candidates={}
 for p in pages:
  for l in p.get("links",[]):
   u=l["url"]
   if (".pdf" in u.lower()) and u not in candidates:
    candidates[u]=(p["territori"],p["tipus_pagina"],l["text"],u)
 # Cap to 7 PDFs per jurisdiction for a low-impact probe. Split into target territory groups.
 pgroup={}
 for x in candidates.values():pgroup.setdefault(x[0],[]).append(x)
 jobs=[x for group in pgroup.values() for x in group[:7]]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:documents=list(pool.map(pdf_task,jobs))
 def wr(name,cols,records):
  with (out/name).open("w",newline="",encoding="utf-8") as f:
   w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore");w.writeheader();w.writerows(records)
 wr("SSTT_PAGINES.csv",["territori","tipus_pagina","url_pagina","status","final_url","html_bytes","data_actualitzacio","error"],pages)
 wr("SSTT_PDFS.csv",["territori","tipus","text_enllac","url","http","bytes","binari_pdf","pagines","any_2526","any_2627","indicis_codis","indicis_dates_periode","candidat_revisar","pdf_sha256","error"],[
 {**p,"indicis_codis":"|".join(p.get("indicis_codis",[])),"indicis_dates_periode":"|".join(p.get("indicis_dates_periode",[]))} for p in documents])
 links=[{"territori":p["territori"],"origen":p["tipus_pagina"],"text":x["text"],"url":x["url"]} for p in pages for x in p.get("links",[])]
 wr("SSTT_ENLLACOS.csv",["territori","origen","text","url"],links)
 summary=[]
 for area in [x[0] for x in TERRITORIES]+[EXTRA[0][0]]:
  pg=[x for x in pages if x["territori"]==area];pdfs=[x for x in documents if x["territori"]==area]
  summary.append({"territori":area,"pagines_consultades":len(pg),
    "pagines_http_200":sum(x["status"]==200 for x in pg),
    "pdf_enllacos_trobats":len([x for x in links if x["territori"]==area and ".pdf" in x["url"].lower()]),
    "pdf_consultats":len(pdfs),"pdf_accessibles":sum(x["binari_pdf"] for x in pdfs),
    "pdf_indicis_2526":sum(x["any_2526"] for x in pdfs),
    "pdf_indicis_507_627_F57_F87_amb_dates":sum(x.get("candidat_revisar",False) for x in pdfs),
    "exhaustiu":"NO"})
 wr("SSTT_MATRIU_PASADA.csv",list(summary[0]),summary)
 audit={"as_of":datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "scope":"2025-11-01..2026-02-28; public DC offers 507 627 F57 F87",
  "territorial_areas":12,"pages_consulted":len(pages),
  "pages_http_200":sum(x["status"]==200 for x in pages),
  "pdf_links_discovered":len(candidates),"pdf_requested":len(documents),
  "pdf_accessible":sum(x["binari_pdf"] for x in documents),
  "pdf_potential_old_relevance":sum(x.get("candidat_revisar",False) for x in documents),
  "area_results":summary,
  "old_publications_certified":0,"new_unique_ids_certified":0,
  "warnings":["This is a public-source inventory, not a historic census.",
  "Most live PDF documents may have changed to course 2026-2027.",
  "Co-occurrence of code and target-period date in same PDF does not prove same job posting.",
  "A missing current offer does not imply historical zero.",
  "Only vacancy metadata/keyword counts were saved; applicant identities suppressed.",
  "PFI sources are included only when linked/discoverable; not exhaustive."],
  "verdict":"PASS 12-area live source coverage / FAIL historical completeness"}
 (out/"AUDITORIA_PASADA_TERRITORIAL.json").write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({k:audit[k] for k in ["territorial_areas","pages_consulted","pages_http_200","pdf_links_discovered","pdf_requested","pdf_accessible","pdf_potential_old_relevance"]},ensure_ascii=False))
 return 0

if __name__=="__main__":
 parser=argparse.ArgumentParser();parser.add_argument("--test",action="store_true");parser.add_argument("--output",default="exports_territorial");args=parser.parse_args()
 if args.test:test()
 else:raise SystemExit(run(args.output))
