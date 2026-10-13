# AUDITORIA V65 — PDF històrics sobreescrits: reintents, noms datats i control de falsos positius

**Data:** 13/10/2026. **Manual aplicat:** `REFERENCIA_RECUPERACIO_HISTORICA_PDF_DC_507_627_F57_F87.md` (Biblioteca, v1.0).

**Missió:** ofertes i republicacions publicades entre 01/11/2025 i 28/02/2026 per a 507, 627, F57, F87, a Catalunya. El cens continua provisional: **36 identificadors**, 0/48 blocs territori-mes exhaustius.

## 1. V63: reintent REAL de quatre HTTP 502/504 de Common Crawl

Font original: [V62](exports_commoncrawl/COMMONCRAWL_V62_BCO_DATED_PDFS.json). Quatre consultes exactes bloquejades; [reintents V63](exports_commoncrawl/COMMONCRAWL_V63_BCO_RETRY_5XX.json).

| PDF datat | Col·lecció Common Crawl consultada | V62 | V63 | Lectura correcta |
|---|---|---|---|---|
| Barcelonès 14/11/2025 | CC-MAIN-2025-47 | 502 | **404** | Sense captura en aquell índex |
| Barcelonès 05/12/2025 | CC-MAIN-2025-51 | 502 | **404** | Sense captura en aquell índex |
| Barcelonès 23/01/2026 | CC-MAIN-2026-04 | 504 | **404** | Sense captura en aquell índex |
| Barcelonès 27/02/2026 | CC-MAIN-2026-12 | 504 | **502 i 504** | **Bloqueig tècnic pendent** |

V62 + V63: de les 13 consultes de V62, 9 tenien 404 i 4 errors; **3 dels 4 errors resolts**. Per tant, **12 de les 13 consultes** han retornat 404, **una** queda bloquejada. Cap registre CDXJ positiu ni PDF WARC validat. **No** significa que les 11 ofertes datades fossin inexistents; tan sols no han tornat captures en aquests índexs concrets.

## 2. V64: via alternativa d'Arquivo.pt específicament per als 11 PDF amb noms datats

Hi havia un buit operatiu: la V59/V60 havia cobert 32 URL **habituals/mutables**, no els 11 documents `Barcelones-SEC-...` i `BCO-SEC-...` amb data al nom verificats a `cens/INDEX_PDFS_BCO_V22_11_LOTS.csv`.

S'han executat **11/11** peticions reals al servei públic documentat `https://arquivo.pt/textsearch?versionHistory=...`, totes **amb resposta JSON vàlida**, **0 errors** i **0 captures** per a les 11 URL exactes. S'ha conservat la consulta original de cadascuna i el resultat buit al fitxer [V64](exports_official/ARQUIVO_PT_V64_BCO_11_DATED_PDFS.json).

Això **no** exclou versions amb altres noms, antigues adreces de domini o captures als serveis Wayback, PADICAT, col·leccions de tercers i Common Crawl.

## 3. Cerca de PDF i miralls addicionals

S'han consultat cerques independents de PDF nominals de novembre/desembre 2025 i gener/febrer 2026, serveis territorials que no tenen cap ID recuperat, còpies a Scribd/Docsity, variants de URL `?nocache=`, PDF de resultats territorials i especialitats PFI. Troballes i exclusions contrastades:

- **Baix Llobregat PFI, `BLL-PFI.pdf`**: PDF oficial amb text indexat, signat a Sant Feliu **01/07/2025**, menciona `Institut Torre Roja` i `F57 → 507` (1 vacant); **fora de l'interval** 01/11/2025–28/02/2026. No es duplica com nova oferta. URL font: https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/baix-llobregat/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/BLL-PFI.pdf
- **Maresme–Vallès Oriental**: PDF de resultats accessible amb referències a adjudicacions de l'inici del curs **setembre 2025**, però la versió recuperada no aporta cap nova publicació datada de novembre a febrer de 507/627. URL: https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/maresme-valles-oriental/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/MVO-SEC-dificil-cobertura-vacants-cobertes.pdf
- **Catalunya Central i Girona**: les versions actuals del PDF de resultats de secundària estan centrades en l'any escolar **2026–2027**. Una fila 627 de setembre 2026 a Catalunya Central **és fora de l'abast** i no es compta. URL: https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/catalunya-central/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/CCE-SEC-dificil-cobertura-vacants-cobertes.pdf
- **Falsos positius de motors alternatius**: algunes cerques textuals retornen el catàleg estatal del SEPE, convocatòries de València o PDF vigents 2026–2027. Aquests resultats **no** són les DC docents catalanes 507/627 del nostre període.
- **Variants `?nocache=` en URL de PDF actuals**: diversos enllaços de 2026–2027 apareixen a índexs amb aquest paràmetre; els paràmetres URL o snippets actuals **no** són per si sols captures històriques del document antic.

Els testimonis indexats es conserven com a nivell **C**, amb distinció entre *text que hi havia a l'índex* i *bytes d'un document original*. No s'afirma que els PDF sobreescrits s'hagin recuperat com a binari.

## 4. Auditoria

- **PASS**: 3 errors 5xx reintentats fins a resultat inequívoc; 11/11 URL datades d'Arquivo.pt revisades efectivament; comprovació temporal dels candidats fora de finestra.
- **BLOCKED**: Common Crawl, PDF Barcelonès 27/02/2026, col·lecció `CC-MAIN-2026-12`, després de reintent acotat.
- **PARTIAL**: recuperació de fragments indexats; **0** PDF binaris antics nous i **0** identificadors nous.
- **FAIL / OBJECTIU EXHAUSTIU NO ASSOLIT**: els 12 àmbits i els 48 controls mensuals no queden certificats. **36 IDs provisionals**.

La següent línia útil és identificar **URL antigues amb altres noms / mirrors de tercers amb text del 2025–2026**, i recuperar snapshots originals. Repetir les mateixes URL amb 404 en un sol rastreig no és productiu. Distingir sempre `data_nom_del_pdf`, `data_publicacio`, `data_captura`, `data_inici`, `data_resultat`.

**Seguretat:** no s'han publicat dades personals de persones candidates o adjudicatàries.
