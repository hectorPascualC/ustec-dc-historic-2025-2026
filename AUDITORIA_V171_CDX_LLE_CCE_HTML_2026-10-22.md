# Auditoria V171 — Wayback exacte/prefix i HTML Lleida / Catalunya Central (22/10/2026)

Abast: DC 507, 627, F57, F87; publicacions 01/11/2025–28/02/2026; 11 SSTT + EDUBCN. No dades personals.

## Proves reals P0/P1

Consultes live Firecrawl `maxAge=0`, proxy stealth, al CDX de Wayback, sense collapse, `from=2025&to=2026`, HTTP 200 en totes sis consultes:

1. PDF d'OFERTA exacte `LLE-SEC-dificil-cobertura-oferta-vacants.pdf` (Lleida): `[]`.
2. PDF d'OFERTA exacte `CCE-SEC-dificil-cobertura-oferta-vacants.pdf` (Catalunya Central): `[]`.
3. Prefix de carpeta oficial de secundària Lleida: 1 registre PDF `Solicitud_dificil_cobertura.pdf`, captura **2025-05-19 18:28:14 UTC**, estat arxivat 200, digest CDX `CXFAHFSV5MEZMR27NBTWS6MUNAJR5UTX`, longitud CDX 1635171. **Formulari de sol·licitud, fora de finestra; NO oferta 507/627/F57/F87**.
4. Prefix de carpeta oficial de secundària Catalunya Central: `[]`.
5. HTML oficial de secundària Lleida, URL exacta: 1 registre `http://...` amb captura **2025-04-26 19:02:50 UTC**, estat **301** (redirecció), no HTML amb contingut d'ofertes; fora de finestra.
6. HTML oficial de secundària Catalunya Central, URL exacta: `[]`.

Les respostes `[]` són negatives **només per URL/prefix i CDX consultats**, no zero publicacions ni absència en altres arxius. La captura de 2025-05 i el 301 de 2025-04 no acrediten publicacions dins el període.

P2: enllaços oficials HTML actuals verificats directament a PDFs d'oferta LLE (6 pàgines, inclou 507 `2026/SEC/089`) i PEN (11 pàgines, 2026-27), més CCE (6 pàgines). **No** són originals 2025-26 ni permeten sumar IDs. Fonts:
- https://educacio.gencat.cat/ca/departament/serveis-territorials/lleida/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/
- https://educacio.gencat.cat/ca/departament/serveis-territorials/catalunya-central/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/
- https://educacio.gencat.cat/ca/departament/serveis-territorials/penedes/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/

## Estat i límits

0 IDs nous; 36 provisionals (21×507, 14×627, 1×F57-507) + 1 candidat separat; 4 registres EDUBCN amb data de publicació del portal (05/12/2025, 21/01/2026, 22/01/2026 ×2), no dates de primera publicació absoluta. 12/12 territoris; 48 controls: **0 PASS / 14 PARTIAL / 34 BLOCKED**, 0 exhaustius. V91 run 39415173344 SUCCESS (segons V135); **V92 qpdf/PDFResurrect no executat, 0/13**. Cap nou SHA PDF ni WARC Range. HEAD abans d'aquesta auditoria `330b0cac3d12011fc8ebf0ede16305a1efc785cb`.

Proper mètode: Wayback/PADICAT per variants HTML amb noms antics datats i fonts independents dels territoris encara sense ID; executar V92 només amb runner qpdf/PDFResurrect i contrast de SHA V24/V86. No repetir aquests CDX exactes sense una nova hipòtesi.
