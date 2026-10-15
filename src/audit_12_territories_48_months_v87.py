#!/usr/bin/env python3
"""V87: Reconcile ALL eleven ST and EDUBCN against actual evidence.

Read original V24 30 PDF hashes, V86 current 30 PDFs, V73 provisional unique
vacancy codes and certified EDUBCN publication dates, V69 48 historical
territory-month cells, and V82 Jan-Oct EDUBCN historic corpus. Produce three
traceable artifacts. Do not confuse current availability with historical.
"""
import argparse,csv,datetime,io,json,re,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/"exports_territorial/SSTT_PDFS.csv"
LIVE=ROOT/"exports_territorial/SSTT_V86_PDF_DATES_2025_11_TO_2026_02.json"
CENSUS=ROOT/"cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V73_36IDS.csv"
MATRIX=ROOT/"AUDITORIA_V69_MATRIU_48_TERRITORI_MES_NO_EXHAUSTIUS.md"
EDU=ROOT/"exports_padicat/EDUBCN_V82_FULL_OCT_DELTA_2025_26.json"
MONTHS=["2025-11","2025-12","2026-01","2026-02"]
def read_csv(path):
    with path.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def write_csv(path,rows):
    file=Path(path);file.parent.mkdir(parents=True,exist_ok=True)
    with file.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main(area_path,month_path,json_path):
    old=read_csv(OLD)
    new=json.loads(LIVE.read_text(encoding="utf-8"))
    census=read_csv(CENSUS)
    ed=json.loads(EDU.read_text(encoding="utf-8"))
    old_by_url={x["url"]:x for x in old}
    now=new["documents"];now_by_url={x["original_url"]:x for x in now}
    if len(old)!=30 or len(now)!=30 or set(old_by_url)!=set(now_by_url):
        raise RuntimeError("V24/V86 corpus mismatch; do not compare hashes")
    old_count=collections.Counter(x["territori"] for x in old)
    assert len(old_count)==11
    census_count=collections.Counter(x["territori"] for x in census)
    assert len(census)==36 and len({x["id"] for x in census})==36
    expected={"507":21,"627":14,"F57-507":1}
    assert dict(collections.Counter(x["especialitat"] for x in census))==expected
    valid_pub=[x for x in census if x["data_publicacio_certificada"]]
    assert len(valid_pub)==4
    lines=MATRIX.read_text(encoding="utf-8").splitlines()
    matrix=[]
    for line in lines:
        if not line.startswith("|"):continue
        cols=[x.strip() for x in line.strip().split("|")][1:-1]
        if len(cols)<4 or cols[1] not in MONTHS:continue
        status=re.sub(r"[*_]", "",cols[2]).strip()
        if status not in ("PARTIAL","BLOCKED"):continue
        matrix.append({"area":cols[0],"month":cols[1],
                       "previous_evidence_state":status,"source_note":cols[3]})
    assert len(matrix)==48, "Expected V69 48 distinct (area,month) cells"
    assert len(set((x["area"],x["month"]) for x in matrix))==48
    all_areas=set(x["area"] for x in matrix)
    assert set(old_count).issubset(all_areas) and len(all_areas)==12
    by_area=[]
    changed_urls=[]
    for area in sorted(all_areas):
        entries=[x for x in now if x["area"]==area]
        for x in entries:
            if old_by_url[x["original_url"]]["pdf_sha256"]!=x["sha256"]:
                changed_urls.append({"area":area,"url":x["original_url"],
                 "old_sha256":old_by_url[x["original_url"]]["pdf_sha256"],
                 "sha256_v86":x["sha256"]})
        area_valid=[x for x in valid_pub if x["territori"]==area]
        rows=[x for x in matrix if x["area"]==area]
        by_area.append({
          "territori":area,
          "pdfs_inventariats_i_llegits_v86":len(entries),
          "pdfs_valids_v86":sum(bool(x["is_pdf"]) for x in entries),
          "pdfs_sha_diferent_v24_v86":sum(old_by_url[x["original_url"]]["pdf_sha256"]!=x["sha256"] for x in entries),
          "pdfs_actuals_amb_dates_nov25_feb26_i_codis":sum(bool(x["possible_blocks"]) for x in entries),
          "ids_provisionals_v73":census_count[area],
          "dates_publicacio_portal_certificades_v73":len(area_valid),
          "controls_mensuals_parcials":sum(x["previous_evidence_state"]=="PARTIAL" for x in rows),
          "controls_mensuals_bloquejats":sum(x["previous_evidence_state"]=="BLOCKED" for x in rows),
          "controls_mensuals_exhaustius":0,
          "font_principal":"V86 PDF actual / V73 cens / V69 matriu / V82 EDUBCN",
          "advertiment":"Cap ID recollit implica absencia real; data de captura/inici no es data de publicacio."
        })
    pub_months=collections.Counter((x["territori"],x["data_publicacio_certificada"][:7]) for x in valid_pub)
    month_rows=[]
    for row in matrix:
        area=row["area"];month=row["month"]
        month_rows.append({
          "territori":area,"mes":month,
          "estat_cobertura":row["previous_evidence_state"],
          "publicacions_datades_al_portal_verificades":pub_months[(area,month)],
          "exhaustivitat_acreditada":"NO",
          "ofertes_inexistents_provades":"NO",
          "base_documental":row["source_note"][:260],
          "referencia":"V69 + V73 + V86 + V82",
          "criteri":"Data portada PDF/resultat no justifica data publicacio primer anunci"
        })
    assert sum(x["publicacions_datades_al_portal_verificades"] for x in month_rows)==4
    assert len(changed_urls)==13,f"Expected 13 V24/V86 changes; got {len(changed_urls)}"
    assert ed["jan_distinct_pdf_urls"]+ed["oct_distinct_pdf_urls"]-ed["oct_url_already_in_jan"]==557
    write_csv(area_path,by_area)
    write_csv(month_path,month_rows)
    detail={"at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "period":["2025-11-01","2026-02-28"],
        "territorial_areas_total":12,"sstt_areas":11,"edubcn_areas":1,
        "months_total":48,
        "months_evidence_partial":sum(x["estat_cobertura"]=="PARTIAL" for x in month_rows),
        "months_evidence_blocked":sum(x["estat_cobertura"]=="BLOCKED" for x in month_rows),
        "months_certified_exhaustive":0,
        "sstt_official_pdf_urls":30,
        "sstt_current_binary_pdfs_verified":sum(x["is_pdf"] for x in now),
        "sstt_pdf_url_same_but_sha_changed_since_v24":len(changed_urls),
        "sstt_pdf_historical_month_target_leads":sum(len(x["possible_blocks"]) for x in now),
        "pdf_changed_source_links":changed_urls,
        "provisional_identifiers":len(census),
        "identifiers_by_specialty":expected,
        "certified_portal_publishing_dates":len(valid_pub),
        "edubcn_unique_archived_pdf_urls":557,
        "territories":by_area,
        "warnings":["A changed SHA does not prove changed human-readable PDF text, only different bytes.","Current PDFs cannot close any historical month.",
          "Zero IDs in a territory is not zero real offers.",
          "4 portal dates in archived Jan 2026 do not prove initial posting or absence of prior reposting.",
          "No personal candidate details stored."]}
    target=Path(json_path);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(detail,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:detail[k] for k in ("territorial_areas_total","months_total",
         "months_evidence_partial","months_evidence_blocked",
         "sstt_current_binary_pdfs_verified","sstt_pdf_url_same_but_sha_changed_since_v24",
         "provisional_identifiers","certified_portal_publishing_dates")},ensure_ascii=False),flush=True)
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--areas",required=True)
    p.add_argument("--months",required=True)
    p.add_argument("--json",required=True)
    a=p.parse_args();main(a.areas,a.months,a.json)
