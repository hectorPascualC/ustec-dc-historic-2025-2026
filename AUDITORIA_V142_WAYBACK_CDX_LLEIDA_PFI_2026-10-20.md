# Auditoria V142 — Wayback CDX Lleida PFI, 20/10/2026 23:30 Europe/Madrid

Abast: convocatòries DC 507/627/F57/F87 publicades 01/11/2025–28/02/2026; 11 SSTT i EDUBCN. No és el monitor 2026–27.

## P1 — consultes noves, respostes HTTP verificades

URL objectiu: `https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/lleida/personal-docent/nomenaments-telematics/dificil-cobertura/oferta-moduls-pfi-ptt/LLE-dificil-cobertura-oferta-PFI.pdf`.

1. Wayback CDX URL exacta, `from=202511&to=202602&filter=statuscode:200&output=json`: HTTP 200, JSON `[]`.
2. Wayback CDX prefix del directori `/lleida/personal-docent/nomenaments-telematics/dificil-cobertura/`, `matchType=prefix&from=202511&to=202602&filter=statuscode:200&output=json&collapse=urlkey`: HTTP 200, JSON `[]`.
3. Control positiu independent: Wayback CDX prefix Baix Llobregat `/baix-llobregat/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/`, `from=2025&to=2026`, HTTP 200 amb tres PDF capturats el 25/07/2025: `BLL-CFA-SECUNDARIA-CFA-PENITENCIARI.pdf` (15:03:59 UTC), `BLL-PFI.pdf` (13:48:11 UTC), `BLL-Vacants-Dificl-cobertura-IFE.pdf` (14:54:53 UTC). Ja documentats V141; aquí només control positiu de transport, NO nous documents.

Endpoint: `https://web.archive.org/cdx/search/cdx`. Consultes efectuades amb Firecrawl live `maxAge=0`; HTTP reportat en `metadata.statusCode`. Els dos `[]` només proven absència de registres retornats per aquestes consultes concretes amb filtre HTTP 200. No acrediten inexistència de captures amb altres codis, altres URL, altres índexs, ni inexistència d'ofertes. No s'ha recuperat WARC ni PDF nou, ni s'ha calculat SHA de payload.

## P2 i cens

Script públic `src/forensic_qpdf_pdfresurrect_v92.py` rellegit: 40 pàgines màxim, només `2025`, cap validació de SHA V24/V86, sense workflow V92 executat. GitHub `main` verificat abans d'aquesta auditoria: `0150998ca494ff30e6f977711dadee1cfef3b066`; darrer run real V91 `39415173344`, 13/13 descàrregues PyMuPDF, **0/13 qpdf/PDFResurrect**.

Sense oferta ni data nova acreditada: 36 IDs provisionals (21×507, 14×627, 1×F57-507) + 1 candidat separat; quatre registres EDUBCN amb data del portal (05/12/2025, 21/01/2026, 22/01/2026 dues vegades); 12/12 àmbits, 48 controls: 0 PASS / 14 PARTIAL / 34 BLOCKED. Cap control mensual esdevé exhaustiu per aquestes consultes.

**Estat: PARTIAL.** Següent via: validar URL alternatives i captures fora del període de Lleida, cercar originals dels resultats, desbloquejar workflow V92 amb comparació SHA.
