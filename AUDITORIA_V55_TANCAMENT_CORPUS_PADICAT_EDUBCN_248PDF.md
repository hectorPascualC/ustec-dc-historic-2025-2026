# AUDITORIA V55 — cobertura integral del directori PADICAT EDUBCN del 29/01/2026

**Data:** 13/10/2026. **Objectiu general:** ofertes publicades 01/11/2025–28/02/2026 de 507/627/F57/F87 als 11 SSTT i EDUBCN. **Aquest tancament és del corpus concret arxivat, NO del període complet.**

## 1. Partició documental sense solapaments

L'índex CDX públic de PADICAT per `https://www.edubcn.cat/rcs_gene/seleccio/` proporciona **252 registres**, dels quals **248 corresponen a URL PDF amb HTTP original 200**. La partició nominal dels 248 és:

| Auditoria | Selecció sense solapament | URL PDF recuperades | Resultat target |
|---|---|---:|---|
| V45 | PDF GENSEC/GESEC no RESULTAT | **33** | **4** ofertes ja al cens |
| V47 | PDF no-GENSEC sense paraules d'exclusió (primeres 7 pàgines) | **87** | 0 perfils documentats |
| V53 | PDF no-GENSEC restants, amb noms abans exclosos (totes les pàgines) | **113** | 0 candidats contextuals |
| V54 | PDF GENSEC/GESEC RESULTAT (totes les pàgines) | **15** | 2 resultats dels 4 casos coneguts |
| **TOTAL** | **Totes les URL PDF arxivades amb HTTP 200** | **248/248** | **4 ofertes diferents**, cap nova respecte de V51 |

Les 113 comprovacions V53: **113/113** descàrregues PDF correctes, **165 pàgines** llegides amb text extractable, **0** documents candidats. Les 15 comprovacions V54: **15/15** descàrregues correctes, **15 pàgines** llegides, **2** resultats ja coneguts. A V47: **87/87** PDFs vàlids amb text, només primers set fulls per document. A V45: **33/33** documents originals recuperats.

**No confondre 248 PDF arxivats amb 248 ofertes DC, ni 248 URL amb necessàriament 248 continguts binaris diferents.** El corpus inclou resultats, procediments administratius i especialitats alienes. Cap OCR d'imatges escanejades ha estat fet. La V47 pot no detectar mencions en pàgines posteriors a la setena, i cap detecció automàtica demostra absència universal de perfils en un PDF.

## 2. Els quatre identificadors objectiu recuperats de l'API arxivada

| ID canònic | Especialitat | Centre | Jornada contrastada V52 |
|---|---|---|---|
| `GENSEC_147` | 627 | Institut Escola del Treball | Sencera |
| `GENSEC2526_167` | 507 | Institut Pedralbes | Sencera |
| `GENSEC_2526_145` | 507 | Institut Tecnològic de Barcelona | Sencera |
| `GENSEC_2526_149` | 627 | Institut Tecnològic de Barcelona | **0,25** |

Els dos documents RESULTAT objectiu són els de `GENSEC_147` i `GENSEC_2526_145` (V52/V54). El primer identifica una adjudicació; el segon indica «Alta titular». No es dedueix una plaça deserta ni una persona fora de borsa. El PDF original `GENSEC_2526_149` presenta una **data final incoherent 31/08/2025**, que no s'usa com a fi real.

## 3. Temporalitat i PADICAT

- Fotografia única API històrica principal: **29/01/2026 a les 22:46:30Z**, **49 files**.
- Consultes CDX addicionals d'API per al període de novembre a mitjan març han recuperat les captures `ca` i `es` del **29/01**, però no una fotografia útil del febrer.
- Els PDF de l'ITB 507 i 627 indiquen terminis inicials del **03/12/2025** i **12/12/2025** respectivament, amb possible prolongació fins que es cobreixin; això no és prova de la data exacta de publicació inicial.
- Una captura del 29/01 no cobreix noves ofertes de febrer ni retirades anteriors a la captura. L'índex arxivat és una mostra de la web, no un registre administratiu diari.

## 4. Estat del cens nacional

**36 identificadors provisionals únics**: 21 de 507, 14 de 627, 1 F57-507. Inclou 4 EDUBCN i 32 d'altres SSTT. **0/48 blocs territori-mes complets certificats**. Ni l'exhaustivitat de Catalunya ni tots els casos deserts, retirats i republicats estan acreditats.

## 5. Fonts reproduïbles i integritat

- Índex directori: [V46](exports_padicat/EDUBCN_PADICAT_V46_FULL_DIRECTORY.json).
- Grup GENSEC ofertes: [V45](exports_padicat/EDUBCN_PADICAT_V45_ALL_PDFS.json).
- Grup no-GENSEC normal: [V47](exports_padicat/EDUBCN_PADICAT_V47_NONCODED_PDFS.json).
- Grup no-GENSEC noms exclosos: [V53](exports_padicat/EDUBCN_V53_REMAINING_EXCLUDED_PDFS.json).
- Grup GENSEC resultats: [V54](exports_padicat/EDUBCN_V54_GENSEC_RESULTS.json).
- Detall de resultats i condicions: [V52](AUDITORIA_V52_EDUBCN_RESULTATS_JORNADES_2026-10-13.md).
- Matriu territorial: [V51](cens/MATRIU_TERRITORIAL_V51_36IDS.csv).
- API original: https://wayback.padicat.cat/20260129224630id_/https://www.edubcn.cat/pdc_rest/convocatories/ca
- Scripts reproduïbles: `src/padicat_edubcn_remaining_pdfs_v53.py` i `src/padicat_edubcn_gensec_results_v54.py`.

**Veredicte documental: PASS** — revisió de totes les 248 URL PDF amb captura històrica vàlida del directori EDUBCN a PADICAT el 29/01/2026. **Veredicte de la missió general: FAIL / no exhaustiva** — no hi ha proves de cobertura de totes les dates i territoris. Les absències d'índex no impliquen zero convocatòries reals.

**Protecció de dades:** cap nom de docent/adjudicatari, identificador personal, telèfon o correu de candidat publicat als resultats de les rondes V53/V54/V55.
