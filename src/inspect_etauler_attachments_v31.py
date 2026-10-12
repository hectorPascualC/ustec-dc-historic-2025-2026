#!/usr/bin/env python3
"""Extended historical keyword sweep of Generalitat e-TAULER; no private data.

No edict text, applicant names, ids, payloads or cookies published.
"""
import argparse, json, datetime, urllib.parse, hashlib, re
import fitz
from pathlib import Path
from playwright.sync_api import sync_playwright
URL="https://tauler.seu-e.cat/inici?idEns=1"
JS="""() => ({
 title:document.title,
 url_path:location.pathname,
 inputs:[...document.querySelectorAll('input')].map(x=>({tag:x.tagName,type:x.type,placeholder:x.placeholder,name:x.name,aria:x.getAttribute('aria-label'),id:x.id})).slice(0,55),
 buttons:[...document.querySelectorAll('button,[role=button]')].filter(x=>!x.closest('article')).map(x=>({text:(x.innerText||x.getAttribute('aria-label')||'').trim().slice(0,70),aria:x.getAttribute('aria-label'),type:x.type})).slice(0,60),
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
    if u.path=="/api/edictes" and q.method=="POST" and len(data.get("payloads",[]))<22:
     try:
      body=q.post_data_json
      def safe(x,depth=0):
       if depth>3:return "<deep>"
       if isinstance(x,dict):return {str(k)[:50]:safe(v,depth+1) for k,v in list(x.items())[:20]}
       if isinstance(x,list):return {"list_length":len(x),"first":safe(x[0],depth+1) if x else None}
       if isinstance(x,(int,float,bool)) or x is None:return x
       return str(x)[:45] if str(x) in ("0","1","2","3","ACTIU","HISTORIC","HITORIC","true","false","507","627","F57","F87","difícil cobertura","dificil cobertura","GENSEC_2526","2025/SEC","nomenaments interí") else "<string_redacted>"
      data.setdefault("payloads",[]).append(safe(body))
     except Exception as ex:data.setdefault("payloads",[]).append({"error_type":type(ex).__name__})
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
    data["historic_dom"]=page.evaluate("""() => [...document.querySelectorAll('body *')].filter(x=>x.childElementCount===0 && (x.textContent||'').trim()==='Històric').slice(0,4).map(x=>({self:x.outerHTML.slice(0,600),parent:x.parentElement?.outerHTML.slice(0,1250),grandparent:x.parentElement?.parentElement?.outerHTML.slice(0,1650),visible:!!x.getClientRects().length}))""")
    try:
     if historic.count():
      historic.first.click(timeout=4500)
      page.wait_for_timeout(1200)
      data["historic_mode_selected"]=True
     else:data["historic_mode_selected"]=False
    except Exception as ex:data["historic_mode_error"]=str(ex)[:130]
   # Explicitly select the historic radio state=2 rather than clicking its text span.
   historic_radio=page.locator('input[name="state"][value="2"]')
   if not historic_radio.count():
    selector=page.locator('button[aria-label^="Estat:"]')
    if selector.count():selector.first.click()
   if historic_radio.count():
    try:
     historic_radio.check(force=True,timeout=4500)
     data["historic_radio_checked"]=True
    except Exception as ex:data["historic_radio_error"]=str(ex)[:190]
   # The popover has an Apply ('Mostrar resultats') button.
   # The radio itself only changes local state until that button is clicked.
   apply=page.locator('[role="dialog"] button[type="submit"]')
   data["apply_buttons_found"]=apply.count()
   if apply.count():
    try:
     apply.last.click(force=True,timeout=4000)
     data["historic_applied_via_dialog"]=True
    except Exception as ex:data["historic_apply_error"]=str(ex)[:160]
   page.wait_for_timeout(900)
   data["status_after_menu"]=page.locator('button[aria-label^="Estat:"]').first.get_attribute("aria-label") if page.locator('button[aria-label^="Estat:"]').count() else None
   data["radio_current"]=page.evaluate("""() => [...document.querySelectorAll('input[name=state]')].map(x=>({value:x.value,checked:x.checked}))""")
   all_button=page.get_by_role("button",name="Veure'ls tots")
   data["show_all_button_count"]=all_button.count()
   if all_button.count():
    try:
     all_button.first.click(force=True,timeout=4500)
     page.wait_for_timeout(1100)
     data["clicked_veurels_tots"]=True
    except Exception as ex:data["show_all_error"]=str(ex)[:180]
   data["search_area_dom"]=page.locator("#search-input").evaluate("(x)=>x.parentElement?.parentElement?.outerHTML.slice(0,1800)")
   page.keyboard.press("Escape")
   queries=["personal docent"]
   data["searches"]=[]
   for q in queries:
    try:
     page.locator("#search-input").fill(q)
     if q==queries[0]:
      data["search_button_disabled"]=page.locator('button[aria-label="Cercar"]').evaluate("(e)=>e.disabled")
      data["status_label_after_historic"]=page.evaluate("""() => [...document.querySelectorAll("button")].map(x=>x.getAttribute("aria-label")||"").find(x=>x.startsWith("Estat:"))||null""")
     page.locator('button[aria-label="Cercar"]').click(force=True,timeout=3000)
     page.wait_for_timeout(1700)
     d=page.evaluate("""() => {
       const text=document.body.innerText||'';
       return {counts:[...text.matchAll(/(?:\\d[\\d.,]*\\s+anuncis)/gi)].map(x=>x[0]).slice(0,5),
       has2025:/2025/.test(text),has2026:/2026/.test(text),
       hits_education:(text.match(/Educació|Formació Professional/gi)||[]).length,
       hits_difficult:(text.match(/dif[ií]cil cobertura/gi)||[]).length,
       page_url_path:location.pathname,
       text_chars:text.length,
       article_count:document.querySelectorAll("article").length,
       article_metadata:[...document.querySelectorAll("article")].slice(0,8).map(a=>{
        const t=a.innerText||"";
        return {dates:[...t.matchAll(/\\b[0-3]?\\d[\\/.-][01]?\\d[\\/.-]20[0-9]{2}\\b/g)].map(z=>z[0]).slice(0,4),
           has_507:/\\b507\\b/.test(t),has_627:/\\b627\\b/.test(t),
           has_F57:/\\bF57\\b/.test(t),has_F87:/\\bF87\\b/.test(t),
           has_DC:/dif[ií]cil\\s+cobertura/i.test(t)}
       })
       }
     }""")
     data["searches"].append({"query":q,**d})
    except Exception as ex:data["searches"].append({"query":q,"error":str(ex)[:130]})
   # Examine ONLY first three public notices dated in the 2025-11 to 2026-02
   # window from prior V28. Keep boolean classifications and dates, no content.
   data["candidate_details"]=[]
   page.locator("#search-input").fill("personal docent")
   page.locator('button[aria-label="Cercar"]').click(force=True,timeout=4000)
   page.wait_for_timeout(1500)
   for idx in range(3):
    one={"list_index":idx}
    try:
     articles=page.locator("article")
     if articles.count()<=idx:one["error"]="No corresponding public notice";data["candidate_details"].append(one);continue
     card=articles.nth(idx)
     one["card_dates"]=card.evaluate("""x=>[...x.innerText.matchAll(/\\b[0-3]?\\d[\\/.-][01]?\\d[\\/.-]20\\d{2}\\b/g)].map(v=>v[0]).slice(0,4)""")
     btn=card.locator('button[role="link"]')
     if not btn.count():one["error"]="No notice detail button";data["candidate_details"].append(one);continue
     btn.first.click(force=True,timeout=3000)
     page.wait_for_timeout(1000)
     u=urllib.parse.urlsplit(page.url)
     params=urllib.parse.parse_qs(u.query)
     one["public_notice_id"]=params.get("idEdicte",[None])[0]
     one["detail_path"]=u.path
     one["detail_flags"]=page.evaluate("""() => {
       const s=document.body.innerText||"";
       const links=[...document.querySelectorAll('a[href]')];
       return {has_dc:/dif[ií]cil\\s+cobertura/i.test(s),
         has_507:/\\b507\\b/.test(s),has_627:/\\b627\\b/.test(s),
         has_F57:/\\bF57\\b/.test(s),has_F87:/\\bF87\\b/.test(s),
         has_vacant:/\\bvacan(?:t|ts)\\b/i.test(s),
         has_docent:/docent|professorat|educaci[oó]/i.test(s),
         has_concurs:/concurs|oposici[oó]|proc[eé]s selectiu/i.test(s),
         attachment_count:links.filter(a=>/pdf|document|annex/i.test(a.href+" "+a.innerText)).length,
         body_chars:s.length}
     }""")
     # Inspect public attachments in memory; persist ONLY keyword flags,
     # cryptographic hash and size, never source content or personal records.
     one["attachments_checked"]=[]
     links=page.locator("a[href]").evaluate_all("""els=>els.filter(x=>/\\b(pdf|document|annex|adjunt)\\b/i.test((x.innerText||'')+' '+x.href)).slice(0,8).map(x=>({href:x.href,visible:!!x.getClientRects().length}))""")
     for ref in links:
      url=ref.get("href","")
      u2=urllib.parse.urlsplit(url)
      if u2.scheme not in ("http","https") or not (u2.hostname or "").endswith(("seu-e.cat","aoc.cat","gencat.cat")):continue
      evidence={"public_url_host":u2.hostname,"public_url_path":u2.path[:150]}
      try:
       response=page.request.get(url,timeout=15000)
       evidence["http"]=response.status
       b=response.body()[:12000000]
       evidence["is_pdf"]=b[:4]==b"%PDF"
       if evidence["is_pdf"]:
        evidence["sha256"]=hashlib.sha256(b).hexdigest()
        doc=fitz.open(stream=b,filetype="pdf")
        text="\n".join(doc[k].get_text("text") for k in range(min(30,len(doc))))
        evidence["pages_checked"]=min(30,len(doc))
        evidence["has_dc"]=bool(re.search(r"dif[ií]cil\\s+cobertura",text,re.I))
        evidence["has_507"]=bool(re.search(r"\\b507\\b",text))
        evidence["has_627"]=bool(re.search(r"\\b627\\b",text))
        evidence["has_F57"]=bool(re.search(r"\\bF57\\b",text))
        evidence["has_F87"]=bool(re.search(r"\\bF87\\b",text))
        doc.close()
      except Exception as ex:evidence["error_type"]=type(ex).__name__
      one["attachments_checked"].append(evidence)
     page.go_back(wait_until="domcontentloaded",timeout=14000)
     page.wait_for_timeout(850)
     # SPA should restore historic filter; otherwise reselect it explicitly.
     state=page.locator('button[aria-label^="Estat:"]')
     one["state_after_back"]=state.first.get_attribute("aria-label") if state.count() else None
     if state.count() and "Històric" not in one["state_after_back"]:
      state.first.click()
      page.locator('input[name="state"][value="2"]').check(force=True)
      page.locator('[role="dialog"] button[type="submit"]').last.click(force=True)
     page.locator("#search-input").fill("personal docent")
     page.locator('button[aria-label="Cercar"]').click(force=True,timeout=3000)
     page.wait_for_timeout(1250)
    except Exception as ex:one["error"]=type(ex).__name__+": "+str(ex)[:110]
    data["candidate_details"].append(one)
   browser.close()
 except Exception as ex:data["error"]=str(ex)[:250]
 o=Path(path);o.parent.mkdir(parents=True,exist_ok=True)
 o.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({"http":data.get("http"),"error":data.get("error"),"inputs":len(data.get("ui",{}).get("inputs",[])),"buttons":len(data.get("ui",{}).get("buttons",[])),"requests":len(data["network"])},ensure_ascii=False))
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--output",required=True)
 run(ap.parse_args().output)
