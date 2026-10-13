# AUDITORIA V61 — 11 lots datats del Barcelonès, trajectòries sense duplicats

**Data de contrast:** 13/10/2026. **Objectiu:** convocatòries DC 507/627/F57/F87 publicades entre 01/11/2025 i 28/02/2026. Protocol base: `REFERENCIA_RECUPERACIO_HISTORICA_PDF_DC_507_627_F57_F87.md` de la Biblioteca.

## Corpus i controls

Sources: `cens/INDEX_PDFS_BCO_V22_11_LOTS.csv`, `cens/REPUBLICACIONS_BCO_V22_11_LOTS_VERIFICATS.csv`, `cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V49_36IDS.csv`.

- **11 documents de PDF amb noms datats**, de 07/11/2025 a 27/02/2026.
- **60 aparicions** d'identificadors d'interès en els 11 documents.
- **17 identificadors diferents**, tots 17 ja inclosos al cens provisional nacional de 36 identificadors. No incrementar el cens per repeticions.
- Les 17 seqüències d'aparició són contínues **dins els 11 lots observats**: cap identificador desapareix i després torna a aparèixer en aquest mostreig. Aquesta continuïtat NO demostra cobertura de totes les setmanes ni cap adjudicació efectiva.

## Casos persistents

| ID | Especialitat | Lots amb presència | Primera aparició dins mostra | Última aparició dins mostra |
|---|---|---:|---|---|
| 19089426 | 507 | 11 | 07/11/2025 | 27/02/2026 |
| 19143261 | 507 | 11 | 07/11/2025 | 27/02/2026 |
| 19312477 | 507 | 7 | 16/01/2026 | 27/02/2026 |
| 19317939 | 507 | 6 | 23/01/2026 | 27/02/2026 |
| 19303623 | 507 | 4 | 16/01/2026 | 06/02/2026 |
| 19331041 | 507 | 4 | 06/02/2026 | 27/02/2026 |

D'aquestes 60 aparicions, **43 són recurrències de codis ja observats en altres documents de la mostra**; no són automàticament 43 places noves ni 43 ofertes independents.

## Contrast temporal d'indexació independent

Els cercadors conserven testimonis de documents de **24/10/2025, 14/11/2025, 05/12/2025 i 20/03/2026** amb el mateix ID `19143261` (507, Institut Provençana), jornada **0,50**, amb terminis i dates d'inici diferents. Això indica actualitzacions/noves inclusions en llistats successius abans, dins i després del període, però no aporta el PDF binari antic ni la data exacta de publicació de cada lot.

Fonts indexades contrastades:
- 24/10/2025: https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/barcelones/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/Barcelones-SEC-dificil-cobertura-oferta-vacants_24102025.pdf
- 14/11/2025: https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/barcelones/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/Barcelones-SEC-dificil-cobertura-oferta-vacants_14112025.pdf
- 05/12/2025: https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/barcelones/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/Barcelones-SEC-dificil-cobertura-oferta-vacants_05122025.pdf
- 20/03/2026 (fora de finestra): https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/barcelones/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/BCO-SEC-dificil-cobertura-oferta-vacants_20032026.pdf

Els documents antics actualment poden donar HTTP 404 i, per tant, la lectura prové de text indexat, no de binaris històrics. **Nivell d'evidència C**, mai A/B fins a tenir bytes i hash. La data al nom d'un PDF no s'ha copiat a `publication_date`.

## Recuperació addicional de PDF via Common Crawl

L'auditoria V62 (`src/commoncrawl_dated_bco_v62.py`) cerca les **11 URL exactes de noms datats del corpus** en índexs contemporanis de Common Crawl i, si troba un registre, intenta recuperar el PDF dins del WARC per validació de bytes i SHA256. **Resultat real V62**: 13 consultes completades (11 URL exactes, 2 consultes complementàries en un altre rastreig); **9 HTTP 404 sense captura**, **2 HTTP 502** i **2 HTTP 504**, cap registre CDXJ recuperat i **0 PDF binaris**. El primer intent V62 era invàlid per capçalera User-Agent mal formada i fou substituït per una execució real corregida el 13/10/2026. Els quatre errors 502/504 continuen sent bloquejos tècnics, no zeros de captures. [JSON V62](exports_commoncrawl/COMMONCRAWL_V62_BCO_DATED_PDFS.json).

**Conclusió V61:** PASS en deduplicació i cronologia documental; PARTIAL en determinació de publicació i estats de cobertura; FAIL en cens nacional exhaustiu. **Cens de 36 sense canvis, 0/48 territori-mes certificats.**
