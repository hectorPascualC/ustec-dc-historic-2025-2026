#!/usr/bin/env python3
"""Reconstruct 2025-11..2026-02 DC *published offer evidence*, not personnel counts.

Archive results may be incomplete. Failure to locate a capture is never a zero-offers claim.
Only publishes metadata from public sources; no teacher names / applicant identifiers.
"""
from __future__ import annotations
import argparse, collections, csv, hashlib, io, json, os, re, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlsplit
import requests

START, END = '20251101', '20260228'
CODES = {'507', '627', 'F57', 'F87'}
HOST = 'https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials'
TERRITORIES = {
    'Barcelonès':'barcelones', 'Baix Llobregat':'baix-llobregat',
    'Vallès Occidental':'valles-occidental', 'Maresme–Vallès Oriental':'maresme-valles-oriental',
    'Catalunya Central':'catalunya-central', 'Girona':'girona', 'Lleida':'lleida',
    'Tarragona':'tarragona', 'Terres de l’Ebre':'terres-ebre',
    'Penedès':'penedes', 'Alt Pirineu i Aran':'alt-pirineu-aran',
}
BCO = HOST + '/barcelones/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/'
BLL = HOST + '/baix-llobregat/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/'
PEN = HOST + '/penedes/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/'
PREVIOUS_IDS = {
'19217376','19243858','19258737','19262024','19336990','19072798','19239349',
'19273855','19281261','19089426','19143261','19181817','19254245','19276920',
'19297807','19303623','19312477','19317939','19181782','19246854','19258568',
'19303622','19334052','19357285','2025/SEC/266','2025/SEC/259',
'2025/SEC/PFI/245','19224754'
}
SEED_URLS = [
    (BLL + 'PENDENTS_BLL-SEC-dificil-cobertura-oferta-vacants.pdf','Baix Llobregat'),
    (BLL + 'RESULTAT_BLL-SEC-dificil-cobertura-vacants-cobertes.pdf','Baix Llobregat'),
    (PEN + 'PEN-SEC-dificil-cobertura-vacants-cobertes.pdf','Penedès'),
    *[(BCO + fname,'Barcelonès') for fname in [
        'Barcelones-SEC-dificil-cobertura-oferta-vacants_07112025.pdf',
        'Barcelones-SEC-dificil-cobertura-oferta-vacants_14112025.pdf',
        'Barcelones-SEC-dificil-cobertura-oferta-vacants_28112025.pdf',
        'Barcelones-SEC-dificil-cobertura-oferta-vacants_09012026.pdf',
        'Barcelones-SEC-dificil-cobertura-oferta-vacants_16012026.pdf',
        'BCO-SEC-dificil-cobertura-oferta-vacants23012026.pdf',
        'BCO-SEC-dificil-cobertura-oferta-vacants30012026.pdf',
        'BCO-SEC-dificil-cobertura-oferta-vacants06022026.pdf',
        'BCO-SEC-dificil-cobertura-oferta-vacants20022026.pdf',
    ]],
    ('https://www.edubcn.cat/ca/professorat_i_pas/seleccio_rrhh/dificil_cobertura','Consorci Educació Barcelona'),
]
PREFIX_URLS = [(f'{HOST}/{slug}/personal-docent/nomenaments-telematics/dificil-cobertura/', name)
               for name, slug in TERRITORIES.items()]
ARCHIVE_SOURCES = ['Wayback','Arquivo.pt','Common Crawl']
HDR = {'User-Agent':'DC-Catalunya-historical-research/1.0 (public education archives; noncommercial; request-delay 0.4s)',
       'Accept':'application/json,text/plain,*/*'}
CAPS = {'max_archive_hits':180, 'max_pdf_downloads':35, 'max_pdf_bytes':12_000_000}
YEAR_RE = re.compile(r'(?<!\d)(2025|2026)[\-/]?(0[1-9]|1[0-2])[\-/]?([0-3]\d)(?!\d)')
ID_RE = re.compile(r'(?<!\d)(1\d{7}|2\d{7})(?!\d)')
CODE_RE = re.compile(r'(?<!\w)(?:F57|F87|507|627)(?!\w)',re.I)
PERSON_RE = re.compile(r'(?i)\b(?:resultat|cobertes|adjudicad[ao])\b')


def http(url,params=None,timeout=17,raw=False,range_header=None):
    headers=dict(HDR)
    if range_header: headers['Range']=range_header
    r=requests.get(url,params=params,timeout=timeout,headers=headers,allow_redirects=True,stream=True)
    try:
        r.raise_for_status()
        if raw:
            data=b''
            for block in r.iter_content(16384):
                data+=block
                if len(data)>CAPS['max_pdf_bytes']:
                    raise ValueError('download exceeds maximum permitted bytes')
            return data
        return r.text
    finally:
        r.close()


def parse_cdx_wayback(body):
    data=json.loads(body)
    if not isinstance(data,list) or not data: return []
    head=data[0]
    return [dict(zip(head,row)) for row in data[1:] if isinstance(row,list)]


def parse_cdx_cc(body):
    rows=[]
    for line in body.splitlines():
        try:
            row=json.loads(line)
            if isinstance(row,dict): rows.append(row)
        except (ValueError, TypeError): pass
    return rows


def parse_arquivo(body):
    txt=body.lstrip()
    try:
        js=json.loads(txt)
        if isinstance(js,dict): return js.get('response_items',[])
        if isinstance(js,list): return [x for x in js if isinstance(x,dict)]
    except ValueError: pass
    # CDX plain text from arquivo.pt/wayback/cdx may carry CDXJ and header lines.
    rows=[]
    for line in body.splitlines():
        try:
            if line.startswith('{'): rows.append(json.loads(line))
            elif ' {' in line: rows.append(json.loads(line.split(' {',1)[1].join(['{',''])))
        except ValueError: continue
    return rows


def archive_queries(cc_indexes=None):
    """Yield bounded queries with official seed URLs first, then URL prefix discovery."""
    for u,territory in SEED_URLS:
        yield {'source':'Wayback', 'target':u,'territory':territory,'mode':'exact',
               'endpoint':'https://web.archive.org/cdx/search/cdx',
               'params':{'url':u,'output':'json','from':'202510','to':'202610',
                         'filter':'statuscode:200','limit':'120'}}
        yield {'source':'Arquivo.pt','target':u,'territory':territory,'mode':'exact',
               'endpoint':'https://arquivo.pt/textsearch',
               'params':{'versionHistory':u,'maxItems':'100','from':'20251001','to':'20261012'}}
    for u,territory in PREFIX_URLS:
        yield {'source':'Wayback', 'target':u,'territory':territory,'mode':'prefix',
               'endpoint':'https://web.archive.org/cdx/search/cdx',
               'params':{'url':u+'*','output':'json','from':'202510','to':'202603',
                         'filter':'statuscode:200','limit':'500'}}
    # Common Crawl is sparse, but query 4 representative crawl indexes, bounded to 3 scoped prefixes.
    cc_indexes=cc_indexes or ['CC-MAIN-2025-47','CC-MAIN-2025-51','CC-MAIN-2026-04','CC-MAIN-2026-08']
    for index in cc_indexes:
        for url,territory in [ (BCO+'*','Barcelonès'), (BLL+'*','Baix Llobregat'),
                               ('https://www.edubcn.cat/ca/professorat_i_pas/seleccio_rrhh/dificil_cobertura*','Consorci Educació Barcelona')]:
            yield {'source':'Common Crawl','target':url,'territory':territory,'mode':'prefix',
                   'endpoint':f'https://index.commoncrawl.org/{index}-index',
                   'params':{'url':url,'output':'json','filter':'status:200','pageSize':'100'},'collection':index}


def safe_meta(row, source,territory):
    """Keep public URL/date/digest information, never personnel fields."""
    original=row.get('original') or row.get('originalURL') or row.get('url') or ''
    original=str(original)
    stamp=str(row.get('timestamp') or row.get('tstamp') or row.get('captureTimestamp') or '')
    status=str(row.get('statuscode') or row.get('status') or row.get('statusCode') or '')
    digest=str(row.get('digest') or '')
    return {'source':source,'territory':territory,'original_url':original,
            'capture_timestamp':stamp,'status':status,'digest':digest,
            'archive_link':str(row.get('linkToOriginalFile') or row.get('linkToArchive') or ''),
            'warc_file':str(row.get('filename') or ''),
            'warc_offset':str(row.get('offset') or ''), 'warc_length':str(row.get('length') or '')}


def extract_pdf_text(data):
    import fitz  # pymupdf; installed only by runner, unit tests bypass
    d=fitz.open(stream=data,filetype='pdf')
    try: return [(p.number+1,p.get_text(sort=True)) for p in d]
    finally: d.close()


def relevant_codes(text):
    return sorted(set(CODE_RE.findall(text.upper())))


def classify_document(url, text):
    """Only offer documents with explicit offer header; result docs separate."""
    base=urlsplit(url).path.lower()
    first=text[:800].lower()
    if 'vacants-cobertes' in base or 'resultat' in base or ('resultat' in first and 'adjudicacion' in first): return 'resultat'
    if ('oferta-vacants' in base or 'pendents_' in base or 'oferta de vacants' in first or 'oferta de vacants o substitucions' in first): return 'oferta'
    return 'indeterminat'


def pdf_evidence(meta, content, observed_url):
    sha=hashlib.sha256(content).hexdigest()
    rows=[]
    pages=extract_pdf_text(content)
    if not pages: return {'sha256':sha,'pages':0,'codes':[], 'ids':[], 'doc_type':'indeterminat'}, []
    full='\n'.join(t for _,t in pages)
    typ=classify_document(meta['original_url'],full)
    ids=[]; codes=[]
    for n,text in pages:
        found_ids=sorted(set(ID_RE.findall(text)))
        c=relevant_codes(text)
        ids.extend(found_ids);codes.extend(c)
        if c and found_ids:
            for ident in found_ids:
                rows.append({'source':meta['source'],'territory':meta['territory'],'capture_timestamp':meta['capture_timestamp'],
                            'document_url':meta['original_url'],'archive_url':observed_url,
                            'sha256':sha,'document_type':typ,'pdf_page':n,
                            'id':ident,'codes_on_page':';'.join(c),
                            'id_in_previous_28':ident in PREVIOUS_IDS,
                            'date_publication_certified':False})
    return {'sha256':sha,'pages':len(pages),'codes':sorted(set(codes)), 'ids':sorted(set(ids)),'doc_type':typ},rows


def download_capture(meta):
    """Only download captures with verifiable PDF bytes. Drop all non-pdf data."""
    source=meta['source']; ts=meta['capture_timestamp']; u=meta['original_url']
    if source=='Wayback':
        if not ts or not u: raise ValueError('capture timestamp/url absent')
        link=f'https://web.archive.org/web/{ts}id_/{u}'
        raw=http(link,timeout=35,raw=True)
    elif source=='Arquivo.pt':
        link=meta.get('archive_link') or ''
        if not link: link=f'https://arquivo.pt/noFrame/replay/{ts}id_/{u}'
        raw=http(link,timeout=35,raw=True)
    elif source=='Common Crawl':
        n=int(meta['warc_length']); offset=int(meta['warc_offset'])
        if n>2_000_000: raise ValueError('WARC slice exceeds safe limit')
        link='https://data.commoncrawl.org/'+meta['warc_file']
        raw=http(link,range_header=f'bytes={offset}-{offset+n-1}',timeout=35,raw=True)
        from warcio.archiveiterator import ArchiveIterator
        warc=list(ArchiveIterator(io.BytesIO(raw)))
        if not warc: raise ValueError('WARC range not decoded')
        raw=warc[0].content_stream().read(CAPS['max_pdf_bytes']+1)
    else: raise ValueError(source)
    if not raw.lstrip().startswith(b'%PDF-'):
        raise ValueError('archive retrieval not a genuine PDF (no PDF magic)')
    return raw,link


def write_csv(path,items,cols):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,cols,extrasaction='ignore');w.writeheader();w.writerows(items)


def archive_query_once(task):
    start=time.monotonic()
    record={'source':task['source'],'mode':task['mode'],'territory':task['territory'],
            'target':task['target'],'collection':task.get('collection',''),'response':'','hits':0,'error':'','elapsed_sec':0}
    hits=[]
    try:
        # Slow public archives: concurrency cap in run(), per-request timeout and no unconditional retries.
        body=http(task['endpoint'],params=task['params'],timeout=18)
        if task['source']=='Wayback': raw=parse_cdx_wayback(body)
        elif task['source']=='Arquivo.pt':raw=parse_arquivo(body)
        else:raw=parse_cdx_cc(body)
        for row in raw[:CAPS['max_archive_hits']]:
            meta=safe_meta(row,task['source'],task['territory'])
            if not meta['original_url']:continue
            hits.append(meta)
        record['response']='ok';record['hits']=len(hits)
    except Exception as e:
        record['response']='error';record['error']=str(e)[:180]
    record['elapsed_sec']=round(time.monotonic()-start,2)
    return record,hits


def compile_report(results, captures, docs, rows, output):
    sources=collections.Counter(x['source'] for x in captures)
    statuses=collections.Counter((x['source'],x['response']) for x in results)
    unique_docs={d['sha256']:d for d in docs if d.get('sha256')}
    candidates=[x for x in rows if x['document_type']=='oferta' and any(c in CODES for c in x['codes_on_page'].split(';'))]
    confirmed=[x for x in candidates if x['date_publication_certified']]
    unique_ids={x['id'] for x in candidates}
    matches=unique_ids.intersection(PREVIOUS_IDS)
    report={'as_of':datetime.now(timezone.utc).isoformat(),'range':{'start':'2025-11-01','end':'2026-02-28'},
            'codes':sorted(CODES), 'territorial_scopes':list(TERRITORIES)+['Consorci Educació Barcelona'],
            'archive_queries':len(results),'query_result_counts':{f'{a} / {b}':n for (a,b),n in sorted(statuses.items())},
            'archive_hits':len(captures),'by_source':sources,
            'verified_pdf_copies':len(docs),'unique_pdf_sha256':len(unique_docs),
            'candidate_offer_ids_from_verified_pdfs':len(unique_ids),
            'previous_28_matched':len(matches),'new_candidate_ids':sorted(unique_ids-PREVIOUS_IDS),
            'offer_identifiers_with_certified_actual_publication_dates':len(confirmed),
            'completeness':'NOT CERTIFIED',
            'territory_month_certified':0,
            'territory_month_total':48,
            'limitations':[
              'Archive captures are incomplete samples; lack of a capture does NOT demonstrate zero offers.',
              'PDF captures after date range do not prove historic publication date.',
              'Offer document type and page-code-ID matching are heuristic and require human validation.',
              'A PDF result document is not an offer publication; no result-only case is counted as publication.',
              'EDUBCN dynamic historical listings have not been exhaustively enumerated.',
              'Common Crawl and Arquivo.pt coverage can be sparse; a timeout is not an absence.',
              'The 28-case preexisting list includes result-only cases with unknown publication dates.',
            ],'final_audit':'FAIL: incomplete original publication/republication record, not a total census'}
    (output/'AUDITORIA_ARCHIUS_DC.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=list)+'\n',encoding='utf-8')
    return report


def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument('--output',default='archive-results')
    p.add_argument('--workers',type=int,default=4)
    p.add_argument('--max-downloads',type=int,default=35)
    p.add_argument('--test',action='store_true')
    args=p.parse_args(argv)
    if args.test:
        assert len(PREVIOUS_IDS)==28
        assert parse_cdx_wayback('[["timestamp","original","statuscode"],["20251101120000","https://site/x.pdf","200"]]')[0]['timestamp']=='20251101120000'
        assert parse_cdx_cc('{"url":"https://a/x.pdf","status":"200"}\n')==[{'url':'https://a/x.pdf','status':'200'}]
        assert relevant_codes('507 Informàtica 627 Sistemes F57 PFI F87')==['507','627','F57','F87']
        assert classify_document('https://x/oferta-vacants.pdf','')=='oferta'
        assert classify_document('https://x/vacants-cobertes.pdf','')=='resultat'
        assert classify_document('https://x/other.pdf','')=='indeterminat'
        print('7 local unit checks: PASS')
        return 0
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    queries=list(archive_queries());rec=[];all_hits=[]
    with ThreadPoolExecutor(max_workers=max(1,min(args.workers,5))) as executor:
        futs={executor.submit(archive_query_once,q):q for q in queries}
        for f in as_completed(futs):
            result,hits=f.result()
            rec.append(result);all_hits.extend(hits)
            print(f"{result['source']} {result['territory']} {result['mode']}: {result['response']}, hits={result['hits']}",flush=True)
    # Keep exact (capture timestamp, original url, source) keys; do not dedupe distinct dated captures.
    uniq={ (x['source'],x['capture_timestamp'],x['original_url']):x for x in all_hits }
    captures=list(uniq.values())
    # Prioritize clearly named historic official PDF offers, not current overwritten PDFs and result-only files.
    pdf_hits=[h for h in captures if '.pdf' in h['original_url'].lower() and
              any(q in h['original_url'].lower() for q in ['oferta','pendents','coberta','resultat','dc-sec'])]
    pdf_hits.sort(key=lambda h:( 'oferta' not in h['original_url'].lower(),
                               not ('202511' in h['original_url'] or '202601' in h['original_url'] or '202602' in h['original_url']),
                               h['source']!='Wayback',h['capture_timestamp']))
    docs=[];evidence=[];attempts=[]
    cap=min(CAPS['max_pdf_downloads'],max(0,args.max_downloads))
    for h in pdf_hits[:cap]:
        entry={'source':h['source'],'territory':h['territory'],'original_url':h['original_url'],
               'capture_timestamp':h['capture_timestamp'],'status':'error','message':'','sha256':''}
        try:
            content,archive_url=download_capture(h)
            doc,pages=pdf_evidence(h,content,archive_url)
            if not doc['pages']: raise ValueError('pdf has no pages')
            entry.update(status='verified_pdf',message=f"pages={doc['pages']}",sha256=doc['sha256'])
            docs.append({'source':h['source'],'territory':h['territory'],'original_url':h['original_url'],
                         'capture_timestamp':h['capture_timestamp'],'archive_url':archive_url,**doc})
            evidence.extend(pages)
        except Exception as e:entry['message']=str(e)[:170]
        attempts.append(entry)
    write_csv(out/'ARXIU_CONSULTES.csv',sorted(rec,key=lambda r:(r['source'],r['territory'],r['target'])),
              ['source','mode','territory','target','collection','response','hits','error','elapsed_sec'])
    write_csv(out/'ARXIU_CAPTURES.csv',captures,
              ['source','territory','original_url','capture_timestamp','status','digest','archive_link','warc_file','warc_offset','warc_length'])
    write_csv(out/'DOCUMENTS_VERIFICATS.csv',docs,
              ['source','territory','original_url','capture_timestamp','archive_url','sha256','pages','doc_type','codes','ids'])
    write_csv(out/'EXTRACCIO_DOCUMENTS.csv',evidence,
              ['source','territory','capture_timestamp','document_url','archive_url','sha256','document_type','pdf_page','id','codes_on_page','id_in_previous_28','date_publication_certified'])
    write_csv(out/'DESCARREGUES.csv',attempts,
              ['source','territory','original_url','capture_timestamp','status','message','sha256'])
    report=compile_report(rec,captures,docs,evidence,out)
    print(json.dumps({'archive_queries':report['archive_queries'],'archive_hits':report['archive_hits'],
        'verified_pdf_copies':report['verified_pdf_copies'], 'new_candidate_ids':report['new_candidate_ids'],
        'final_audit':report['final_audit']},ensure_ascii=False,indent=2),flush=True)
    return 0

if __name__=='__main__':sys.exit(main())