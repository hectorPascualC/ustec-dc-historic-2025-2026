#!/usr/bin/env python3
"""V66 — search real official directory prefixes in Common Crawl indices.

All input prefixes are grounded by a known live PDF from the official
education domain (V24 inventory or externally verified published SPD PDF).
Only aggregate counts and official doc URLs with generic filenames are
saved, never personal names or archive body text. Empty index cannot prove
no historical vacancies. Bounded per collection and stops on consecutive
server errors.
"""
import argparse,csv,datetime,json,re,time
from pathlib import Path
from urllib.parse import urlsplit
import requests
BASE="https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/"
TR="personal-docent/nomenaments-telematics/dificil-cobertura/"
ROOT=Path(__file__).resolve().parents[1]
COLL=["CC-MAIN-2025-47","CC-MAIN-2025-51","CC-MAIN-2026-04","CC-MAIN-2026-08","CC-MAIN-2026-12"]
GROUPS=[
 ("Alt Pirineu i Aran","secondary",BASE+"alt-pirineu-aran/"+TR+"secundaria/"),
 ("Alt Pirineu i Aran","PFI-IFE",BASE+"alt-pirineu-aran/"+TR+"oferta-moduls-pfi-ife/"),
 ("Maresme-Valles Oriental","secondary",BASE+"maresme-valles-oriental/"+TR+"secundaria/"),
 ("Tarragona","secondary",BASE+"tarragona/"+TR+"secundaria/"),
 ("Terres de l'Ebre","secondary",BASE+"terres-ebre/"+TR+"secundaria/"),
 ("Catalunya Central","SPD alternative",BASE+"catalunya-central/personal-docent/Provisio-vacants-SPD/"),
]
UA={"User-Agent":"Mozilla/5.0 (public educational archives historic census query, rate limited)"}
DOC_RE=re.compile(r"(dificil[-_]cobertura|provisio[-_]SPD|ofertes[-_]provisio|PFI|resultat).{0,130}\.pdf",re.I)
COURSE_RE=re.compile(r"(?:2025|2026|2526|25[-_]26|novemb|desemb|gener|febrer)",re.I)
def main(dest):
    jobs=[(group,kind,prefix,coll) for group,kind,prefix in GROUPS for coll in COLL]
    observations=[];consecutive_errors=0;halt=False
    for i,(group,kind,prefix,coll) in enumerate(jobs):
        observation={"territory":group,"source_type":kind,"verified_official_url_prefix":prefix,
                     "collection":coll,"http":None,"results":0,
                     "candidate_generic_pdf_urls":[],"error":None}
        try:
            r=requests.get("https://index.commoncrawl.org/"+coll+"-index",
                params={"url":prefix+"*","output":"json","pageSize":20},
                headers=UA,timeout=(10,23))
            observation["http"]=r.status_code
            if r.status_code==200:
                entries=[]
                for line in r.text.splitlines()[:30]:
                    try:row=json.loads(line)
                    except ValueError:continue
                    if isinstance(row,dict):entries.append(row)
                observation["results"]=len(entries)
                for x in entries:
                    url=x.get("url","")
                    if (url.startswith(prefix) and DOC_RE.search(urlsplit(url).path)
                        and not re.search(r"(?i)(sol.licitud|curriculum|cv_|dni|nie|persona)",url)):
                        observation["candidate_generic_pdf_urls"].append({
                            "url":url,
                            "capture_timestamp":str(x.get("timestamp",""))[:14],
                            "status":str(x.get("status","")),
                            "mime":str(x.get("mime","")),
                            "digest":str(x.get("digest","")),
                            "warc_filename":str(x.get("filename","")),
                            "warc_offset":str(x.get("offset","")),
                            "warc_length":str(x.get("length",""))})
            elif r.status_code!=404:
                observation["error"]="HTTP_"+str(r.status_code)
        except Exception as ex:
            observation["error"]=type(ex).__name__+": "+str(ex)[:125]
        observations.append(observation)
        print(f'{i+1}/{len(jobs)} {group} / {kind} / {coll}: HTTP={observation["http"]}; rows={observation["results"]}',flush=True)
        consecutive_errors=consecutive_errors+1 if observation["http"] in (429,502,503,504) else 0
        if consecutive_errors>=3:
            halt=True;break
        time.sleep(1.2)
    hits=[v for o in observations for v in o["candidate_generic_pdf_urls"]]
    output={"utc_checked":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "scope":"6 distinct verified official directory prefixes: 4 never-recovered SSTT plus CCE SPD and APA PFI",
        "source_control":"V24 SSTT_PDFS.csv and 2025 official CCE SPD PDF indexed by public search",
        "collections":COLL,"territorial_prefixes":len(GROUPS),
        "planned_queries":len(jobs),"executed_queries":len(observations),"stopped_on_three_consecutive_server_errors":halt,
        "no_capture_404_count":sum(o["http"]==404 for o in observations),
        "http_200_count":sum(o["http"]==200 for o in observations),
        "blocked_count":sum(o["http"] not in (200,404) for o in observations),
        "all_index_rows_returned":sum(o["results"] for o in observations),
        "generic_doc_candidates":len(hits),
        "verified_pdf_binaries":0,"observations":observations,
        "limitations":["Prefix search retrieves at most 20 per index and is not a complete census if paging occurs.",
            "Errors 502/503/504/429 are blockers, never counted as no snapshots.",
            "A 404 in a specified Common Crawl index is not absence of historic official offers.",
            "Any CDX candidate requires WARC byterange and real PDF bytes/hash validation, then row-level 507/627/F57/F87 check.",
            "Existing 36 IDs must be deduplicated with new evidence; do not publish staff names or sensitive fields."]}
    target=Path(dest);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:output[k] for k in ("planned_queries","executed_queries","no_capture_404_count","blocked_count","all_index_rows_returned","generic_doc_candidates")}),flush=True)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",required=True)
    main(p.parse_args().output)
