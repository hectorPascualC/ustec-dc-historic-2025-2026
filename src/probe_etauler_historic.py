#!/usr/bin/env python3
"""Inspect public Generalitat e-TAULER historic search UI, metadata only.

No edict text, applicant names, ids, payloads or cookies published.
"""
import argparse, json, datetime, urllib.parse
from pathlib import Path
from playwright.sync_api import sync_playwright
URL="https://tauler.seu-e.cat/inici?idEns=1"
JS="""() => ({
 title:document.title,
 url_path:location.pathname,
 inputs:[...document.querySelectorAll('input')].map(x=>({tag:x.tagName,type:x.type,placeholder:x.placeholder,name:x.name,aria:x.getAttribute('aria-label'),id:x.id})).slice(0,55),
 buttons:[...document.querySelectorAll('button,[role=button]')].map(x=>({text:(x.innerText||x.getAttribute('aria-label')||'').trim().slice(0,70),aria:x.getAttribute('aria-label'),type:x.type})).slice(0,60),
 selects:[...document.querySelectorAll('select')].map(x=>({id:x.id,options:[...x.options].map(y=>({label:y.textContent.trim().slice(0,65),value:y.value})).slice(0,40)})).slice(0,20),
 scripts:[...document.scripts].map(x=>x.getAttribute('src')).filter(Boolean).map(x=>new URL(x,location.href).pathname).slice(0,20),
 filters:[...document.querySelectorAll('a')].map(x=>({label:(x.innerText||'').trim().slice(0,60),path:(()=>{try{return new URL(x.href,location.href).pathname}catch(e){return ''}})()})).filter(x=>/cerca|filtr|hist|anunc|educaci/i.test(x.label)).slice(0,40),
 hasOld:[...document.querySelectorAll('body *')].some(x=>x.children.length===0&&/Històric|Histórico|Històrics/.test(x.textContent||'')),
 countMatches:(document.body.innerText.match(/\\d+ anuncis/g)||[]).slice(0,5)
})"""
def run(path):
 data={"run_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"target":URL,"network":[]}
 try:
  with sync_playwright() as p:
   browser=p.chromium.launch(headless=True)
   page=browser.new_page(viewport={"width":1365,"height":940})
   def request(q):
    u=urllib.parse.urlsplit(q.url)
    if u.hostname and (u.hostname.endswith("seu-e.cat") or u.hostname.endswith("aoc.cat")):
     if len(data["network"])<70 and ("/api/" in u.path or "/rest/" in u.path or "/search" in u.path or "/anunci" in u.path or "/edicte" in u.path):
      data["network"].append({"method":q.method,"path":u.path[:180]})  # no query/body/personal data
   page.on("request",request)
   resp=page.goto(URL,wait_until="domcontentloaded",timeout=60000)
   data["http"]=resp.status if resp else None
   page.wait_for_timeout(3500)
   data["ui"]=page.evaluate(JS)
   menu=page.locator('button[aria-label="Estat:Actius"]')
   data["status_filter_found"]=menu.count()
   if menu.count():
    menu.click()
    page.wait_for_timeout(350)
    data["menu_visible_choices"]=page.evaluate("""() => [...document.querySelectorAll('button,[role=option]')].filter(e=>e.getClientRects().length).map(e=>(e.innerText||e.getAttribute('aria-label')||'').trim()).filter(t=>/actius|històric|històrics|retirats|tots/i.test(t)&&t.length<90).slice(0,16)""")
    historic=page.get_by_text("Històric",exact=True)
    data["historic_choice_found"]=historic.count()
    try:
     if historic.count():
      historic.first.click(timeout=4500)
      page.wait_for_timeout(1200)
      data["historic_mode_selected"]=True
     else:data["historic_mode_selected"]=False
    except Exception as ex:data["historic_mode_error"]=str(ex)[:130]
   queries=["difícil cobertura","dificil cobertura","nomenaments interí","GENSEC_2526","2025/SEC","507","627","F57","F87"]
   data["searches"]=[]
   for q in queries:
    try:
     page.locator("#search-input").fill(q)
     page.locator('button[aria-label="Cercar"]').click(timeout=3500)
     page.wait_for_timeout(1100)
     d=page.evaluate("""() => {
       const text=document.body.innerText||'';
       return {counts:[...text.matchAll(/(?:\\d[\\d.,]*\\s+anuncis)/gi)].map(x=>x[0]).slice(0,5),
       has2025:/2025/.test(text),has2026:/2026/.test(text),
       hits_education:(text.match(/Educació|Formació Professional/gi)||[]).length,
       hits_difficult:(text.match(/dif[ií]cil cobertura/gi)||[]).length,
       page_url_path:location.pathname,
       text_chars:text.length
       }
     }""")
     data["searches"].append({"query":q,**d})
    except Exception as ex:data["searches"].append({"query":q,"error":str(ex)[:130]})
   browser.close()
 except Exception as ex:data["error"]=str(ex)[:250]
 o=Path(path);o.parent.mkdir(parents=True,exist_ok=True)
 o.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({"http":data.get("http"),"error":data.get("error"),"inputs":len(data.get("ui",{}).get("inputs",[])),"buttons":len(data.get("ui",{}).get("buttons",[])),"requests":len(data["network"])},ensure_ascii=False))
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--output",required=True)
 run(ap.parse_args().output)
