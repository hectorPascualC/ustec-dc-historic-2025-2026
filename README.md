# Recuperador USTEC — històric de difícil cobertura 2025–2026

Aquest repositori és **públic i sense dades personals**. Fa servir únicament el cercador històric públic d'USTEC, sense cookies, claus ni secrets. Els CSV publicats a `exports/` **anonimitzen `numero_adjudicat`**, per evitar publicar números individuals.

## Única execució / sense cost per minuts

A **Actions → Recuperar DC USTEC 2025-2026 → Run workflow**, branca `main`. El primer commit del workflow a `main` en dispara una execució automàtica. No hi ha cap programació recurrent. El runner `ubuntu-24.04` és estàndard i gratuït en repositoris públics; es limita el job a 30 minuts. Els resultats queden desats a `exports/` en el mateix repositori; **no es creen artefactes facturables d'Actions**.

## Dades que intenta recuperar

- Curs `2025-2026`; nomenaments del `01/11/2025` al `28/02/2026`.
- Especialitats 507, 627, F57 i F87.
- Totes les files, incloent-hi les `No adjudicat` si la taula permet activar-les.
- `USTEC_nomenaments_DC_explicits.csv`: només files que declaren explícitament `Difícil cobertura`.
- `AUDITORIA_EXTRACCIO.json`: pàgines descarregades, total segons la taula, advertiments, estat `complete` i URL AJAX observats.

**Important:** aquesta font recull nomenaments i intents de nomenament, no l'univers complet de publicacions d'ofertes DC; les ofertes no adjudicades, retirades o republicades poden faltar. Un `complete=true` es refereix només a l'extracció de les files retornades per USTEC.

## Diagnòstic

Si el workflow surt en vermell, revisa `exports/AUDITORIA_EXTRACCIO.json` i les pestanyes del run per veure l'error. No interpretis un CSV buit com a absència de places. Si el servidor fallés abans de generar l'auditoria, consulta els logs del run.

## Investigació documental de DC (novembre 2025 – febrer 2026)

- [Cens provisional de **36 identificadors** (V49)](cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V49_36IDS.csv): 21 de 507, 14 de 627, 1 F57-507. **No és exhaustiu**; 0/48 blocs territori-mes certificats.
- [Auditoria territorial i documental V51](AUDITORIA_V51_PADICAT_120PDFS_CENS36.md): 120 PDF històrics analitzats, quatre originals EDUBCN contrastats amb PADICAT.
- [**Auditoria V52**: resultats i correcció de jornada 627 de l'ITB](AUDITORIA_V52_EDUBCN_RESULTATS_JORNADES_2026-10-13.md).
- [**Correccions V52** dels quatre casos EDUBCN](cens/EDUBCN_4_CASOS_V52_CORRECCIONS.csv). **Aquestes correccions prevalen sobre les jornades i estats indeterminats de V49**; els 36 ID continuen sense duplicats.

- [**Auditoria V55 — 248/248 PDF arxivats del directori EDUBCN (29/01/2026)**](AUDITORIA_V55_TANCAMENT_CORPUS_PADICAT_EDUBCN_248PDF.md). Cobertura completa **només d'aquesta fotografia**, no de tot el període ni de Catalunya.
- [**Verificació V56**](exports_padicat/EDUBCN_V56_FULL_PAGES.json): 87 PDF rellegits íntegrament, 320 pàgines, 9 fitxers de més de set pàgines, 0 candidats nous. El tancament V55 incorpora aquesta comprovació.
- [Auditoria V57 — PDF sobreescrits: text antic indexat vs fitxer actual](AUDITORIA_V57_PROTOCOL_PDF_SOBREESCRITS.md). Reconstrucció de proves amb criteris de no duplicació.
- [V58 — cerca de captures PADICAT posteriors al febrer 2026](exports_padicat/PADICAT_V58_POSTWINDOW_OVERWRITTEN_PDFS.json): sis PDF oficials, índex HTTP 200 i 0 captures recuperades per les URL provades.
- [V59 — primera comprovació de versions a Arquivo.pt](exports_official/ARQUIVO_PT_V59_ALL_SSTT_PDF_VERSION_HISTORY.json): 32 PDF oficials, 16 HTTP 200 sense captures i 16 errors de xarxa, corregits a V60.
- [**Auditoria V60 — PDF sobreescrits (protocol original), 32/32 URL Arquivo.pt verificades**](AUDITORIA_V60_TANCAMENT_RECUPERACIO_PDF_SOBREESCRITS.md); [reintents documentats](exports_official/ARQUIVO_PT_V60_REINTENTS_16_URLS.json). Cap nova convocatòria acreditada; 0/48 controls exhaustius.
- [**V61 — Persistència documental al Barcelonès**](AUDITORIA_V61_BCO_PERSISTENCIA_11_LOTS_17_IDS.md): 11 lots datats, 60 aparicions, 17 identificadors únics (tots ja al cens). No confondre aparicions amb places noves.
- [V62 — proves Common Crawl dels 11 PDF datats](exports_commoncrawl/COMMONCRAWL_V62_BCO_DATED_PDFS.json): consultar la sortida després de l'execució corregida del workflow; el primer intent fou invàlid per una capçalera HTTP incorrecta.

- [**Auditoria V65 — PDF sobreescrits, Common Crawl V63 i Arquivo.pt V64**](AUDITORIA_V65_REINTENTS_I_MIRALLS_PDF_2026-10-13.md): 3/4 errors V62 resolts, 11/11 PDF datats de Barcelonès comprovats a Arquivo.pt, 1 bloqueig CC pendent, cens 36 no exhaustiu.
- [**Auditoria V68 — comprovació de qualitat dels 36 identificadors**](AUDITORIA_V68_CONTROL_QUALITAT_PUBLICACIO_36IDS_I_CDX_SSTT.md): 22 ofertes indexades, 1 oferta i resultat, 9 resultats només, 4 originals EDUBCN; **0/36 dates de publicació certificades** al cens V49.
- [V66 — Common Crawl per directoris territorials](exports_commoncrawl/COMMONCRAWL_V66_TERRITORIAL_PREFIXES.json): 3 de 30 consultes executades, 3 errors 502/504, aturada segura.
- [V67 — Common Crawl per nom exacte/prefix PDF](exports_commoncrawl/COMMONCRAWL_V67_SSTT_PRECISE_PDF_PREFIXES.json): 7 de 12 consultes executades, 6 errors 5xx, 1 resultat 404 restringit a un índex; no es poden certificar absències.
- [**Auditoria V69 — Matriu completa dels 48 controls territori×mes**](AUDITORIA_V69_MATRIU_48_TERRITORI_MES_NO_EXHAUSTIUS.md): 14 controls PARTIAL, 34 BLOCKED, 0 PASS; cap cas sense document no es considera zero places.
- [**V74 — prova històrica de la data de publicació (HTML+JS+API EDUBCN, 29/01/2026)**](AUDITORIA_V74_EDUBCN_PROVA_DATA_PUBLICACIO_I_CENS_CONSOLIDAT.md): 4 dates de publicació segons el portal acreditades; **primera publicació absoluta encara no provada**.
- [**Cens consolidat V73 — 36 ID, 4 dates certificades de portal i correccions de jornada**](cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V73_36IDS.csv); [control JSON](exports_padicat/EDUBCN_V73_PUBLICATION_PROOF_AND_CENSUS_QA.json). Supera el recompte de `0/36 dates` dels informes V68/V69.
- [V70 — 13 URL HTML/REST oficials PADICAT](exports_padicat/PADICAT_V70_SSTT_HTML_HISTORIC_LINKS.json): 3 captures HTML i 2 JSON EDUBCN; 11 URL HTML territorials sense captura en consulta exacta.
- [V71–V72 — fitxers JS arxivats i la relació de `Data de publicació` amb `DATA`](exports_padicat/EDUBCN_V72_ARCHIVED_JS_PUBLIC_API_ROUTES.json).
- [**V75 — originals PDF EDUBCN de gener: 4/4 SHA256 verificats, dues creacions internes de desembre 2025**](exports_padicat/EDUBCN_V75_PDF_ORIGINAL_CREATION_DATES.json). No equivalen a dues dates de primera publicació demostrades.
- [**V80 — auditories V76–V79: buit de febrer, setmanes datades i resultats EDUBCN**](AUDITORIA_V80_BARCELONES_BUITS_I_EDUBCN_BILINGUE_RESULTATS.md): sense nova plaça; 36 IDs, 4 dates portal, 0/48 controls exhaustius.
- [V76 — dues respostes PADICAT gener/octubre EDUBCN](exports_padicat/EDUBCN_V76_JAN_OCT_2026_TARGET_DIFF.json): 49 vs 145 files, cap nova oferta de novembre–febrer.
- [V77 — sis divendres sense PDF datat al Barcelonès](exports_official/BCO_V77_GAPS_PDF_FILENAME_PROBES.json): 18 URL hipotètiques testades, 18 HTTP 404 actuals; no prova absència en 2025–26.
- [V78 — 4 API arxivades EDUBCN, català/castellà](exports_padicat/EDUBCN_V78_BILINGUAL_API_HISTORIC_DIFF.json): mateix conjunt de codis en els dos idiomes, quatre ofertes objectiu.
- [V79 — dates de creació de dos PDFs de resultats EDUBCN](exports_padicat/EDUBCN_V79_RESULT_PDF_DATES.json): 2/2 hash coincideixen amb arxiu V54, no primeres dates d'oferta.
- [**Auditoria V83 — PADICAT EDUBCN, 557 URL de PDF diferents en dues captures**](AUDITORIA_V83_TANCAMENT_557PDF_PADICAT_EDUBCN_I_RASTRES_SSTT.md): 248 PDF de gener ja auditats, 309 documents nous d'octubre verificats, 0 noves ofertes segons cerca textual; testimonis indexats de Girona/Tarragona sense data publicació dins període.
- [**V82 — 309/309 PDF nous de la captura d'octubre verificats**](exports_padicat/EDUBCN_V82_FULL_OCT_DELTA_2025_26.json): 557 URL úniques entre gener/octubre, 79 comunes sense canvi de digest, cap candidat nou 507/627/F57/F87 del curs 2025–26 detectat; no prova absència entre captures.
- [V81 — primera indexació post-gener EDUBCN](exports_padicat/EDUBCN_V81_POST_JAN_ARCHIVED_PDFS.json): 393 captures i 390 URL PDF al rang febrer–octubre; primera lectura de 65 candidats, completada a V82.
