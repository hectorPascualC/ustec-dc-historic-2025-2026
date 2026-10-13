#!/usr/bin/env python3
"""V73: reconcile V49 36-ID census with Jan 2026 archived EDUBCN UI+API.

Independent official evidence required:
  - PADICAT Jan29 REST JSON: four CODI + DATA dates.
  - PADICAT Jan29 JS bundle template: explicit Data de publicacio -> DATA.
  - V52 original PDFs: FTE, result status, inconsistent original deadlines.

The portal-displayed posting date need not be first-ever publication; preserve
original historical source and date fields; never infer uncovered territory.
"""
import argparse,csv,datetime,json,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V49_36IDS.csv"
FIX=ROOT/"cens/EDUBCN_4_CASOS_V52_CORRECCIONS.csv"
API=ROOT/"exports_padicat/EDUBCN_20260129_V41_TARGET_OFFERS.json"
JS=ROOT/"exports_padicat/EDUBCN_V72_ARCHIVED_JS_PUBLIC_API_ROUTES.json"
NEW_COLUMNS=[
  "data_publicacio_portal_EDUBCN_arxivada",
  "evidencia_data_publicacio_portal",
  "advertencia_data_publicacio_vs_primera_publicacio",
  "jornada_pdf_original_verificada",
  "tipus_document_pdf_original_verificat",
  "estat_resultat_pdf_original",
  "termini_inicial_pdf_original",
  "fi_literal_pdf_original",
  "alerta_posterior_a_original",
]
ARCHIVED_API="https://wayback.padicat.cat/20260129224630id_/https://www.edubcn.cat/pdc_rest/convocatories/ca"
ARCHIVED_JS="https://wayback.padicat.cat/20260129224629id_/https://www.edubcn.cat/pdc/js/app.bundle-v05.js"
def csvrows(p):
    with p.open("r",encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))
def main(csv_dest,json_dest):
    rows=csvrows(SRC)
    fixes={r["id_canonic"]:r for r in csvrows(FIX)}
    api_doc=json.loads(API.read_text(encoding="utf-8"))
    api_rows={x["CODI"]:x for x in api_doc["target_rows"]}
    jsdoc=json.loads(JS.read_text(encoding="utf-8"))
    archived=[v for v in jsdoc["versions"] if v["type"].startswith("PADICAT_ARCHIVED_20260129224629")]
    if len(archived)!=1 or archived[0]["download"].get("status")!=200:
        raise RuntimeError("January 2026 JS archive was not read; publication semantics unverified")
    fragments=archived[0]["public_route_string_candidates"]
    if not any("Data de publicació:" in s and "convocatoria.DATA" in s for s in fragments):
        raise RuntimeError("January 2026 archived UI does not link Data de publicacio to DATA")
    if api_doc.get("source_http")!=200 or api_doc.get("capture_at")!="2026-01-29T22:46:30Z":
        raise RuntimeError("Archived EDUBCN API positive control is not verified")
    if len(rows)!=36 or len(fixes)!=4 or len(api_rows)!=4:
        raise RuntimeError("Unexpected census/API/V52 dimensions")
    by_id={r["id"]:r for r in rows}
    if len(by_id)!=36 or set(fixes)!=set(api_rows) or not set(fixes).issubset(by_id):
        raise RuntimeError("IDs mismatch, unsafe to propagate dates or statuses")
    for row in rows:
        for col in NEW_COLUMNS:row[col]=""
        rid=row["id"]
        if rid not in api_rows:continue
        entry=api_rows[rid]
        doc=fixes[rid]
        date=entry["DATA"]
        if not (date.startswith("2025-12") or date.startswith("2026-01")):
            raise RuntimeError("Publication field outside the audited range")
        row["data_publicacio_certificada"]=date
        row["data_publicacio_portal_EDUBCN_arxivada"]=date
        row["evidencia_data_publicacio_portal"]="PADICAT 2026-01-29: API.DATA + plantilla JS Data de publicació"
        row["advertencia_data_publicacio_vs_primera_publicacio"]=(
            "Data indicada com a publicacio al portal; primera publicacio/republicacions anteriors no establertes")
        row["jornada"]=doc["jornada_verificada"]
        row["jornada_pdf_original_verificada"]=doc["jornada_verificada"]
        row["tipus_document_pdf_original_verificat"]=doc["tipus_document_original"]
        row["estat_resultat_pdf_original"]=doc["estat_resultat_pdf"]
        row["termini_inicial_pdf_original"]=doc["termini_inicial_pdf"]
        row["fi_literal_pdf_original"]=doc["fi_prevista_pdf"]
        row["alerta_posterior_a_original"]=doc["alerta_auditoria"]
        row["publicacio_exacta"]="Portal EDUBCN DATA: "+date+" (arxivada 29/01/2026)"
    counts=collections.Counter(x["especialitat"] for x in rows)
    if counts!=collections.Counter({"507":21,"627":14,"F57-507":1}):
        raise RuntimeError(f"Unexpected specialty counts: {counts}")
    cert=[x for x in rows if x["data_publicacio_certificada"]]
    if len(cert)!=4 or sum(x["jornada"]=="0,25" for x in cert)!=1:
        raise RuntimeError("Corrections or certified dates failed invariant")
    dest=Path(csv_dest);dest.parent.mkdir(parents=True,exist_ok=True)
    cols=list(csvrows(SRC)[0].keys())+NEW_COLUMNS
    with dest.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rows)
    summary={"generated_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source_census":str(SRC.relative_to(ROOT)),
        "source_pdf_corrections":str(FIX.relative_to(ROOT)),
        "source_archived_api":str(API.relative_to(ROOT)),
        "source_archived_js":str(JS.relative_to(ROOT)),
        "archived_api_original_url":ARCHIVED_API,
        "archived_publication_template_js":ARCHIVED_JS,
        "jan2026_archive_js_sha256":archived[0]["download"]["sha256"],
        "evidence":"Jan29 captured Angular template Data de publicació: {{ctrl.convocatoria.DATA | date: ...}}",
        "unique_offers":len(rows),"by_specialty":dict(counts),
        "documented_portal_publication_dates":len(cert),
        "first_ever_publishing_proven":0,
        "portal_dates":[{"id":x["id"],"specialty":x["especialitat"],
                          "date":x["data_publicacio_certificada"],"fte":x["jornada"],
                          "initial_pdf_deadline":x["termini_inicial_pdf_original"],
                          "result":x["estat_resultat_pdf_original"],
                          "notice":x["alerta_posterior_a_original"]} for x in cert],
        "other_32_undated":len(rows)-len(cert),
        "verified_exhaustive_territory_month_cells":0,
        "warnings":["The official archived UI labels API.DATA as date of publication, not as the first ever or only publication.",
          "The 2025 PDF deadlines for some Jan 2026 portal records may indicate an old notice, republication, or portal update.",
          "The PDF source for GENSEC_2526_149 has contradictory finish date 31/08/2025; not a reliable end date.",
          "No candidate or winning teacher names, identity numbers, emails or phone numbers exported."]}
    jd=Path(json_dest);jd.parent.mkdir(parents=True,exist_ok=True)
    jd.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:summary[k] for k in ("unique_offers","by_specialty","documented_portal_publication_dates",
      "other_32_undated","verified_exhaustive_territory_month_cells")},ensure_ascii=False))
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output-csv",required=True)
    p.add_argument("--output-json",required=True)
    a=p.parse_args();main(a.output_csv,a.output_json)
