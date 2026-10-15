# V90 — Passada d'arxius web i comprovació de falsos positius (16/10/2026)

**Hora de la passada:** 16/10/2026, 01:26–01:45 Europe/Madrid (aproximada). **Veredicte:** PARTIAL/BLOCKED; cap nou PDF històric recuperat, cap ID nou certificat.

## Proves noves realment executades

1. **Common Crawl — inventari de col·leccions:** petició real a https://index.commoncrawl.org/collinfo.json; contingut JSON llegible amb els índexs CC-MAIN-2025-47 (06–19/11/2025), CC-MAIN-2025-51 (04–17/12/2025), CC-MAIN-2026-04 (12–25/01/2026), CC-MAIN-2026-08 (06–19/02/2026). Això confirma la disponibilitat de l'inventari, NO pas captures de documents.
2. **Common Crawl — quatre consultes CDXJ:** tres URL exactes del PDF oficial GIR-SEC-dificil-cobertura-oferta-vacants.pdf (índexs 2025-47, 2025-51, 2026-04) i una consulta per prefix GIR-SEC* (índex 2026-08). Totes quatre han retornat el bloqueig del transport 'invalid_redirect_url'; no s'ha rebut cap resposta CDXJ interpretable. **4 BLOCKED; 0 comprovacions concloents; 0 WARC.**
3. **Wayback CDX i Arquivo.pt:** prova d'URL exacta del PDF de Girona en ambdós serveis; totes dues han retornat 'invalid_redirect_url' del transport. **2 BLOCKED**, no 0 captures.
4. **P0 — cerca de documents indexats:** consultes per Girona/507/novembre 2025, Tarragona/627/desembre 2025, Maresme–Vallès Oriental/507/gener 2026 i altres territoris amb 0 ID. Han aparegut PDF de 2026–27, fragments de resultats i el PDF MVO-SEC-dificil-cobertura-oferta-Tillers_estiu.pdf, que correspon a l'estiu de 2026 i queda **fora del període**. No hi ha cap ID nou admissible.
5. **Deduplicació:** el PDF BCO-SEC-dificil-cobertura-oferta-vacants20022026.pdf mostra l'ID 19357285, que ja consta al cens V73. No sumar-lo de nou.

## URL i mètode reproduïbles

- URL diana exacta: https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/girona/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/GIR-SEC-dificil-cobertura-oferta-vacants.pdf
- Índex CC: https://index.commoncrawl.org/collinfo.json
- CDXJ: https://index.commoncrawl.org/CC-MAIN-2025-47-index?url=<URL_Diana_URL_Encoded>&output=json (igual per 2025-51, 2026-04, 2026-08; l'última consulta amb prefix GIR-SEC*).
- Wayback CDX: https://web.archive.org/cdx/search/cdx (URL exacta; output=json; rang 2025–2026).
- Arquivo.pt CDX: https://arquivo.pt/wayback/cdx (URL exacta; output=json).
- Els errors invalid_redirect_url pertanyen al servei d'accés; no es pot inferir cap absència històrica.

## Estat que es preserva

**36 IDs provisionals:** 21×507, 14×627, 1×F57-507; 4 dates de publicació acreditades; 12/12 àmbits amb passada nominal; 14/48 controls parcials, 34/48 bloquejats i 0/48 PASS exhaustius. Sense canvis de cens en V90.

**Proper mètode:** CDXJ URL exacta i prefix amb client HTTP directe, desant resposta real, i si apareixen registres recuperar WARC per Range i validar PDF/SHA; continuar inventari P0 datat dels territoris amb 0 ID; anàlisi PDFResurrect/qpdf dels 13 PDF canviats pendent. Cap dada personal ni secret publicat.