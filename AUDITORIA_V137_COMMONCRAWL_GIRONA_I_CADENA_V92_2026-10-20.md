# Auditoria V137 — 20/10/2026 (Europe/Madrid)

Abast: publicacions DC 507/627/F57/F87 entre 01/11/2025 i 28/02/2026; 11 SSTT + EDUBCN. No és AUTO-PUBLIC.

## P1: Common Crawl Girona — índexs nous
Consulta exacta de `GIR-SEC-dificil-cobertura-oferta-vacants.pdf` amb `output=json`, via Firecrawl live (`maxAge=0`), 20/10/2026:
- CC-MAIN-2026-08: HTTP 504, BLOCKED.
- CC-MAIN-2026-12: HTTP 504, BLOCKED.
- CC-MAIN-2026-17: HTTP 404, resposta literal `No Captures found for: [URL exacta]`, NEGATIVE només en aquest índex.
- CC-MAIN-2026-17, prefix del directori Girona: HTTP 504, BLOCKED.
- Control `https://example.com/` en CC-MAIN-2026-17: HTTP 504, BLOCKED. No és una validació positiva del servei.
Cap registre CDXJ amb `filename/offset/length`; cap WARC Range. Els 504 NO són zero captures.

## P2: revisió de la cadena V91→V92
- GitHub `main` HEAD verificat: `d60b81b8a26a0c1416e4ab9b26e7e16d5a893d26`. Últim run forense verificat: V91 `39415173344` success, 13/13 descàrregues (PyMuPDF).
- El directori `.github/workflows/` no conté workflow V92. Existeixen `src/forensic_qpdf_pdfresurrect_v92.py` i V91, però el codi V92 actual només examina 40 pàgines, cerca 2025, no valida SHA V24/V86 i pot exportar `output_excerpt` de subprocessos.
- `pdfresurrect` 0.23-2 està disponible a Ubuntu 24.04 `universe`; la instal·lació al runner és viable, no verificada en execució real. Fonts: `https://packages.ubuntu.com/noble/pdfresurrect` i `https://manpages.ubuntu.com/manpages/resolute/man1/pdfresurrect.1.html`.
- Intent de patch V92 per comparar SHA, llegir totes les pàgines, separar PDF sense text i parsejar `-q`: rebutjat per `OpenAI's safety checks`. Cap commit nou V137, cap run V92.


## P1 addicional: Arquivo.pt textsearch i CDX
Consultes públiques verificades amb Firecrawl live, 20/10/2026:
- `q="GIR-SEC-dificil-cobertura-oferta-vacants"`: HTTP 200, `estimated_nr_results=0`, `response_items=[]`. Només absència en aquesta consulta textual, no absència d'arxius.
- `q="F57-507"&siteSearch=educacio.gencat.cat`: HTTP 200, 0 coincidències.
- `q="difícil cobertura" "507"&siteSearch=educacio.gencat.cat`: HTTP 200, 1 resultat amb `tstamp=20230327104450` sobre requisits de borsa; **exclòs** (2023, no és oferta DC de la finestra).
- CDX exacte de Girona via `/wayback/cdx`: recuperació bloquejada pel lector (no es pot interpretar com a zero captures).
- Control de CDX `url=expresso.pt`: HTTP 200 amb registres reals, que verifica el format CDX d'Arquivo.pt; no és evidència de Catalunya.

## Veredicte
PARTIAL; cap nova oferta ni data acreditada. Cens: 36 IDs (21×507, 14×627, 1×F57-507) + 1 candidat; 4 registres EDUBCN amb data de portal (05/12/2025, 21/01/2026, 22/01/2026 ×2), 3 dies únics. 12/12 àmbits, 48 controls: 0 PASS / 14 PARTIAL / 34 BLOCKED. Pròxim: desplegar workflow V92 després d'autoritzar publicació, executar 13 PDFs amb qpdf/PDFResurrect i reprendre CC exact/prefix amb transport funcional.