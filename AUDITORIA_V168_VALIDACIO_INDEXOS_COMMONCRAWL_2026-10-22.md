# Auditoria V168 — Control de validesa dels índexs Common Crawl (22/10/2026)

Abast: ofertes docents DC 507/627/F57/F87, 01/11/2025–28/02/2026, 11 SSTT + EDUBCN. Sense dades personals.

## Nova comprovació: inventari oficial d'índexs
Consulta en viu de `https://index.commoncrawl.org/collinfo.json` amb Firecrawl (`maxAge=0`): HTTP 200. Entre els índexs existents: `CC-MAIN-2025-51` (desembre 2025), `CC-MAIN-2026-04` (gener), `CC-MAIN-2026-08` (febrer), `CC-MAIN-2026-21` (maig), `CC-MAIN-2026-34` (agost), `CC-MAIN-2026-43` (octubre). **`CC-MAIN-2026-26` NO figura a l'inventari.**

Prova independent contra l'endpoint `CC-MAIN-2026-26-index` amb URL de control `https://example.com/`: HTTP 404, resposta literal `No index found for collection 'CC-MAIN-2026-26'`. Els índexs de control `CC-MAIN-2026-05` i `CC-MAIN-2026-33` també retornen HTTP 404 amb `No index found`. **Rectificació V167:** la consulta anterior a 2026-26 (504) no es pot considerar una comprovació vàlida de captures d'aquell PDF, perquè la col·lecció no existeix. El 504 és un error de transport/proxy, no un resultat de l'índex.

## Consultes noves a índexs vàlids
URL exacta oficial: `https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/barcelones/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/Barcelones-SEC-dificil-cobertura-oferta-vacants_05122025.pdf`.
- `CC-MAIN-2025-51`: HTTP 404, JSON `No Captures found for: [URL exacta]` — negatiu **només en aquest índex**.
- `CC-MAIN-2026-04`: HTTP 504 Gateway Time-out — BLOCKED.
- `CC-MAIN-2026-34`: HTTP 504 Gateway Time-out — BLOCKED.
- `CC-MAIN-2026-40`: HTTP 504 — també **col·lecció absent** de l'inventari; no considerar consulta vàlida.
- `CC-MAIN-2026-21`: negatiu documentat V167, no repetit avui.

No s'ha recuperat cap CDXJ amb `filename/offset/length`; cap WARC Range nou ni PDF binari nou. Sense prova de data original de primera publicació. Intent de recuperar els bytes de la captura Wayback `20260105180042` des del contenidor: DNS `NameResolutionError` — BLOCKED, no zero captures.

## Estat
PARTIAL. GitHub HEAD consultat `5314f3e4fa1a5ab9386ac8fb22ff6045b556e737`; darrer run V91 documentat `39415173344` SUCCESS; V92 qpdf/PDFResurrect no executat (0/13). 36 IDs provisionals (21×507, 14×627, 1×F57-507) + 1 candidat; quatre registres EDUBCN amb data del portal (05/12/2025, 21/01/2026, 22/01/2026 ×2); cobertura 12/12, controls 0 PASS / 14 PARTIAL / 34 BLOCKED, 0 exhaustius.

Següent pas: enumerar índexs exclusivament a partir de `collinfo.json` abans de cada consulta; prioritzar 2025-51, 2026-04/08/12/17/21/25/30/34/39/43 amb URL exacta i prefix, i no confondre col·lecció absent amb `No Captures found`.
