# AUDITORIA V74 — Prova de la semàntica de DATA i cens integrat V73

**Data de comprovació:** 13/10/2026. **Interval de la investigació:** ofertes 507 / 627 / F57 / F87 publicades del 01/11/2025 al 28/02/2026, onze SSTT + Consorci d'Educació de Barcelona.

**Protocol metodològic original:** `REFERENCIA_RECUPERACIO_HISTORICA_PDF_DC_507_627_F57_F87.md` (Biblioteca, v1.0). Distingir PDF d'oferta, resultat, captura d'arxiu, data real de publicació, republicacions, dates d'inici i fi.

## 1. NOVA PROVA DOCUMENTAL: la data de l'API EDUBCN és la data de publicació mostrada pel portal

En la V70 hem recuperat:
1. HTML oficial d'EDUBCN del **29/01/2026 a les 22:46:29 UTC**, captura PADICAT: `https://wayback.padicat.cat/20260129224629id_/https://www.edubcn.cat/ca/professorat_i_pas/seleccio_rrhh/dificil_cobertura` (**HTTP 200**, SHA256 del cos HTML `7238f2109786ba37bcb16c6adb57fa1f79e54f18f5a7a07910c43922b485c4e7`).
2. API de dades pública del mateix minut, **29/01/2026 a les 22:46:30 UTC**, `https://wayback.padicat.cat/20260129224630id_/https://www.edubcn.cat/pdc_rest/convocatories/ca`. JSON original 49 files i quatre target 507/627 ja documentats en V41.
3. Aplicació JavaScript referenciada per l'HTML històric, `https://wayback.padicat.cat/20260129224629id_/https://www.edubcn.cat/pdc/js/app.bundle-v05.js`, arxivada a PADICAT **aquell dia**. Les V71/V72 verifiquen lectura HTML + JS i recuperen al bundle original el text de la plantilla pública:

   `Data de publicació: {{ctrl.convocatoria.DATA | date: ...}}`

Aquest **vincle directe del camp `DATA` amb la interfície que diu «Data de publicació»** permet certificar el significat de la data de la fitxa del portal, cosa que no podíem acreditar a V68. La plantilla és **un fitxer JS efectivament arxivat el 29/01**, no una deducció del JavaScript vigent el 2026-10. La validació automatitzada V73 obliga a trobar el text i la unió `convocatoria.DATA` a la versió arxivada abans de modificar cap fila.

## 2. Les quatre ofertes i les seves dates al portal

| Codi oficial | Especialitat | Centre | Data publicació a l'API/portal (provada) | Jornada original PDF | Resultat |
|---|---|---|---|---|---|
| `GENSEC_147` | 627 | Institut Escola del Treball | **05/12/2025** | Sencera | Adjudicació documentada |
| `GENSEC2526_167` | 507 | Institut Pedralbes | **21/01/2026** | Sencera | Sense resultat identificat a la captura 29/01 |
| `GENSEC_2526_145` | 507 | Institut Tecnològic de Barcelona | **22/01/2026** | Sencera | «Alta titular» |
| `GENSEC_2526_149` | 627 | Institut Tecnològic de Barcelona | **22/01/2026** | **0,25** | Sense resultat identificat a la captura 29/01 |

**Advertència d'auditoria:** les dues ofertes de l'Institut Tecnològic conserven PDF amb terminis inicials de **03/12/2025** (507) i **12/12/2025** (627), malgrat que la fitxa arxivada de l'API mostra «Data de publicació» el 22/01/2026. Això **no prova que fossin publicades per primer cop al gener**: pot haver-hi una publicació prèvia, pròrroga o republicació. El camp certificat és la data mostrada pel portal arxivat el 29/01, **no la primera data de difusió històrica**.

Per a la 627 `GENSEC_2526_149`, el PDF original conté una **fi 31/08/2025** incompatible amb la fitxa posterior. No es pot considerar una fi real corroborada. La 507 `GENSEC_2526_145` té resultat **«Alta titular»**, no «deserta». No es pot inferir fora de borsa dels altres resultats.

## 3. Cens material consolidat: V73

Cens de treball V49 de 36 IDs preservat integralment en una **versió nova** sense esborrar les evidències d'origen:

- [**CSV V73 integrat: 36 ID amb dates acreditades**](cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V73_36IDS.csv).
- [**Control JSON V73: proves, quatre dates i conciliació**](exports_padicat/EDUBCN_V73_PUBLICATION_PROOF_AND_CENSUS_QA.json).
- [Script reproduïble V73](src/consolidate_census_v73_publication_dates.py).
- [Prova arxivada de JS i patró DATA V72](exports_padicat/EDUBCN_V72_ARCHIVED_JS_PUBLIC_API_ROUTES.json).
- [Captures HTML/REST exactes V70](exports_padicat/PADICAT_V70_SSTT_HTML_HISTORIC_LINKS.json).
- [Originals i resultats PDF V52](AUDITORIA_V52_EDUBCN_RESULTATS_JORNADES_2026-10-13.md).

**Auditoria interna del nou fitxer:**

- **36 de 36** identificadors originals V49 conservats.
- **21 × 507, 14 × 627, 1 × F57-507.**
- **4/36** registres amb `data_publicacio_certificada` del portal (cap acreditació de primera aparició absoluta).
- **32/36** encara sense publicació exacta certificada.
- Correcció de **0,25** jornada per a `GENSEC_2526_149`.
- Resultats i anomalies de V52 integrats en camps complementaris sense substituir fraudulentament la data real de fi.

## 4. Limitacions territorials i l'estat del període

La V70, un cop corregits els paràmetres `matchType=exact` i `output=json`, ha obtingut **13/13 respostes HTTP 200** per als onze HTML territorials més la pàgina i l'API EDUBCN. Hi ha **3 captures d'HTML EDUBCN** i **2 de l'API**. Les onze URL exactes HTML dels SSTT no retornen captures per aquest arxiu, però això **no exclou altres rutes o arxius**.

En el corpus de **48 combinacions territori × mes** de V69, **cap mes ni territori està tancat com a exhaustiu**. La V74 millora la cronologia en dos mesos del Consorci: desembre de 2025 (un cas) i gener de 2026 (tres casos), però **no n'acredita l'exhaustivitat**. V69 continua vigent com a mapa de cobertura parcial/bloquejada; només la xifra V68 `0/36 dates` ha estat **superada per V73**.

**Resultat de la ronda:** **0 identificadors nous**, **4 dates de publicació de portal provades**, **36 identificadors provisionals**, **0/48 blocs exhaustius**.

**Privacitat:** no s'han publicat noms, dades de barem, identitats ni dades de contacte de docents o aspirants.

**Veredicte:** **PASS** en prova arxivística de significat de DATA, cadena JS+HTML+API, CSV integrat i correccions V52; **PENDENT** trobar dates de primer anunci/possibles republicacions i completar els SSTT; **NO ASSOLIT** cens català exhaustiu.

## 5. V75 — forense de creació PDF abans de la publicació del portal

L'auditoria [V75](exports_padicat/EDUBCN_V75_PDF_ORIGINAL_CREATION_DATES.json) ha fet un control independent sobre els quatre PDF de la captura de gener.

- **4/4** PDF originals descarregats correctament i **SHA256 idèntic** als hash originals V41.
- **4/4** URL exactes dels PDF tenen captura pròpia a PADICAT del **29/01/2026, aproximadament a les 23:22 UTC**, amb un PDF de reproducció HTTP 200 i SHA256 concordant.
- El PDF `GENSEC_2526_145` (507 ITB) conté `creationDate = D:20251201141851+01'00'`, data del fitxer **01/12/2025**, i termini inicial **03/12/2025**. El portal arxivat mostra publicació **22/01/2026**.
- El PDF `GENSEC_2526_149` (627 ITB) conté `creationDate = D:20251210150325+01'00'`, data del fitxer **10/12/2025**, i termini inicial **12/12/2025**. El portal arxivat mostra publicació **22/01/2026**.
- `GENSEC_147` (627 Escola del Treball): creació PDF **05/12/2025**, publicació portal **05/12/2025**.
- `GENSEC2526_167` (507 Pedralbes): creació PDF **21/01/2026**, publicació portal **21/01/2026**.

**Conclusió forense limitada:** dos documents PDF de l'ITB **porten dates internes de desembre**, concordants amb els terminis interns de desembre, però l'API els presentava amb data de publicació **22/01/2026**. Això justifica **prioritzar la cerca de les primeres convocatòries o republicacions de desembre de 2025** per aquests dos codis. No podem atribuir una data inicial pública exacta a partir de les metadades: `creationDate` pot no coincidir amb el primer moment de difusió, i cap arxiu anterior dels mateixos PDF ha estat recuperat en aquesta comprovació.

**Auditoria final de la ronda:** quatre dates del portal acreditades, quatre PDFs històrics SHA256 verificats i quatre metadades temporals contrastades, **0 identificadors nous**, cens provisional **36**, **0/48** blocs territori-mes exhaustius.
