#!/usr/bin/env python3
"""Extracció auditada de la taula històrica de nomenaments USTEC.

No pressuposa endpoint PHP/JSON: fa servir la instància real de DataTables dins
Chromium i documenta les peticions XHR que es produeixen. Conserva dades de
nomenaments i només etiqueta com a DC les files que realment indiquen DC.

Requisits: pip install playwright && python -m playwright install chromium
Execució: python recuperar_ustec_dc.py --output ./resultats
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from datetime import datetime, date
from pathlib import Path
from urllib.parse import urlparse

SITE = "https://www.sindicat.net/eines/nomenaments/nomenaments2.php"
COLUMNS = ["servei_territorial", "data", "numero_adjudicat", "centre", "jornada",
           "especialitat", "data_inici", "data_fi", "procediment", "curs"]
CODES = ("507", "627", "F57", "F87")


def clean(raw):
    if raw is None:
        return ""
    if isinstance(raw, (dict, list)):
        raw = json.dumps(raw, ensure_ascii=False)
    s = str(raw)
    s = re.sub(r"<[^>]*>", " ", s)
    import html
    return " ".join(html.unescape(s).split()).strip()


def normalize(s):
    return "".join(c for c in unicodedata.normalize("NFD", clean(s)).lower()
                   if not unicodedata.combining(c))


def date_parse(s):
    x = clean(s)
    if not x:
        return None
    for pattern in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%d/%m/%y"):
        try:
            return datetime.strptime(x[:10], pattern).date()
        except ValueError:
            continue
    return None


def is_dc(s):
    x = normalize(s)
    return bool(re.search(r"\bdificil[\s_-]*cobertura\b|\b(?:procediment|nom[. ]*)?dc\b", x))


def matches_code(s, code):
    return bool(re.search(r"(?<![A-Za-z0-9])" + re.escape(code) + r"(?![A-Za-z0-9])", clean(s), flags=re.I))


def record_from_raw(headers, raw):
    if isinstance(raw, list):
        values = [clean(x) for x in raw]
    elif isinstance(raw, dict):
        values = [clean(raw.get(str(i), raw.get(headers[i], ""))) for i in range(len(headers))]
        if not any(values):
            values = [clean(x) for x in raw.values()]
    else:
        return None
    if len(values) < len(COLUMNS):
        return None
    # Si hi ha capçalera inesperada no fer un mapeig inventat.
    if len(values) > len(COLUMNS):
        values = values[:len(COLUMNS)]
    return dict(zip(COLUMNS, values))


def reduce_records(raw_items, codes, initial, final, course):
    all_rows, period_rows, dc_rows, diagnostics = [], [], [], Counter()
    seen = set()
    for item in raw_items:
        row = record_from_raw([], item) if isinstance(item, list) else item
        if not isinstance(row, dict):
            diagnostics["malformed_rows"] += 1
            continue
        if not all(key in row for key in COLUMNS):
            diagnostics["malformed_rows"] += 1
            continue
        key = hashlib.sha256(json.dumps(row, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        if key in seen:
            diagnostics["duplicated_exact_rows"] += 1
            continue
        seen.add(key)
        if not any(matches_code(row["especialitat"], c) for c in codes):
            diagnostics["different_specialty"] += 1
            continue
        if clean(row["curs"]) != course:
            diagnostics["different_course"] += 1
            continue
        all_rows.append(row)
        d = date_parse(row["data"])
        if d is None:
            diagnostics["unparseable_nomination_date"] += 1
            continue
        if initial <= d <= final:
            period_rows.append(row)
            if is_dc(row["procediment"]):
                dc_rows.append(row)
            else:
                diagnostics["non_dc_procedure"] += 1
    return all_rows, period_rows, dc_rows, diagnostics


GET_META = r"""() => {
  const jq = window.jQuery;
  if (!jq || !jq.fn || !jq.fn.dataTable) return {error:'jquery/DataTables unavailable'};
  const ts = jq.fn.dataTable.tables();
  if (!ts.length) return {error:'no initialized DataTables table'};
  const api = jq(ts[0]).DataTable();
  const labels = Array.from(api.columns().header()).map(h => (h.textContent || '').trim().replace(/\s+/g,' '));
  const settings = api.settings()[0];
  const inputs = Array.from(document.querySelectorAll('input, select')).map(x => ({tag:x.tagName,type:x.type,name:x.name,id:x.id,placeholder:x.placeholder,value:x.value,checked:x.checked}));
  return {labels,serverSide:!!settings.oFeatures.bServerSide,
          ajaxSrc:api.ajax && api.ajax.url ? api.ajax.url():null,
          info:api.page.info(),inputs,
          scripts:Array.from(document.scripts).map(s=>s.src).filter(Boolean)};
}"""

INITIAL_DRAW = r"""async ({code,course,size,timeout}) => {
  const jq = window.jQuery;
  const api = jq(jq.fn.dataTable.tables()[0]).DataTable();
  const hs = Array.from(api.columns().header()).map(h => (h.textContent || '').trim().toLowerCase());
  const ci = hs.findIndex(h => h.includes('especialitat'));
  const yi = hs.findIndex(h => h.includes('curs'));
  if(ci < 0 || yi < 0) throw new Error('Missing especialitat/curs headers: '+JSON.stringify(hs));
  return await new Promise((resolve,reject)=>{
    let done=false; let timer;
    const handler=()=>{ if(done)return;done=true;clearTimeout(timer);api.off('draw',handler);resolve(snapshot()) };
    function snapshot(){ const nodes=api.rows({page:'current'}).nodes().toArray(); const rows=nodes.map(n=>Array.from(n.children).filter(c=>c.tagName==='TD').map(c=>(c.textContent||'').replace(/\s+/g,' ').trim())); return {info:api.page.info(),rows:rows.length?rows:api.rows({page:'current'}).data().toArray()}}
    api.one('draw',handler);
    timer=setTimeout(()=>{if(done)return;done=true;api.off('draw',handler);reject(new Error('draw timed out'))},timeout);
    api.search('');
    api.columns().search('');
    api.column(ci).search(code);
    api.column(yi).search(course);
    api.page.len(size).draw();
  });
}"""

NEXT_DRAW = r"""async ({pageNum,timeout}) => {
  const jq=window.jQuery; const api=jq(jq.fn.dataTable.tables()[0]).DataTable();
  return await new Promise((resolve,reject)=>{
    let done=false; let timer;
    const handler=()=>{if(done)return;done=true;clearTimeout(timer);api.off('draw',handler);const nodes=api.rows({page:'current'}).nodes().toArray();const rows=nodes.map(n=>Array.from(n.children).filter(c=>c.tagName==='TD').map(c=>(c.textContent||'').replace(/\s+/g,' ').trim()));resolve({info:api.page.info(),rows:rows.length?rows:api.rows({page:'current'}).data().toArray()})};
    api.one('draw',handler);
    timer=setTimeout(()=>{if(done)return;done=true;api.off('draw',handler);reject(new Error('page draw timed out'))},timeout);
    api.page(pageNum).draw('page');
  });
}"""


CHECK_UNASSIGNED = r"""() => {
 const button=document.querySelector('#btn-filter');
 const label=(button?.textContent||'').trim();
 return {found:!!button,changed:false,control_type:button?.tagName||'',
         text:label,
         meaning:'The button applies search value 0 to column 2, restricting to unassigned rows; no filter returns all rows'};
}"""


def write_csv(path, rows, anonymize=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        if anonymize:
            # Les dades públiques de nomenaments inclouen possibles números personals.
            # Un artefacte de GitHub públic només ha de contenir dades anonimitzades.
            writer.writerows({**row, "numero_adjudicat": "NO ADJUDICAT" if "no adjudicat" in normalize(row.get("numero_adjudicat", "")) else "REDACTAT"} for row in rows)
        else:
            writer.writerows(rows)


def run_browser(opts):
    from playwright.sync_api import sync_playwright
    output = Path(opts.output)
    output.mkdir(parents=True, exist_ok=True)
    network = []
    raw = []
    checks = []
    diagnostics = {"url": SITE, "started": datetime.now().astimezone().isoformat(),
                   "year":opts.course, "date_range":[opts.start,opts.end],
                   "codes":list(opts.codes), "tests":checks, "network":network,
                   "complete":False, "warnings":[]}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not opts.headful,
            executable_path=opts.chromium if opts.chromium else None)
        context = browser.new_context(locale="ca-ES",viewport={"width":1440,"height":980})
        page = context.new_page()

        def request_logger(req):
            if req.resource_type in ("xhr", "fetch"):
                parsed = urlparse(req.url)
                if parsed.hostname and parsed.hostname.endswith("sindicat.net"):
                    payload = req.post_data or ""
                    network.append({"method":req.method,"url":req.url,
                                    "post_size":len(payload),"post_example":payload[:1200]})
                    if len(network)>250:
                        del network[0:100]
        page.on("request",request_logger)
        try:
            page.goto(SITE,wait_until="domcontentloaded",timeout=60000)
            page.wait_for_function("!!(window.jQuery && window.jQuery.fn.dataTable && window.jQuery.fn.dataTable.tables().length)",timeout=55000)
            page.wait_for_timeout(3500)
            meta = page.evaluate(GET_META)
            diagnostics["table"] = meta
            labels = [normalize(s) for s in meta.get("labels", [])]
            if len(labels) < 10 or not all(any(word in l for l in labels) for word in ("procediment","curs","especialitat","data")):
                raise RuntimeError("Columns don't match expected structure: "+repr(meta.get("labels")))
            if labels.index(next(l for l in labels if "especialitat" in l)) != 5 or labels.index(next(l for l in labels if "curs" in l)) != 9:
                raise RuntimeError("Column order changed. Refusing to silently mislabel rows: "+repr(meta.get("labels")))
            diagnostics["unassigned"] = page.evaluate(CHECK_UNASSIGNED)
            if not diagnostics["unassigned"]["found"]:
                diagnostics["warnings"].append("Checkbox 'Veure les NO adjudicades' not verified; incomplete records possible")
            elif diagnostics["unassigned"]["changed"]:
                page.wait_for_timeout(1200)
            for code in opts.codes:
                try:
                    snapshot = page.evaluate(INITIAL_DRAW,{"code":code,"course":opts.course,"size":opts.page_size,"timeout":25000})
                    info = snapshot["info"]
                    n_pages = int(info.get("pages") or 0)
                    retrieved = list(snapshot["rows"])
                    one = {"code":code,"reported_filtered":info.get("recordsDisplay"),
                           "pages":n_pages,"retrieved_first_page":len(snapshot["rows"]),
                           "reported_total":info.get("recordsTotal")}
                    if n_pages>opts.max_pages:
                        diagnostics["warnings"].append(f"{code}: truncated {n_pages} pages at {opts.max_pages}")
                    for ix in range(1,min(n_pages,opts.max_pages)):
                        result=page.evaluate(NEXT_DRAW,{"pageNum":ix,"timeout":25000})
                        if int(result["info"].get("page",-1)) != ix:
                            diagnostics["warnings"].append(f"{code}: requested page {ix}, server returned {result['info'].get('page')}")
                            break
                        retrieved.extend(result["rows"])
                    one["retrieved_total"] = len(retrieved)
                    checks.append(one)
                    raw.extend(retrieved)
                    if one["reported_filtered"] is not None and len(retrieved)<int(one["reported_filtered"]):
                        diagnostics["warnings"].append(f"{code}: incomplete pagination: {len(retrieved)}/{one['reported_filtered']}")
                    if not retrieved:
                        diagnostics["warnings"].append(f"{code}: no DataTables results; cannot certify zero DC")
                except Exception as exc:
                    checks.append({"code":code,"error":str(exc)})
                    diagnostics["warnings"].append(f"{code} failed: {exc}")
            # The table is a NOMENAMENTS history, not the offer/publication archive.
            diagnostics["complete"] = bool(checks and all("error" not in k and k.get("reported_filtered") == k.get("retrieved_total") for k in checks)
                and diagnostics["unassigned"].get("found") and not diagnostics["warnings"])
        except Exception as e:
            diagnostics["fatal_error"] = str(e)
            diagnostics["warnings"].append(str(e))
            try:
                page.screenshot(path=str(output/"ustec_error.png"),full_page=True)
            except Exception:
                pass
        finally:
            browser.close()

    raw_rows=[]
    for item in raw:
        mapped=record_from_raw(diagnostics.get("table",{}).get("labels",[]),item)
        if mapped is not None:
            raw_rows.append(mapped)
    a,b,c,counts=reduce_records(raw_rows,opts.codes,date.fromisoformat(opts.start),date.fromisoformat(opts.end),opts.course)
    diagnostics["rows"] = {"retrieved":len(raw),"valid_course_specialty":len(a),
                           "target_period":len(b),"explicit_dc":len(c),"exclusions":dict(counts),
                           "procedures":dict(Counter(r["procediment"] for r in b))}
    if diagnostics.get("fatal_error") or diagnostics["warnings"]:
        diagnostics["complete"] = False
    diagnostics["finished"] = datetime.now().astimezone().isoformat()
    write_csv(output/"USTEC_nomenaments_curs_i_codis.csv",a,opts.anonymize)
    write_csv(output/"USTEC_nomenaments_periode.csv",b,opts.anonymize)
    write_csv(output/"USTEC_nomenaments_DC_explicits.csv",c,opts.anonymize)
    (output/"AUDITORIA_EXTRACCIO.json").write_text(json.dumps(diagnostics,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"rows_period":len(b),"dc_explicit":len(c),"complete":diagnostics["complete"],"warnings":diagnostics["warnings"],"output":str(output)},ensure_ascii=False,indent=2))
    return 0 if diagnostics["complete"] else 2


def main():
    pa=argparse.ArgumentParser(description=__doc__)
    pa.add_argument("--output",default="./resultats_ustec")
    pa.add_argument("--course",default="2025-2026")
    pa.add_argument("--codes", nargs="+", default=list(CODES))
    pa.add_argument("--start",default="2025-11-01")
    pa.add_argument("--end",default="2026-02-28")
    pa.add_argument("--page-size",type=int,default=250)
    pa.add_argument("--max-pages",type=int,default=120)
    pa.add_argument("--chromium",help="Explicit installed Chromium path")
    pa.add_argument("--headful", action="store_true")
    pa.add_argument("--test",action="store_true",help="Execute offline self-tests")
    pa.add_argument("--anonymize", action="store_true", help="Mask assigned teacher numbers for publicly downloadable CSV artifacts")
    args=pa.parse_args()
    if args.test:
        from unittest import TestCase, TestLoader, TextTestRunner
        class Basic(TestCase):
            def test_dc_accents(self):
                self.assertTrue(is_dc('Nomenament per Difícil cobertura'))
                self.assertTrue(is_dc('DC'))
                self.assertFalse(is_dc('Nomenaments telemàtics'))
            def test_specialties(self):
                self.assertTrue(matches_code('F57-507','507'))
                self.assertTrue(matches_code('F57-507','F57'))
                self.assertFalse(matches_code('1507','507'))
            def test_dates(self):
                self.assertEqual(date_parse('20/11/2025'),date(2025,11,20))
                self.assertEqual(date_parse('2026-01-02'),date(2026,1,2))
            def test_anonymize(self):
                import tempfile
                with tempfile.TemporaryDirectory() as d:
                    path=Path(d)/"a.csv"
                    write_csv(path,[dict(zip(COLUMNS,["BLL","15/12/2025","45781","Institut X","1","627","16/12/2025","30/06/2026","Difícil cobertura","2025-2026"]))],True)
                    data=path.read_text(encoding="utf-8-sig")
                    self.assertNotIn("45781",data)
                    self.assertIn("REDACTAT",data)
            def test_filters(self):
                rec=dict(zip(COLUMNS,['BLL','15/12/2025','No adjudicat','Institut X','1','627','16/12/2025','30/06/2026','Difícil cobertura','2025-2026']))
                all_,month,dc,_=reduce_records([rec,rec],CODES,date(2025,11,1),date(2026,2,28),'2025-2026')
                self.assertEqual((len(all_),len(month),len(dc)),(1,1,1))
        result=TextTestRunner(verbosity=2).run(TestLoader().loadTestsFromTestCase(Basic))
        return 0 if result.wasSuccessful() else 1
    if date.fromisoformat(args.start)>date.fromisoformat(args.end):
        pa.error("start must not be after end")
    return run_browser(args)


if __name__=='__main__':
    sys.exit(main())