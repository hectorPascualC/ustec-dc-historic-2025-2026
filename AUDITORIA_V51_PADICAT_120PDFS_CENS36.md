# AUDITORIA V51 — recuperació intensiva PADICAT, EDUBCN i PDF de tots els SSTT

**Tancament de la ronda:** 13/10/2026 (Europa/Madrid).  
**Finestra de les ofertes:** 01/11/2025–28/02/2026.  
**Especialitats objectiu:** 507, 627, F57, F87, combinacions documentades.  
**Cobertura territorial exigida:** 11 Serveis Territorials + EDUBCN, 48 blocs territori-mes.

## 1. Resultat consolidat i regla d'evidència

**36 identificadors únics al cens**: **21** 507, **14** 627, **1** F57-507. Corresponen als **32** casos provisionals ja reconstruïts a la V23 més **4** convocatòries noves originals de l'EDUBCN, recuperades de la resposta JSON pública capturada a PADICAT el **29/01/2026 22:46:30 UTC**.

**27** casos amb rastre d'oferta: **23** text d'oferta indexat (sense necessàriament binari immutable), **4** PDF originals públics íntegres verificats, amb captura JSON històrica; **9** casos només sustentats per resultats indexats. **0/48** blocs territori-mes es poden declarar exhaustius.

**No confondre:** (a) data `DATA` del JSON amb hora exacta de publicació, (b) captura PADICAT amb data de publicació, (c) una republicació amb una plaça nova, (d) un resultat amb convocatòria d'oferta original, ni (e) menció d'un codi dins un PDF amb una plaça d'aquella especialitat, si no figura al context d'especialitat.

## 2. Les quatre ofertes originals 507/627 de la fotografia EDUBCN del 29/01/2026

| ID canònic del registre oficial | Data `DATA` | Centre | Especialitat | Jornada contrastada al PDF | Evidència |
|---|---|---|---|---|---|
| `GENSEC_147` | 05/12/2025 | Institut Escola del Treball | 627 | **Sencera** | API PADICAT + PDF original de 3 pàgines + document resultat |
| `GENSEC2526_167` | 21/01/2026 | Institut Pedralbes | 507 | **Sencera** | API PADICAT + PDF original de 3 pàgines |
| `GENSEC_2526_145` | 22/01/2026 | Institut Tecnològic de Barcelona | 507 (ciberseguretat) | **Sencera** | API PADICAT + PDF original de 2 pàgines + document resultat |
| `GENSEC_2526_149` | 22/01/2026 | Institut Tecnològic de Barcelona | 627 | **No determinada** | API PADICAT + PDF original de 3 pàgines |

En tres documents, l'extractor de condicions original identifica explícitament «jornada sencera» prop de l'apartat de jornada. Al quart, les comprovacions no autoritzen afirmar que sigui sencera ni parcial. La data de finalització específica tampoc no queda certificada per a tots quatre.

URL originals:
- `GENSEC_147`: https://www.edubcn.cat/rcs_gene/seleccio/GESEC2526_147_INS_ESCOLA_DEL_TREBALL_627.pdf
- `GENSEC2526_167`: https://www.edubcn.cat/rcs_gene/seleccio/GESEC2526_167_INS_PEDRALBES_507_INFORMATICA.pdf
- `GENSEC_2526_145`: https://www.edubcn.cat/rcs_gene/seleccio/GENSEC_2526_145_Inst_Tecnologic_507.pdf
- `GENSEC_2526_149`: https://www.edubcn.cat/rcs_gene/seleccio/GENSEC_2526_149_Inst_Tecnologic_627.pdf

**Dues variants de nom no són dues vacants addicionals:** `GESEC2526_147` del nom de fitxer correspon a `GENSEC_147` del registre API; `GESEC2526_167` correspon a `GENSEC2526_167`. El codi, el centre, l'especialitat i el **SHA-256 binari** dels originals han estat reconciliats. El detector inicial V45 les havia marcat provisionalment com a possibles noves perquè comparava noms en lloc de SHA; la correcció s'ha executat, i ara dona **0 falses novetats**.

## 3. Inventari de PDF històrics PADICAT: tot el directori real

**Directori públic arxivat:** `https://www.edubcn.cat/rcs_gene/seleccio/` (29/01/2026).

- **252** registres de l'índex PADICAT.
- **248** registres de PDF amb estat HTTP original 200; alguns són convocatòries, altres resultats, llistes o documents administratius. **248 NO vol dir 248 places DC.**
- D'aquests, **33 PDF originals GENSEC/GESEC**, exclosos els fitxers explícits RESULTAT, han estat **descarregats del reproductor PADICAT i validats**, **33/33**.
- **Només 4 dels 33** presenten una especialitat objectiu documentada 507/627. Tots quatre ja incorporats al cens. No hi ha noves places addicionals dins aquest subgrup.
- Fora de GENSEC/GESEC, l'índex conté **190 PDF** no identificats per aquest prefix sense marca explícita de RESULTAT, entre ells molts processos administratius diferents. **87** documents seleccionats com a no-resultat ni llista/resolució pel nom s'han descarregat de PADICAT i llegit correctament: **87/87**; cap no ha mostrat un perfil explícit 507/627/F57/F87 en el context d'especialitat dels **primers 7 fulls** llegits. No és una certificació d'absència a la resta dels documents, en imatges escanejades o més endavant al PDF.
- **120 PDF binaris històrics diferents revisats directament aquesta ronda** (33 + 87), sense reproduir ni publicar dades personals.

Fitxers:
- [Índex amb 48 URLs GENSEC/GESEC, inclosos alguns RESULTAT](exports_padicat/PADICAT_EDUBCN_V44_PDF_DIRECTORY.json).
- [Comprovació 33 PDF originals GENSEC/GESEC, SHA256 i codis](exports_padicat/EDUBCN_PADICAT_V45_ALL_PDFS.json).
- [Classificació dels 248 PDF del directori sencer](exports_padicat/EDUBCN_PADICAT_V46_FULL_DIRECTORY.json).
- [87 PDF no codificats inspeccionats sense text personal](exports_padicat/EDUBCN_PADICAT_V47_NONCODED_PDFS.json).
- [Prova directa de 6 PDF (4 ofertes + 2 resultats)](exports_padicat/EDUBCN_V44_OFFERS_RESULTS_PDF.json).
- [Revisió automatitzada de condicions dels 4 PDF](exports_padicat/EDUBCN_PDF_CONDITIONS_V43.json).
- [Fotografia ca/es i octubre comparades](exports_padicat/EDUBCN_V43_ARCHIVE_COMPARISON.json).

**Una comprovació històrica addicional:** l'API d'EDUBCN capturada **també en castellà** el 29/01/2026 conté els mateixos quatre codis objectiu. La captura del **04/10/2026** és una fotografia de llistat diferent i no recupera els registres antics dins la finestra. Això demostra la importància de preservar versions originals i no consultar només la llista actual.

## 4. Pistes per als altres SSTT i límits del rastreig PADICAT

- V36 i V48: PADICAT ha estat consultat per noms exactes, variants HTTP/HTTPS, arbres territorials, i **nou variants de dominis oficials de Gencat**, `educacio.gencat.cat`, `ensenyament.gencat.cat` i `documents.espai.educacio.gencat.cat`.
- La consulta general de l'arrel d'Educació va tornar **180 registres i es va truncar**; els prefixos específics de la carpeta de PDF de difícil cobertura dels SSTT no van retornar registres.
- La V50 inicial emprava una sintaxi incorrecta de filtre (`url:.*`). S'ha corregit seguint la documentació oficial de **pywb** amb `~url:.*`. **Les proves positives funcionen**: control 300 registres d'educacio.gencat.cat (truncat), 26 d'ensenyament.gencat.cat i 3 de documents.espai.educacio.gencat.cat. Les cerques filtrades `~url:.*dificil.*`, `~url:.*nomenaments.*` i `~url:.*vacants.*` han retornat **0 captures indexades per aquells dominis en el rang provat**. **Això és un resultat vàlid de l'índex PADICAT, no una prova que no hi hagués convocatòries publicades ni captures en altres dominis o rutes**. [Auditoria amb controls](exports_padicat/PADICAT_V50_TERRITORIAL_FILTERS.json).
- Common Crawl V37 (12 consultes sota límits) no va retornar metadades amb `filename/offset/length` i per tant no s'ha pogut recuperar cap nou WARC per Range.
- Les fonts oficials vives dels **11 SSTT + EDUBCN** ja havien estat consultades en V24: **37 pàgines HTTP 200 i 30 PDF actuals**, però els actuals no proven l'històric.
- La forense V33 havia inspeccionat aquests 30 PDF actuals: **13 amb múltiples EOF i revisions internes llegibles**, cap amb text canviat que recuperés una oferta 2025–2026.

## 5. Estat territorial i documental

| Àmbit | Identificadors provisionals |
|---|---:|
| Barcelonès (SSTT) | 17 |
| Baix Llobregat | 9 |
| Lleida | 3 |
| Vallès Occidental | 2 |
| Penedès | 1 |
| Consorci d'Educació de Barcelona (EDUBCN) | **4** |
| Alt Pirineu i Aran, Catalunya Central, Girona, MVO, Tarragona i Terres de l'Ebre | 0 recuperats, **NO zero real** |
| **Total** | **36** |

El cas d'Escola del Treball (`GENSEC_147`, desembre de 2025) queda **inclòs al cens general**; l'exclusió personal anterior de `GENSEC_2627_034` és un **altre identificador/curs**. L'exclusió de Barcelona ciutat només és aplicable a la **shortlist**, no a una recerca exhaustiva de tot Catalunya.

## 6. Lliurables i veredicte

- [Cens V49, 36 identificadors, 3 jornades d'EDUBCN corroborades](cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V49_36IDS.csv).
- [Matriu territorial actual de 12 àmbits](cens/MATRIU_TERRITORIAL_V51_36IDS.csv).
- [Correspondència entre els dos codis divergents de PDF i API](cens/EDUBCN_2025_26_CANONICAL_ID_CROSSWALK.csv).

**PASS** per reconstruir el cens provisional fins als 36 identificadors, verificar **4 noves ofertes originals**, estudiar **120 PDF històrics** amb control d'especialitat i depurar els àlies.

**FAIL respecte a l'exhaustivitat general**: no és possible certificar tots els PDF de 2025–2026 i totes les places desertes, retirades o republicades dels 48 blocs. Els documents no indexats dels altres SSTT continuen sent la principal limitació.

**No** s'han fet pagaments nous, difós noms d'adjudicataris, emmagatzemat contingut dels seus PDF en públic, ni qualificat cap absència de resultats d'internet com una absència real de convocatòries.
