#!/usr/bin/env python3
"""Non-personal metadata audit of EDUBCN public difficult-coverage listings.

No page HTML or person names saved; only counts, public offer codes and source URLs.
"""
import argparse, json, re, sys
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

URL='https://www.edubcn.cat/ca/professorat_i_pas/seleccio_rrhh/dificil_cobertura'
SPECIALTIES=['507','627','F57','F87']
GENSEC_PATTERN=r'GENSEC_(?:2526|2627)_[0-9]+'

SCAN = r'''() => {
 const codeRx=/GENSEC_(?:2526|2627)_\d+/ig, text=document.body?.innerText||'';
 const scripts=[...document.scripts].map(x=>x.src).filter(Boolean).filter(x=>new URL(x).host.endsWith('edubcn.cat'));
 const dynamic=[...document.querySelectorAll('iframe')].map(x=>x.src).filter(Boolean);
 const inputs=[...document.querySelectorAll('input,select')].slice(0,70).map(x=>({tag:x.tagName,id:x.id,cls:x.className?.toString().slice(0,65),placeholder:x.placeholder||'',type:x.type||'',name:x.name||''}));
 const gensec=[...new Set((text.match(codeRx)||[]))];
 const links=[...document.querySelectorAll('a[href]')].filter(x=>/GENSEC_|dificil|cobertura/i.test(x.href)).map(x=>({href:x.href,offer_codes:[...new Set(x.href.match(codeRx)||[])]})).slice(0,100);
 const counts={};for(const c of ['507','627','F57','F87'])counts[c]=(text.match(new RegExp('(^|\\W)'+c+'(\\W|$)','g'))||[]).length;
 return {title:document.title,final_url:location.href,body_text_chars:text.length,links_count:document.links.length,
         gensec_visible:gensec,gensec_2526_count:gensec.filter(x=>x.includes('_2526_')).length,
         gensec_2627_count:gensec.filter(x=>x.includes('_2627_')).length,
         inputs,embedded_urls:dynamic,first_party_scripts:scripts,offer_links:links,
         specialties_mentions:counts,has_pdf_link:links.some(x=>x.href.toLowerCase().endsWith('.pdf'))}
}'''

def audit(output):
 result={'url':URL,'run_at':datetime.now(timezone.utc).isoformat(),'mode':'read-only; no personal names'}
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  page=browser.new_page()
  responses=[]
  def trace(r):
   u=r.url
   if 'edubcn.cat' in urlsplit(u).netloc and (r.request.resource_type in ('xhr','fetch') or 'dificil' in u):
    responses.append({'url':u.split('?')[0],'status':r.status,'resource_type':r.request.resource_type})
  page.on('response',trace)
  try:
   page.goto(URL,wait_until='domcontentloaded',timeout=60000)
   page.wait_for_timeout(12000)
   before=page.evaluate(SCAN)
   result['dom_initial']=before
   # Try only preexisting public search fields; no submission/posting.
   search_inputs=page.locator('input[type="search"], input[placeholder*="Cerca"], input[placeholder*="cerca"]')
   if search_inputs.count():
    try:
     inp=search_inputs.first
     inp.fill('507')
     inp.press('Enter')
     page.wait_for_timeout(4000)
     result['dom_search_507']=page.evaluate(SCAN)
    except Exception as e: result['search_error']=str(e)[:180]
  except Exception as e:result['error']=str(e)[:400]
  result['public_http_responses']=list({(r['url'],r['status'],r['resource_type']):r for r in responses}.values())[:60]
  browser.close()
 result['historic_rows_verified']=0
 result['historic_2025_26_complete']=False
 result['note']='Only a 2025-2026 date+offer-ID source proves historic record; current 2026-27 GENSEC entries are not evidence of earlier dates.'
 Path(output).parent.mkdir(parents=True,exist_ok=True)
 Path(output).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'error':result.get('error'), 'visible_2025_26_ids':result.get('dom_initial',{}).get('gensec_2526_count'), 'historic_complete':False},ensure_ascii=False))

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();audit(args.output)