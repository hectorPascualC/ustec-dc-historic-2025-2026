# Auditoria V173 — HTML arxivat de vies alternatives de provisió (22/10/2026)

Abast: difícil cobertura publicada 01/11/2025–28/02/2026, especialitats 507, 627, F57, F87; 11 SSTT + EDUBCN. Sense dades personals.

## Catalunya Central: prova real dins la finestra
Wayback CDX exacte (HTTP 200, from=2025, to=2026, sense collapse) per https://educacio.gencat.cat/ca/departament/serveis-territorials/catalunya-central/personal-docent/provisio-vacants-SPD/ :
- 2025-05-19 17:22:53 UTC, HTML 200, digest PWIAU2W3TCJCEH3QBN25OBLTRVVSOECT, length CDX 28190.
- 2025-11-27 09:08:57 UTC, HTML 200, digest YAYL2S6Y3DPAGH3IT2M23S2LUFX4KSFM, length CDX 36363.
Replay https://web.archive.org/web/20251127090857id_/https://educacio.gencat.cat/ca/departament/serveis-territorials/catalunya-central/personal-docent/provisio-vacants-SPD/ : HTTP 200, menció literal del curs 2025-2026, Data d'actualització 29.08.2025, sol·licituds fins a la seva cobertura. L'apartat Oferta de places no conté cap enllaç d'oferta en el HTML recuperat. L'apartat Resultat enllaça Adjudicacions-SEC-SPD.pdf i Adjudicacions-PRI-SPD.pdf.
CDX exacte del PDF Adjudicacions-SEC-SPD.pdf a /web/.content/home/departament/serveis-territorials/catalunya-central/personal-docent/Provisio-vacants-SPD/: HTTP 200 []; CDX prefix carpeta: HTTP 200, només formulari Solicituds-provisio.pdf capturat 2025-05-19 18:36:57 UTC, digest MNCZL6GXYPJIVMGEJCQSWANGKFNOAEKK, length CDX 1603104.
Una captura de 27/11/2025 NO acredita publicació d'una oferta el 27/11/2025. La data d'actualització de la pàgina és 29/08/2025. No afegir cap ID.

## Altres variants verificades
- Baix Llobregat /personal-docent/provisio-vacants-personal-docent/: CDX 200, HTML 200 capturat 2025-05-17 11:05:07 UTC, més HTTP 301 capturat 2026-01-28 17:24:07 UTC. El 301 no és oferta.
- Penedès /personal-docent/nomenaments-telematics/dificil-cobertura/procediment-provisio-especific/: CDX 200, HTML 200 2025-07-25 12:38:21 UTC, fora finestra.
- URL HTML ordinària de secundària Vallès Occidental i Penedès: CDX 200 []; variants http:// també []. Baix Llobregat: HTML 200 2025-07-25 13:12:14 UTC, replay HTTP 200, actualització 01/07/2025, enllaços PDF coneguts; fora de finestra.
- PDF PENDENTS_BLL-SEC-dificil-cobertura-oferta-vacants.pdf URL exacta: CDX 200 []. Negatives només per aquests endpoints consultats, no per tot el territori.

## Resultat
Prova nova: captura HTML oficial Catalunya Central 27/11/2025 que preserva la ruta alternativa i enllaços de resultats, sense convocatòria 507/627/F57/F87 datada dins finestra. 0 IDs nous, 0 dates de primera publicació acreditades, 0 PDF binaris històrics, 0 SHA-256 nou, 0 WARC Range.
Cens provisional 36 (21x507, 14x627, 1xF57-507) + 1 candidat separat; 4 registres EDUBCN amb data de portal (05/12/2025, 21/01/2026, 22/01/2026 x2). 12/12 territoris; 48 controls: 0 PASS / 14 PARTIAL / 34 BLOCKED, 0 exhaustius. Darrer run forense V91 39415173344 SUCCESS (V135); V92 qpdf/PDFResurrect 0/13 NO EXECUTAT.
Següent mètode: altres variants HTML amb actualització dins finestra, recuperar PDF original si disponible, comparar SHA i conciliar resultat-oferta. No repetir negatives sense nova hipòtesi.