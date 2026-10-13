# AUDITORIA V60 — Recuperació de PDF sobreescrits en línia (13/10/2026)

**Referència metodològica:** `REFERENCIA_RECUPERACIO_HISTORICA_PDF_DC_507_627_F57_F87.md`, versió 1.0 del 12/10/2026, fitxer de Biblioteca. L'abast real d'aquest informe són els mètodes i les URL concretament comprovats; **no el cens complet de Catalunya**.

## 1. Objectiu i estat real

Reconstrucció d'ofertes DC de **507, 627, F57, F87** entre **01/11/2025 i 28/02/2026**, 11 SSTT + EDUBCN, evitant confondre PDF sobreescrit amb absència històrica. Fonts originals, data d'oferta, captures d'arxiu, adjudicacions i republicacions són entitats diferents.

**Cens únic provisional:** **36 IDs** (21 de 507; 14 de 627; 1 F57-507). En aquesta ronda **0 IDs nous** i **0/48** controls territori-mes exhaustius.

## 2. Quatre actuacions completades

| Fase | Accés / mètode | URLs | Prova i resultat |
|---|---|---:|---|
| V57 | Contrast text indexat vs PDF actual | 3 exemples territorials documentats | Indicis de substitució de versió, cap PDF original recuperat ni ID nou |
| V58 | PADICAT CDX, captura posterior al període (març–octubre 2026) | 6 URL originals de PDF | HTTP 200, **0 registres** indexats per aquestes URL, cap PDF històric descarregat |
| V59 | Arquivo.pt `versionHistory`, URLs reals ja inventariades | 32 URL, 12 àmbits (30 SSTT + 2 EDUBCN) | **16** respostes vàlides sense captures i **16** errors de connexió/timeout des de runner de GitHub |
| V60 | Reintent independent de les 16 fallades, mateix endpoint públic documentat | 16 URL | **16/16** respostes JSON reals, **0** captures; bloqueig operatiu V59 resolt |

**Consolidat Arquivo.pt V59+V60: 32/32 URL consultades amb èxit a través de dues vies de consulta, 0 versions conservades en aquell arxiu per les URL exactes i 0 PDF originals recuperats.** El control positiu `https://educacio.gencat.cat/` retorna **13 captures** (inclosa 2025-12-23, codi 301), corroborant que l'API està activa, però **no és un control de captura PDF**. Els errors originals del runner no han estat recodificats silenciosament com a «zero»; els reintents independents estan traçats al JSON V60.

### Casos de sobreescriptura documental

- **Lleida**: PDF de resultats amb ruta estable `LLE-SEC-dificil-cobertura-vacants-cobertes.pdf`. Testimoni residual del curs 2025–2026 indexat en cercador; URL viva serveix contingut de 2026–2027. Casos `2025/SEC/266` (507) i `2025/SEC/259` (627), **ja al cens**, no són ofertes originals recuperades ni tenen data de publicació certificada.
- **Barcelonès**: PDF d'ofertes amb nom nominal `BCO-SEC-dificil-cobertura-oferta-vacants_27022026.pdf` i text residual indexat, ara 404. Les seves files ja estaven al `cens/INDEX_PDFS_BCO_V22_11_LOTS.csv` i `cens/REPUBLICACIONS_BCO_V22_11_LOTS_VERIFICATS.csv`. La continuïtat d'ID entre dos lots pot ser republicació; **no** és vacant addicional.
- **Girona**: documentació anterior V16 descriu divergència entre contingut indexat de 2025–2026 i versió actual 2026–2027, sense recuperació independent de binari antic en aquesta passada.

## 3. Límit dels resultats negatius

- Un resultat de 0 del cercador d'un **arxiu concret** no equival a 0 ofertes reals, 0 publicacions a Catalunya ni 0 còpies possibles en altres arxius.
- El rang de captura pot ser posterior al període d'oferta: data d'arxiu no és data de publicació.
- Un text indexat vell és testimoni **C** i no prova completa **A/B** de PDF original amb SHA256.
- La documentació del Protocol obliga a explorar també **PDF datats encara accessibles, indexació textual en motors diferents, Wayback, Common Crawl/WARC, còpies de tercers, PDF de resultats i fonts HTML/API**. No s'han esgotat universalment aquestes vies amb aquesta ronda.
- Revisions PDF incrementals: V33 va trobar revisions internes d'alguns PDF actuals, però **cap contingut 2025-26** recuperat en aquell conjunt. No implica que no n'existeixin en altres documents.

## 4. Reproductibilitat i cadena de custòdia

- [Contrast V57](AUDITORIA_V57_PROTOCOL_PDF_SOBREESCRITS.md); [CSV de casos V57](exports_official/V57_CONTRAST_PDFS_SOBREESCRITS.csv).
- [PADICAT després del període, V58](exports_padicat/PADICAT_V58_POSTWINDOW_OVERWRITTEN_PDFS.json), [script V58](src/padicat_postwindow_overwritten_pdfs_v58.py).
- [Arquivo.pt, execució inicial V59](exports_official/ARQUIVO_PT_V59_ALL_SSTT_PDF_VERSION_HISTORY.json), [script V59](src/arquivo_version_history_all_sstt_v59.py).
- [**V60 reintents independents de les 16 consultes fallides**](exports_official/ARQUIVO_PT_V60_REINTENTS_16_URLS.json).
- [Cens territorial V51](cens/MATRIU_TERRITORIAL_V51_36IDS.csv).

**Privacitat**: resultats amb metadades de documents i codis d'oferta, sense noms, DNI ni dades dels candidats o adjudicataris.

**Veredicte parcial:** **PASS** en consulta comprovada de les 32 URL d'Arquivo.pt i en conciliació dels 16 errors operatius; **FAIL** en recuperació de PDF antics territorials per aquesta font; **NO_ACONSEGUIT** respecte a cens exhaustiu 11 SSTT + EDUBCN, novembre 2025–febrer 2026.
