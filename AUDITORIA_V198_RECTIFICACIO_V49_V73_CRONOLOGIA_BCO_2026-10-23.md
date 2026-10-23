# Auditoria V198 — rectificació censal i cronologia de fotografies nominals (23/10/2026)

Abast: ofertes DC 507/627/F57/F87 i combinacions acreditades publicades entre 01/11/2025 i 28/02/2026, 11 SSTT + EDUBCN. Aquest registre no tracta el monitor 2026–2027.

## Correcció efectiva

S'ha contrastat `cens/REPUBLICACIONS_BCO_DESEMBRE2025_GENER2026_V21.csv` (blob `5e97d215733cbe732b3d09d5c5c65d885a46e0bc`) amb les files de `19297807` dels censos V49 i V73. V21 acredita una **fotografia nominal coneguda** de 09/01/2026 (507; termini 11/01; inici previst 12/01; fi prevista 29/01); V49/V73 conservaven com a primera la fotografia 16/01 (termini 18/01; inici previst 20/01; mateixa fi). No s'acredita ni la primera data de publicació ni el moment exacte de republicació.

La fila `19297807` s'ha corregit als censos V49 i V73, conservant la segona fotografia a les observacions. Els dos CSV s'han rellegit: **36 files cadascun**, `primera_evidencia=09/01/2026`, `primer_fitxer_nominal_verificat=2026-01-09`, sense introduir dates de publicació certificades. Blobs verificats V49 `1f89a91e42cc06c32bda59c2e07246023b2ee49d`; V73 `db919322a6d259dbcf96ce182cda9201b9538391`.

El nou `cens/V198_CRONOLOGIA_FOTOGRAFIES_BCO_19297807_19303622.csv` conserva **quatre observacions** (dues per ID) i separa data del nom del PDF, termini, inici, fi, font i estat de corroboració. Blob `dcc8fb0c6da08e398de8041f7518882cdeba853f`. La fotografia 16/01 de `19303622` continua **pendent de prova primària V3**; V22 documenta la del 23/01 (p.14/22), però no demostra absència el dia 16. No s'ha canviat la primera evidència de `19303622`.

## Controls i límits

GitHub verificat: correcció V73 commit `ac82b565004c1c7db318cfbd02d3f3a9316b0c21`; correcció V49 commit `506e6ab8bbc86afc496c9f4ec341c5d75a2882eb`; cronologia commit `06153c4b09a087956447096d8915914cf882fcc2`. V87 conserva 48 files i les quatre Barcelonès ja corregides a V195. Cerques independents de PDF 09/01 i 16/01 no han retornat binari antic; la URL oficial 16/01 és 404 actual i el cercador conserva un fragment de l'oferta; 404 no és absència històrica.

No hi ha nou ID, nova data acreditada de primera publicació, PDF històric descarregat, hash SHA-256 de PDF ni WARC Range. No s'ha executat V92: **0/13**. Darrer run forense conegut V91 `39415173344` (històric, no executat en aquesta passada).

Cens **36 IDs provisionals** (21×507, 14×627, 1×F57-507) + 1 candidat separat; **4 registres EDUBCN amb data de portal** (05/12/2025, 21/01/2026, 22/01/2026 ×2), no necessàriament primera publicació. **12/12 territoris; 48 controls: 0 PASS / 14 PARTIAL / 34 BLOCKED; 0 exhaustius**. Veredicte **PARTIAL**.

Següent via: obtenir l'evidència V3 o HTML/PDF íntegre 16/01 per a `19303622`, PDF 09/01 complet amb SHA, continuar els nou resultats sense oferta i executar V92 sobre els 13 PDF amb validació dels SHA originals en runner autoritzat.
