# Auditoria V135 — 20/10/2026 13:33 Europe/Madrid

Abast exclusiu: ofertes DC publicades 01/11/2025–28/02/2026, especialitats 507/627/F57/F87, 11 SSTT + EDUBCN. Aquesta auditoria no és el monitor 2026–2027.

## Progrés real verificat — GitHub

- Commit de correcció V91 **`423b075d8b8772a7a6a295a0cdae08e418c3b284`**: el generador `src/forensic_13_changed_v91.py` ara conserva `old_sha256` (V24) i `sha256_v86` (V86), amb validació de 13 URL úniques i hashes SHA-256 de 64 dígits.
- Run real **39415173344**, `push`, 20/10/2026 11:28:17 UTC, conclusió **success**; 9/9 passos del job en verd. És **V91/PyMuPDF, NO qpdf/PDFResurrect**.
- Artefacte públic de metadades anonimitzades **12261815486**, `v91-anonymized-pdf-metadata`, ZIP SHA-256 **`e1c9c92ba8782e022280bed10e64008effe6bcc580db13a6785825d2f7586279`**; dues entrades: CSV d'entrada (13 files, 4 camps incloent dos SHA de referència) i JSON de resultats.
- Lectura del JSON: **13/13 PDF descarregats HTTP 200**, **7/13** amb múltiples marcadors EOF, **6** revisions anteriors vàlides obertes per la tècnica V33, **1** revisió amb text diferent (PDF d'oferta de Tarragona), **0** candidats 2025–2026 amb els codis objectiu segons l'extractor. No són resultats de PDFResurrect.
- **Nova dada temporal important:** només **4/13** SHA actuals coincideixen amb `sha256_v86` (Girona, Penedès i els dos PDF de Tarragona); **9/13 han tornat a canviar des de V86**. Cap SHA actual coincideix amb V24. Això impedeix presentar el lot actual com si fos exactament el lot V86; cal conservar la relació de hashes i registrar cada data de descàrrega.
- La revisió de Tarragona amb text diferent no conté cap referència 2025 segons el JSON. **No acredita cap oferta històrica nova ni cap data de primera publicació**.
- El patch V92 que comparava SHA, examinava totes les pàgines i parsejava `pdfresurrect -q` fou rebutjat pel control de seguretat de l'eina; **cap commit V92, 0/13 qpdf/PDFResurrect real**. No s'ha intentat eludir el bloqueig.

## P1 — Comprovacions de captures diferenciades

- Wayback CDX, consulta real **prefix** de `Barcelones-SEC-dificil-cobertura-oferta-vacants_`, sense `collapse`, rang captures 2025-11 a 2026-10: **1 fila HTTP 200**, captura `20260105180042` del PDF `_05122025.pdf`, digest CDX `ZXXVBFRAVQJPGJ64SMCMYGGDJU2UCTIN`, ja conegut V126–V127. La consulta no descobreix cap segon PDF; això **no** acredita absència històrica.
- Wayback CDX **exacte** de `PEN-SEC-dificil-cobertura-oferta-vacants.pdf` (rang 2025–2026): resposta JSON `[]` en aquesta consulta; no és una prova universal d'absència.
- Common Crawl CDXJ exacte de la mateixa URL Penedès: quatre índexs **2025-47, 2025-51, 2026-04, 2026-39** han retornat `No Captures found` (limitació d'aquests quatre índexs); **2026-21** ha respost **504**, i prefix de carpeta a **2026-39** també **504**. Aquests dos errors són **BLOCKED**, no zero captures. Sense registre CDXJ amb `filename/offset/length`, **0 extraccions WARC possibles** d'aquestes consultes.

## Control final i següents passos

Cens provisional **36 ID** (21×507, 14×627, 1×F57-507) + 1 candidat separat. **4 registres EDUBCN amb data de portal** (05/12/2025, 21/01/2026, 22/01/2026 ×2; 3 dies únics). Cobertura territorial 12/12; **48 controls: 0 PASS, 14 PARTIAL, 34 BLOCKED**; 0 exhaustius. Les proves forenses V91 són transversals, no tanquen cap cel·la mensual.

**Següent via:** V92 real qpdf/PDFResurrect en runner autoritzat i amb validador de recompte; preservar els 9 canvis de SHA posteriors a V86; continuar P0 de les nou ofertes originals no localitzades i P1 en altres índexs/CDX. **Veredicte: PARTIAL; V91 reparat i executat, V92 pendent.**