# AUDITORIA V89 — Comprovació estricta del protocol de Biblioteca i rectificació V88

**Data:** 15/10/2026. **Objectiu:** determinar què s'ha fet, què és insuficient, què no s'ha executat i què falta per recuperar PDF de difícil cobertura 507, 627, F57 i F87 publicats entre el 01/11/2025 i el 28/02/2026 a tots els SSTT i EDUBCN.

**Protocol normatiu:** fitxer personal de Biblioteca `REFERENCIA_RECUPERACIO_HISTORICA_PDF_DC_507_627_F57_F87.md`, v1.0 (12/10/2026), seccions 3–9, llegit de nou expressament. El fitxer privat no es copia al repositori públic.

## RECTIFICACIÓ OBLIGATÒRIA DE V88

L'expressió «passada final / completa» a V88 **només descriu que els 11 SSTT i EDUBCN tenen fonts visitades i un estat**. **NO** acredita haver executat totes les vies de recuperació de PDF històrics per cada territori i mes.

V87 va **heretar** les 48 classificacions de V69 (`14 PARTIAL` i `34 BLOCKED`) i va confrontar els resultats amb 30 PDF **actuals**, no amb 48 corpus mensuals originals. Una fila de V87 **no** és una auditoria amb les 8 fases completades per aquell territori i mes. `0/48 PASS`. No donar l'objectiu per completat.

## Protocol original: comprovació mètode per mètode

| Via (manual) | Què consta executat | Què **NO** s'ha pogut acreditar / falta |
|---|---|---|
| P0. Inventari complet de PDF originals, ofertes/resultats, fitxers datats | V24: **30 PDF públics actuals** dels **11 SSTT**, 26 de secundària i 4 de descoberta PFI. BCO V22/V61: **11 lots amb nom datat**, 17 IDs, 60 aparicions; V77: **18 URL hipotètiques** de sis setmanes absents, tots 404 | No s'han recuperat tots els PDF **originals de 2025-26** ni l'inventari immutable de noms/rutes datades per cadascun dels 11 SSTT. Comprovar especialment altres rutes PFI/FP, dates setmanals absents, adjunts i HTML antics. |
| P0. Fragments indexats i múltiples motors | 23 IDs amb rastre d'oferta indexada, 9 només resultats, 4 PDF originals EDUBCN; tests BCO/BLL/LLE/GIR/TAR i tercers | Falta **registre literal i complet per consulta**, amb motor, URL, hora UTC i fragment per tots els territoris/mesos, i rescatar els snippets no conciliats. No convertir dates d'inici/resultat o de nom del PDF en data de publicació. |
| P1. Wayback CDX | `exports_official/ARXIU_CONSULTES.csv`: **13 exactes i 11 de prefix**, cap consulta d'aquest lot amb resposta útil. Reintent V32 `RESUM_CDX_65S.json`: **3 URL, 3 HTTP 503**, 0 captures | **No esgotat.** Falta una passada efectiva i traçable **exacte+prefix**, variants històriques reals, rang de captures anterior i posterior al període, i resultat diferenciant 200/404/403/429/5xx; el reintent V32 usava `collapse=digest`, de manera que no és un inventari cru sense col·lapse com indica el manual. Tots els 503 són BLOCKED, **mai 0 captures**. |
| P1. PADICAT | V36/48/50/58/70: proves exactes, prefixos, dominis alternatius, filtrar URL; EDUBCN PADICAT gener+octubre: **557 URL PDF úniques** revisades, **4 ofertes originals** amb data de portal corroborada | Els resultats del CDX territorial no van donar originals SSTT dins la finestra; manca recuperar HTML alternatiu i revisar variants de rutes **antigues**, mensualitats sense captures, i fonts PFI. La cobertura d'EDUBCN de gener/octubre **no cobreix febrer**. |
| P1. Common Crawl CDXJ + WARC | V37: **12 consultes d'índex**, **0 registres CDXJ** i per tant **0 extraccions WARC**. V62: 13 consultes BCO, errors 5xx reintentats V63: 12 respostes 404 d'índex concret, 1 bloquejada. V66: **3/30** consultes executades, 3 errors 502/504. V67: **7/12**, 6 errors i 1 HTTP 404. | **No esgotat.** Moltes consultes planificades **NO EXECUTADES**; només subconjunt d'índexs 2025/26. Cercar per PDF exacte i prefix en **més rastreigs**, altres noms de fitxer i possiblement consultes sobre índex/col·lecció alternatives. Si CDXJ retorna `filename/offset/length`, recuperar WARC via HTTP Range i separar capçalera/cos amb `warcio`. Avui no hi ha cap WARC PDF històric validat. |
| P1. Arquivo.pt | V59/V60: **32/32 URL exactes** (30 SSTT+2 EDUBCN) comprovades, 0 captures; V64: **11/11 PDF amb nom datat BCO**, 0 captures | **No esgotat.** `versionHistory` d'URL exactes no cobreix **cerca de contingut/text complet, prefixos, carpetes, noms antics de fitxer ni possibles altres dominis/URL**; cap 0 de l'arxiu representa 0 convocatòries. |
| P1. Miralls de tercers, resultats, sindicats | V85: miralls reals Girona/Tarragona, però 2021/2023 o octubre 2025; 9 IDs només resultats al cens V73 | Falta cercar còpies de **novembre-febrer**, original dels **9 només resultat**, resultat→oferta, convocatòria→republicació i codis F57/F87. GitHub tercer 06/11/25 conserva enllaç BCO del 31/10/25 però no bytes PDF. |
| P2. HTML, XHR, API pública, CSV/XLSX | EDUBCN: HTML + plantilla JS + API Jan 2026 reals (4 dates etiquetades «Data de publicació»); comparació API octubre, llengües català/castellà. Tests USTEC amb codi navegador però extracció històrica no certificada a V17 | Falta rastre XHR/Network dels **11 SSTT**, cercar exportacions públiques reals d'ofertes/resultats històrics i verificar paràmetres de curs/paginació **sense inventar endpoints**. Completar extracció USTEC/UGT si factible, només com a contrast de nomenaments. |
| P2. Versions incrementals **dins** PDF, PDFResurrect | V33: **30 PDF** revisats, **13** amb EOF/revisió interna llegible, **0 versions amb text anterior diferent** en aquell lot | **Insuficient:** la V33 feia una extracció per marcadors EOF + lector PDF, no acredita execució de `pdfresurrect -q/-w` ni `qpdf` sobre cada candidat. **A V86 hi ha 13 fitxers SHA diferent respecte al lot V24:** cal repetir forense sobre **aquests nous bytes** i discriminar canvi cosmètic vs contingut. No es poden recuperar versions d'un fitxer completament substituït només amb PDFResurrect. |
| P3. Metadades HTTP/cache/CDN | V24/V86: SHA de PDF, comparació amb 13 canvis; V75: metadades PDF originals EDUBCN | Falta fitxa temporal d'`ETag`, `Last-Modified`, `Content-Length`, `Cache-Control` per URL i si hi ha mecanisme **públic documentat** de versions del servidor; headers o `?nocache` **no** recuperen versions anteriors per si sols. |
| Qualitat dels outputs i cronologia | V73: **36 IDs** (21×507, 14×627, 1×F57-507), només **4 dates de publicació de portal EDUBCN** documentades. V87: 12 territoris i 48 estats mensuals | Falta **registre cronològic d'esdeveniments** (publicació, republicació, resultat, retirada), relació ID→versió→data, els camps exactes del manual, i una matriu **48 × fases** amb respostes per mètode; els 48 estats V87 són resum d'evidència parcial, no checklist complerta. |

## Impacte de les 13 diferències de SHA a V86

Entre l'inventari V24 (12/10/2026) i V86 (15/10/2026) **13 de les mateixes 30 URL han servit bytes diferents**. Distribució:
- Alt Pirineu i Aran **2**.
- Catalunya Central **1**.
- Girona **1**.
- Lleida **3**.
- Penedès **1**.
- Tarragona **2**.
- Terres de l'Ebre **1**.
- Vallès Occidental **2**.

**Proper control forense específic:** descarregar la **versió que avui se serveix**, registrar SHA, metadades i estructures `xref`/`/Prev`/`%%EOF`; executar `qpdf --check` i, quan hi hagi revisions, `pdfresurrect -q/-w`, validar cadascuna de les versions extretes amb text, pàgines i SHA. Comparar amb les revisions V33 quan existeixin. No confondre diferència de hash amb PDF històric recobrat: aquestes variants probablement encara poden ser 2026–27.

## Seqüència de recuperació encara pendent — prioritat efectiva

1. **Inventari històric P0 orientat a publicacions, no a PDF actuals**: per cada territori i mes identificar noms de fitxers, enllaços de resultat i PDF datats de 2025-26. Guardar noms verificats per HTML indexat, snippets o font independent i no generar noms fantasiosos com si fossin reals. Llocs amb 0 ID recuperats **primer**: Girona, Tarragona, Catalunya Central, Maresme–Vallès Oriental, Terres de l'Ebre i Alt Pirineu i Aran; no oblidar territoris amb IDs però ofertes efímeres.
2. **Wayback / PADICAT / Arquivo.pt** sobre llistes ampliades de URL i **prefixos**, no només els 30 documents vius i onze noms BCO. Dates de captura fins almenys octubre 2026, preservant els errors i aprofitant HTML amb enllaços originals encara que no hi hagi binari.
3. **Common Crawl per col·leccions**, primer comprovar servei amb un URL control conegut, després consultar tant 507/627 com URL de documents originals, noms datats i carpetes; registrar totes les 5xx i consultes NO EXECUTADES. Si apareix un CDXJ, real WARC Range i PDF amb hash.
4. **PDFResurrect, qpdf i metadades** sobre els 13 PDF que han canviat després de V33. Altres PDF amb revisions internes també es poden reexaminar si es descobreix un canvi de text en noves captures.
5. **XHR/API/fitxers de dades històrics públics**, inspeccionant el trànsit dels portals SSTT i dates de publicació/terminis, sense fabricar endpoints. Prioritzar el sistema font que alimenta els PDF, no les capçaleres de cache.
6. **Conciliació documental completa**: els 9 casos de resultat sense anunci, les 60 aparicions de 17 ID BCO i les 32 dates no certificades. Diferenciar publicació inicial i republicació; no barrejar especialitats F57/F87 sense document de correspondència.
7. **Fita d'auditoria per cadascuna de les 48 cel·les**: comptador de consultes i URL originals per via, PDF capturat i SHA, candidats i exclusió motivada, errors, consulta NO EXECUTADA i evidències; únicament `PASS` quan constin les comprovacions prioritàries realment executades. Mantenir `BLOCKED` quan el servei d'arxiu sigui inaccessible.

## Regla per aturar-se sense exagerar

No es pot dir `OBJECTIU_ACONSEGUIT` ni `exhaustiu` mentre quedin vies prioritàries accessibles sense revisar o seixanta aparicions que no es puguin vincular amb la cronologia de publicació. Si es completen totes les accions factibles i segueixen mancant còpies, es pot tancar una **campanya de cerca amb bloquejos acreditats** però no convertir la falta d'arxiu en falta històrica de places.

### Fonts de l'auditoria

- [Protocol privat, referència bibliogràfica **només**: `REFERENCIA_RECUPERACIO_HISTORICA_PDF_DC_507_627_F57_F87.md`] — no copiat al repositori.
- [V88, passada per 11 SSTT i EDUBCN](AUDITORIA_V88_PASSADA_FINAL_TOTS_11_SSTT_EDUBCN_2026-10-15.md).
- [V87, matriu territorial mensual](cens/V87_MATRIU_48_TERRITORI_MES.csv).
- [V24, inventari de PDF reals actuals](exports_territorial/SSTT_PDFS.csv).
- [V86, 30 PDF i nous hash](exports_territorial/SSTT_V86_PDF_DATES_2025_11_TO_2026_02.json).
- [V33, revisions internes de PDF](exports_forensic/PDF_V33_INCREMENTAL_REVISIONS.json).
- [Wayback, 3 URL reintentades amb 503](exports_wayback/RESUM_CDX_65S.json).
- [Registre inicial de 49 consultes d'arxius](exports_official/ARXIU_CONSULTES.csv).
- [Common Crawl, 12 CDXJ sense cap WARC](exports_commoncrawl/COMMONCRAWL_V37_WARC.json).
- [Common Crawl, 3/30 consultes V66](exports_commoncrawl/COMMONCRAWL_V66_TERRITORIAL_PREFIXES.json).
- [Common Crawl, 7/12 consultes V67](exports_commoncrawl/COMMONCRAWL_V67_SSTT_PRECISE_PDF_PREFIXES.json).
- [PADICAT EDUBCN Jan/Oct i 557 documents](AUDITORIA_V83_TANCAMENT_557PDF_PADICAT_EDUBCN_I_RASTRES_SSTT.md).
- [Arquivo.pt, 32 URL exactes i reintents](AUDITORIA_V60_TANCAMENT_RECUPERACIO_PDF_SOBREESCRITS.md).
- [33+23+9, reconciliació parcial d'IDs al cens](AUDITORIA_V68_CONTROL_QUALITAT_PUBLICACIO_36IDS_I_CDX_SSTT.md).
- [Cens V73](cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V73_36IDS.csv).

**Veredicte global:** **PARTIAL / protocol NO COMPLET**. Passada geogràfica 12/12, control mensual etiquetat 48/48 però controls `PASS` 0/48. **36 IDs provisionals**, dels quals 4 amb data de publicació del portal; **32 sense data acreditada**. Aquest informe **no** executa les fases pendents; les identifica i marca per a una represa traçable. No publicar dades personals ni confidencials.
