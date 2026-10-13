#!/usr/bin/env python3
"""V71: archive JAN 2026 EDUBCN HTML JS asset references and API patterns.
No personal data and no raw JS/HTML body exported. Only public asset paths,
response digest and safe URL path patterns. Historic HTML may call a current
API if replayed without a capture; prevent false historic data claims.
"""
import argparse,datetime,hashlib,json,re,time
from pathlib import Path
from urllib.parse import urljoin,urlsplit
import requests
from bs4 import BeautifulSoup
BASE="https://www.edubcn.cat/ca/professorat_i_pas/seleccio_rrhh/dificil_cobertura"
ARCH="https://wayback.padicat.cat/20260129224629id_/"+BASE
UA={"User-Agent":"Mozilla/5.0 (public archival educational API documentation study, bounded)"}
SAFE=re.compile(r"(/pdc_rest/[a-zA-Z0-9/_-]+|/rcs_gene/[a-zA-Z0-9/_-]+|/js/[a-zA-Z0-9._/-]+)",re.I)
def get(url,timeout=25,limit=850000):
    o={"requested_url":url,"http":None,"content_type":None,"bytes":0,
       "sha256":None,"error":None}
    b=b""
    try:
        r=requests.get(url,headers=UA,timeout=(10,timeout),stream=True)
        o["http"]=r.status_code;o["content_type"]=r.headers.get("content-type","")
        if r.status_code==200:
            ba=bytearray()
            for chunk in r.iter_content(16384):
                ba+=chunk
                if len(ba)>limit:
                    o["error"]="body_limit";break
            b=bytes(ba);o["bytes"]=len(b)
            if not o["error"]:o["sha256"]=hashlib.sha256(b).hexdigest()
        r.close()
    except Exception as e:o["error"]=type(e).__name__+": "+str(e)[:125]
    return o,b
def main(target):
    head,html=get(ARCH)
    script_urls=[];asset_links=[];source_patterns=[]
    if head["http"]==200 and html and html.lstrip().startswith(b"<"):
        soup=BeautifulSoup(html,"html.parser")
        script_urls=sorted(set(urljoin(BASE,x.get("src","")) for x in soup.find_all("script",src=True)))
        styles=sorted(set(urljoin(BASE,x.get("href","")) for x in soup.find_all("link",href=True)
            if x.get("rel") and "stylesheet" in x.get("rel")))
        asset_links=styles
        source_patterns=sorted(set(SAFE.findall(html.decode("utf-8",errors="replace"))))[:100]
    assets=[]
    for url in script_urls[:24]:
        host=urlsplit(url).hostname or ""
        if not host.endswith("edubcn.cat"):
            assets.append({"url":url,"skipped":"third_party"});continue
        stat,body=get(url,limit=1100000)
        matches=sorted(set(SAFE.findall(body.decode("utf-8",errors="replace"))))[:100] if body else []
        assets.append({"url":url,"stats":stat,"url_path_patterns":matches})
        print("JS",urlsplit(url).path,stat["http"],"url_refs",len(matches),flush=True)
        time.sleep(.5)
    out={"utc_checked":datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "historic_html_capture_at":"2026-01-29T22:46:29Z",
         "historic_html_url":ARCH,"html":head,
         "html_embedded_api_paths":source_patterns,
         "official_js_script_count":len(script_urls),
         "scripts":assets,"stylesheet_urls":asset_links,
         "capture_api_known":"https://wayback.padicat.cat/20260129224630id_/https://www.edubcn.cat/pdc_rest/convocatories/ca",
         "source_note":"Script URLs requested on current live server are not necessarily versioned; any content from live JS is not 2026-01-29 evidence.",
         "warnings":["No script bodies, HTML text, names, contact fields or candidate information stored.",
             "A URL path in JS does not establish that the endpoint preserved previous vacancy records.",
             "Original HTML capture proof does not automatically prove dates of older individual offers."]}
    p=Path(target);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"http":head["http"],"script_count":len(script_urls),
                       "html_url_patterns":len(source_patterns),"js_checked":len(assets)}),flush=True)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",required=True)
    main(p.parse_args().output)
