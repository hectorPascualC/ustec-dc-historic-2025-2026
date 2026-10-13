#!/usr/bin/env python3
"""V70: PADICAT historical HTML captures of 11 SSTT and EDUBCN listing pages.

Use real official listing URLs. Public evidence only: capture metadata, dates,
generic document links. No applicant names/text. The CDX timestamp is not the
actual offer publication date. Low-volume bounded official archive queries.
"""
import argparse, datetime, json, re, time
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import requests
from bs4 import BeautifulSoup

BASE="https://educacio.gencat.cat/ca/departament/serveis-territorials/"
TAIL="/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/"
AREAS={
 "Alt Pirineu i Aran":"alt-pirineu-aran","Baix Llobregat":"baix-llobregat",
 "Barcelonès":"barcelones","Catalunya Central":"catalunya-central",
 "Girona":"girona","Lleida":"lleida",
 "Maresme–Vallès Oriental":"maresme-valles-oriental","Penedès":"penedes",
 "Tarragona":"tarragona","Terres de l'Ebre":"terres-ebre",
 "Vallès Occidental":"valles-occidental"}
EXTRA=[("EDUBCN","https://www.edubcn.cat/ca/professorat_i_pas/seleccio_rrhh/dificil_cobertura"),
 ("EDUBCN API (control known archived)","https://www.edubcn.cat/pdc_rest/convocatories/ca")]
CDX="https://wayback.padicat.cat/cdx"
HEADERS={"User-Agent":"Mozilla/5.0 (public archive historical education-research, bounded)"}
def records(text):
    output=[]
    for line in text.splitlines():
        line=line.strip()
        if not line: continue
        if not line.startswith("{") and " {" in line:
            line="{"+line.split(" {",1)[1]
        try:x=json.loads(line)
        except (ValueError,TypeError):continue
        if not isinstance(x,dict):continue
        stamp=str(x.get("timestamp") or "")
        if not re.fullmatch(r"\d{14}",stamp):continue
        output.append({k:x.get(k) for k in ("url","timestamp","status","mime","digest","length")})
    return output
def archive_index(url):
    result={"http":None,"captures":[],"response_bytes":None,"response_content_type":None,"error":None}
    try:
        r=requests.get(CDX,params={"url":url,"matchType":"exact","output":"json","limit":"120","from":"20251101","to":"20261013"},
          headers=HEADERS,timeout=(10,27))
        result["http"]=r.status_code
        result["response_bytes"]=len(r.content)
        result["response_content_type"]=r.headers.get("content-type","")
        if r.status_code==200:result["captures"]=records(r.text)
        else:result["error"]="HTTP_"+str(r.status_code)
    except Exception as e:result["error"]=type(e).__name__+": "+str(e)[:100]
    return result
def replay(url,cap):
    out={"capture":cap["timestamp"],"http":None,"html_read":False,
      "contains_dc":False,"official_pdf_links":[],"error":None}
    try:
        r=requests.get("https://wayback.padicat.cat/"+str(cap["timestamp"])+"id_/"+url,
          headers=HEADERS,timeout=(10,26))
        out["http"]=r.status_code
        if r.status_code!=200 or "html" not in r.headers.get("content-type","").lower():return out
        out["html_read"]=True
        soup=BeautifulSoup(r.text,"html.parser")
        out["contains_dc"]=bool(re.search("difícil cobertura|dif[ií]cil provisió|ofertes de vacants",
           soup.get_text(" ",strip=True),re.I))
        refs=[]
        for a in soup.select("a[href]"):
            href=urljoin(url,a.get("href",""))
            p=urlsplit(href)
            if (p.hostname and p.hostname.endswith(("gencat.cat","edubcn.cat"))
                and p.path.lower().endswith(".pdf")
                and re.search(r"dificil|cobertura|vacants|DC[-_]|GENSEC|GESEC|PFI|resultat",p.path,re.I)
                and not re.search(r"(?i)(curriculum|sol.licitud|dni_|nom_cognom|CV_)",p.path)):
                refs.append(p.scheme+"://"+p.netloc+p.path)
        out["official_pdf_links"]=sorted(set(refs))[:150]
    except Exception as e:out["error"]=type(e).__name__+": "+str(e)[:110]
    return out
def main(output):
    sources=[(t,BASE+slug+TAIL) for t,slug in AREAS.items()]+EXTRA
    checks=[]
    for name,url in sources:
        index=archive_index(url)
        replays=[]
        for cap in index["captures"][:4]:
            if str(cap.get("status"))=="200" and "html" in str(cap.get("mime") or "").lower():
                replays.append(replay(url,cap))
        checks.append({"area":name,"original_listing_url":url,"index":index,"archived_pages":replays})
        print(name,"index",index["http"],"captures",len(index["captures"]),"replays",len(replays),flush=True)
        time.sleep(.7)
    links=sorted(set(link for x in checks for a in x["archived_pages"] for link in a["official_pdf_links"]))
    data={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "scope":"11 official territorial secondary-level HTML listings + EDUBCN listing and API control",
      "capture_time_range":"2025-11-01 to 2026-10-13",
      "urls_checked":len(checks),
      "http_200":sum(x["index"]["http"]==200 for x in checks),
      "captured_records":sum(len(x["index"]["captures"]) for x in checks),
      "replayed_html":sum(sum(a["html_read"] for a in x["archived_pages"]) for x in checks),
      "archived_generic_pdf_urls":links,
      "checks":checks,
      "warnings":["Archive time is not original publishing date.",
        "A PDF hyperlink surviving in HTML is not a proof of historic PDF bytes.",
        "Empty exact URL does not mean no archival snapshots of other URL variants.",
        "No applicant names or personally identifying application information stored."]}
    p=Path(output);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:data[k] for k in ("urls_checked","http_200","captured_records","replayed_html")}))
if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("--output",required=True);main(a.parse_args().output)
