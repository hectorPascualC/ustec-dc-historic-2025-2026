#!/usr/bin/env python3
"""PADICAT public archive interface audit, metadata only.

Look for historic copies of official PDF URLs. No personal records downloaded or published.
"""
import argparse,datetime,json,re,urllib.parse
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT="https://padicat.cat/"
TARGETS=[
 "https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/barcelones/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/Barcelones-SEC-dificil-cobertura-oferta-vacants_07112025.pdf",
 "https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/valles-occidental/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/VOC-SEC-dificil-cobertura-oferta-vacants.pdf"]
def safe_url(u):
 p=urllib.parse.urlsplit(u)
 # Keep only public domain and path; no page bodies or cookies.
 return {"host":p.netloc,"path":p.path[:240],
    "has_capture_timestamp":bool(re.search(r"/(?:19|20)\d{12}(?:id_)?/",p.path)),
    "is_pdf":".pdf" in p.path.lower()}
def run(outpath):
 result={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "portal":ROOT,"searches":[],"request_paths":[]}
 with sync_playwright() as w:
  browser=w.chromium.launch(headless=True)
  context=browser.new_context(viewport={"width":1366,"height":900},accept_downloads=False)
  page=context.new_page()
  def track(req):
   p=urllib.parse.urlsplit(req.url)
   if len(result["request_paths"])<100 and (p.netloc.endswith("padicat.cat") or "wayback" in p.netloc):
    result["request_paths"].append({"host":p.netloc,"path":p.path[:140],"method":req.method})
  page.on("request",track)
  try:
   r=page.goto(ROOT,wait_until="domcontentloaded",timeout=60000)
   result["page_http"]=r.status if r else None
   page.wait_for_timeout(3000)
   result["input_controls"]=page.evaluate("""() => [...document.querySelectorAll('input')].slice(0,35).map(e=>({type:e.type,id:e.id,name:e.name,placeholder:e.placeholder,outer:e.outerHTML.slice(0,450)}))""")
   result["forms"]=page.evaluate("""() => [...document.querySelectorAll('form')].slice(0,12).map(e=>({action:e.getAttribute('action'),method:e.getAttribute('method'),html:e.outerHTML.slice(0,1200)}))""")
   result["buttons"]=page.evaluate("""() => [...document.querySelectorAll('button')].slice(0,35).map(e=>({name:(e.innerText||e.title||e.getAttribute('aria-label')||'').slice(0,65),type:e.type}))""")
   result["frames"]=page.evaluate("""() => [...document.querySelectorAll('iframe')].slice(0,10).map(e=>({src:e.src.split('?')[0]}))""")
   # One known original official PDF URL, plus a fallback domain query.
   for val in [TARGETS[0],"educacio.gencat.cat"]:
    record={"term_type":"official_pdf_exact" if ".pdf" in val else "official_domain"}
    try:
     # Prefer real user-facing search input; never guess private API endpoints.
     inputs=page.locator('input[type="search"], input[type="text"]')
     record["candidate_inputs"]=inputs.count()
     if not inputs.count():record["error"]="No public text input";result["searches"].append(record);continue
     field=inputs.first
     field.fill(val,timeout=5500)
     field.press("Enter",timeout=5500)
     page.wait_for_timeout(3000)
     record["result_url"]=safe_url(page.url)
     record["visible_capture_links"]=page.evaluate("""() => [...document.querySelectorAll('a[href]')].filter(x=>/(wayback|\/web\/\d{8}|capture|captura)/i.test(x.href)).slice(0,20).map(x=>{let u=new URL(x.href);return {host:u.host,path:u.pathname.slice(0,220)}})""")
     record["visible_pdf_links"]=page.evaluate("""() => [...document.querySelectorAll('a[href]')].filter(x=>/\.pdf(?:[?#]|$)/i.test(x.href)).slice(0,15).map(x=>{let u=new URL(x.href);return {host:u.host,path:u.pathname.slice(0,220)}})""")
     record["result_link_count"]=page.locator("a[href]").count()
    except Exception as e:record["error"]=type(e).__name__+": "+str(e)[:180]
    result["searches"].append(record)
    if page.url!=ROOT:
     try:page.goto(ROOT,wait_until="domcontentloaded",timeout=20000);page.wait_for_timeout(1000)
     except Exception:pass
  except Exception as e:result["error"]=type(e).__name__+": "+str(e)[:180]
  finally:browser.close()
 p=Path(outpath);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({"page_http":result.get("page_http"),"forms":len(result.get("forms",[])),
                    "searches":result["searches"],"error":result.get("error")},ensure_ascii=False),flush=True)
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--output",required=True);args=ap.parse_args()
 run(args.output)
