#!/usr/bin/env python3
"""Diagnòstic no invasiu dels filtres públics de la taula USTEC.
No conserva noms ni números de nomenament, ni fragments de files.
"""
import json, argparse
from pathlib import Path
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright

PAGE = "https://www.sindicat.net/eines/nomenaments/nomenaments2.php"
JS = r"""() => {
  const jq=window.jQuery; const t=jq.fn.dataTable.tables()[0];
  const api=jq(t).DataTable();
  const hs=Array.from(api.columns().header());
  const procedureIndex=hs.findIndex(x=>(x.childNodes[0]?.textContent||x.textContent).includes('Procediment'));
  const selects=Array.from(document.querySelectorAll('select')).map(e=>({
    outer:e.outerHTML.slice(0,280),
    value:e.value,
    options:Array.from(e.options).filter(x=>/(cobertura|adjudicad|nomenament|dif|tel|2025)/i.test(x.textContent)).map(o=>({value:o.value,text:o.textContent.trim().slice(0,80)}))
  }));
  const controls=Array.from(document.querySelectorAll('button,input[type=button],input[type=checkbox],label,a'))
    .filter(e=>/no\s+adjudicad|dif[ií]cil\s+cobertura/i.test(e.textContent||e.value||''))
    .slice(0,20).map(e=>({tag:e.tagName,type:e.type||'',id:e.id||'',outer:e.outerHTML.slice(0,700)}));
  const scripts=Array.from(document.scripts).filter(s=>!s.src).flatMap(s=>{
    const txt=s.textContent||'';let hits=[];
    for(const term of ['adjudicades','no_adjud','noadjud','difícil cobertura','Difícil cobertura','procediment']){
      const ix=txt.toLowerCase().indexOf(term.toLowerCase());
      if(ix>=0) hits.push({term,around:txt.slice(Math.max(0,ix-280),ix+400).slice(0,700)});
    }
    return hits;
  }).slice(0,16);
  return {time:new Date().toISOString(),tableIndex:procedureIndex,procedureHeader:hs[procedureIndex]?.outerHTML.slice(0,1400),selects,controls,scripts,unassignedMatches:(document.body.innerText.match(/Veure les NO adjudicades/g)||[]).length,tableInfo:api.page.info()};
}"""
if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    result={"checked_at":datetime.now(timezone.utc).isoformat(),"url":PAGE}
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            page=browser.new_page()
            page.goto(PAGE,wait_until="domcontentloaded",timeout=60000)
            page.wait_for_function("!!(window.jQuery && window.jQuery.fn.dataTable && window.jQuery.fn.dataTable.tables().length)",timeout=55000)
            page.wait_for_timeout(1200)
            result["dom"]=page.evaluate(JS)
            browser.close()
    except Exception as e:
        result["error"]=str(e)
    path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"error":result.get("error"),"controls":len(result.get("dom",{}).get("controls",[])),"procedureIndex":result.get("dom",{}).get("tableIndex")},ensure_ascii=False))
