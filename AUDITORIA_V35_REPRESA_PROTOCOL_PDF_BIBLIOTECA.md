# Auditoria V35 — represa efectiva del protocol històric de PDF de la Biblioteca

**Data d'execució:** 12/10/2026. **Objecte:** recuperar ofertes DC 507, 627, F57 i F87 publicades de 01/11/2025 a 28/02/2026. **Cobertura exigida:** 11 SSTT + CEB, 48 comprovacions territori-mes.

## 1. Document de referència original recuperat

`REFERENCIA_RECUPERACIO_HISTORICA_PDF_DC_507_627_F57_F87.md` (Biblioteca ChatGPT), juntament amb `DC Arxius Novembre2025 Febrer2026` (`README_ARXIUS_DC.md`, `recover_official_dc.py`, `recover-historic-offers.yml`, `probe_edubcn_history.py`, `probe-edubcn-history.yml`).

Aquesta investigació ja ha avançat més que el protocol original: 32 identificadors provisionals (19 507, 12 627 i 1 F57-507), davant els 28 de la seva auditoria V16. **Cap compte d'IDs no implica exhaustivitat**, continuem a 0/48 combinacions territori-mes certificades.

## 2. PADICAT: visor i API CDX, investigació real

**Portal:** https://padicat.cat/  
**Visor Wayback PADICAT:** https://wayback.padicat.cat/wayback/*/https://educacio.gencat.cat

El visor funciona per a una URL genèrica d'Educació; la pàgina de calendari de la consulta provada conté captures dels anys 2021–2023, però no del període estudiat per aquella URL **exacta**. El fitxer oficial amb nom datat de 07/11/2025 no s'ha pogut consultar per l'entrada del visor a la passarel·la usada.

**Endpoint CDX real, verificat en projectes independents:**
`https://wayback.padicat.cat/cdx?url=` — referenciat als repositoris públics [wasteback-machine](https://github.com/overbrowsing/wasteback-machine/blob/main/src/archives/padicat/padicat.js) i [pastpage](https://github.com/nabertronic/pastpage/blob/main/extension/src/core/providers/padicat.ts).

[Execució CDX V34 després de corregir el parser NDJSON](https://github.com/hectorPascualC/ustec-dc-historic-2025-2026/actions/runs/38304352558).

| URL exacta consultada amb rang 2025-11-01 — 2026-10-12 | HTTP | Captures retornades |
|---|---:|---:|
| PDF del Barcelonès datat 07/11/2025 | 200 | 0 |
| PDF amb nom estable de Vallès Occidental | 200 | 0 |
| PDF amb nom estable de Girona | 200 | 0 |
| Arrel `https://educacio.gencat.cat` | 200 | 0 |
| **Control:** `https://efes.cat` | **200** | **4** (23/11/2025, 2×20/02/2026, 05/10/2026) |

L'API respon amb `text/x-ndjson`. La **prova de control amb quatre captures** demostra que el parser actual processa dades reals, no que el portal estigui buit. Les quatre URL educatives han rebut **resposta buida per aquestes consultes exactes i en el rang concret**, NO una certificació que no existeixin captures amb altres variants `http:`, `www.`, altres URL o dates.

La prova Playwright sobre la portada de PADICAT ha fallat `ERR_CONNECTION_RESET` al runner; el **subdomini públic CDX** sí que respon. Per tant, prioritzar aquesta ruta CDX, no repetir la portada bloquejada.

Fitxers:
- [V32 navegador de la portada](exports_padicat/PADICAT_V32_PUBLIC_INTERFACE.json).
- [V34 indexador real NDJSON, cinc casos](exports_padicat/PADICAT_V34_CDX.json).
- [Codi V34](src/query_padicat_cdx_v34.py).

## 3. Anàlisi forense de versions incrementals dels 30 PDF actuals

[Execució V33 real](https://github.com/hectorPascualC/ustec-dc-historic-2025-2026/actions/runs/38304066452), seguint la part P2 del protocol de la Biblioteca i la documentació de PDFResurrect.

S'han tornat a descarregar **30 PDF oficials actuals** del llistat V24, llegint-ne l'estructura i comprovant candidats a versions anteriors amb PyMuPDF.

| Control | Resultat |
|---|---:|
| PDF actuals descarregats i validats | **30/30** |
| Amb múltiples marcadors `%%EOF` | **13** |
| Amb revisió prèvia que s'obre com a PDF llegible | **13** |
| Amb diferències de text entre revisió prèvia i actual | **0** |
| Revisions candidates a recuperació de textos antics 2025–2026 | **0** |

**Cautela important:** 13 revisions llegibles amb text igual no significa que les estructures binàries o els objectes PDF siguin idèntics; també poden reflectir signatures, metadades, anotacions o ajustos. I un PDF completament substituït al servidor no es pot recuperar per aquesta via. Per tant **no hi ha cap oferta històrica recuperada** en els tests, però tampoc no prova que les publicacions antigues no existissin.

- [JSON de les 30 comprovacions estructurals, sense contingut de persones](exports_forensic/PDF_V33_INCREMENTAL_REVISIONS.json).
- [Codi V33](src/forensic_pdf_incremental_v33.py).
- [PDFResurrect](https://github.com/enferex/pdfresurrect).

## 4. Següent prioritat sense repetir feina feta

1. **PADICAT CDX** amb variants **documentades** d'URL: `http`/ `https`, `www` només si era realment usat, fitxers amb nom datat del Barcelonès, prefixos de carpeta i fonts del curs 2025–26. No són zeros fins a cobrir variants i paginació.
2. **Common Crawl**: buscar registres CDXJ d'URL i, quan existeixin `filename`/`offset`/`length`, descarregar el **WARC per Range HTTP** i extreure el PDF autèntic, verificant SHA256 i contingut.
3. **Còpies documentals textuals**: completar l'inventari de noms nominals dels SSTT no barcelonins, sense sumar com a places diferents les republicacions.
4. **PDFResurrect** sobre documents que realment presentin **diferència de contingut** entre revisions, si apareixen en futures captures; no insistir cíclicament sobre els 30 PDF amb text inalterat.

## 5. Veredicte i privacitat

**PASS metodològic:** recuperat protocol de Biblioteca, visor i CDX reals de PADICAT verificats amb control de captures, parser NDJSON corregit; 30 PDF analitzats estructuralment sense difusió de dades personals.

**FAIL respecte al cens exhaustiu:** **cap nova oferta original recuperada**, cens provisional mantingut en **32 identificadors**, i **0/48** territori-mes certifiquen exhaustivitat. Els zeros de consulta CDX d'URL exacta no es confonen amb zeros històrics administratius.

No s'ha pagat cap servei nou, revelat cap credencial ni publicat el text o contingut dels PDF.
