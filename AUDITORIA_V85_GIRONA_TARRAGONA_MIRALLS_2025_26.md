# AUDITORIA V85 — Girona i Tarragona: miralls externs, proves cronològiques i exclusions

**Data:** 15/10/2026. **Missió:** recuperar ofertes 507, 627, F57 i F87 **publicades** entre l'1 de novembre de 2025 i el 28 de febrer de 2026. Protocol obligatori: `REFERENCIA_RECUPERACIO_HISTORICA_PDF_DC_507_627_F57_F87.md`, Biblioteca ChatGPT (v1.0), amb dates de publicació, documents originals, resultats i republicacions diferenciats.

## 1. Recerca externa executada

Cerca textual pública específica per les **URL oficials GIR-SEC i TAR-SEC** d'ofertes/resultats, els codis `507`, `627`, `F57`, `F87`, cursos `2025–2026`, mesos novembre–febrer, i mirrors `docsity.com`, `scribd.com`, incloses variants de noms de fitxer. Eines de cerca independents; fonts finals verificades amb el contingut publicat.

**Troballa 1 — repositori d'un tercer amb segell de temps contemporani.**
- Repositori públic `blackcub3s/projectesDocker`, fitxer `scrapEnsenyament/parsejaDifCob.py`.
- [Commit `b48a40964a1e5fb1a91623bd873627f8ddcfdfd1` del 06/11/2025](https://github.com/blackcub3s/projectesDocker/blob/b48a40964a1e5fb1a91623bd873627f8ddcfdfd1/scrapEnsenyament/parsejaDifCob.py), data de committer 2025-11-06 14:59:31 UTC; missatge: «afegit pdf barcelones i afegit sistema per detectar si el PDF no hi es a la URL: control excepcions filenotfou».
- El codi d'aquell commit inclou **un enllaç nominal oficial** `Barcelones-SEC-dificil-cobertura-oferta-vacants_31102025.pdf` i rastreja explícitament les especialitats **627 i 507**, entre altres.
- **Aporta un testimoni independent que el 6/11/2025 aquell enllaç ja constava en un script públic de monitoratge**; **NO** acredita que una plaça determinada fos anunciada durant el període objectiu. El document nominal és de **31/10/2025, fora de la finestra**.
- El programa descarrega PDFs de les URL de la Generalitat, en llegeix les línies coincidents i al final fa `esborra_pdfs(..., True)`. **No hi ha fitxers històrics versionats al repositori ni una persistència de continguts en l'script mateix**. L'enviament de notificacions per Pushover tampoc no és un arxiu públic accessible.

**Troballa 2 — Docsity té fragments d'un PDF original de Tarragona, però de l'octubre de 2025.**
- [Mirall Docsity](https://www.docsity.com/es/docs/dificil-cobertura-en-diferentes-contextos/14696135/), apartat «Oferta de vacants o substitucions», text reproduït.
- Registre `103-43005704`: especialitat **507**, Institut Francesc Vidal i Barraquer, jornada sencera, incorporació **octubre de 2025**.
- Registre `104-43005704`: mateix centre i especialitat **507**, jornada sencera, incorporació **octubre de 2025**, fi indicada «Alta titular».
- Els dos casos són **anteriors a novembre pel seu inici**, i ja consten entre els casos que no s'han incorporat a `cens/V26_CANDIDATS_EXCLOSOS_I_NO_CERTIFICATS.csv`. Per tractar-los com oferta de novembre–febrer caldria **prova de publicació o republicació dins la finestra**, inexistent en aquest mirall.
- La classificació editorial externa de Docsity «2023/2024» **no s'ha emprat com a any del PDF original**: aquest últim conté explícitament `Octubre 2025`. Tampoc s'ha assumit una data exacta de pujada del mirall que no estigui corroborada.

**Troballa 3 — mirrors Scribd reals, però de cursos antics.**
- [Tarragona, resultats de curs 2023–2024](https://www.scribd.com/document/761847498/TAR-SEC-Dificil-Cobertura-Vacants-Cobertes): hi figuren dates d'inici `1/9/2023` i de fi `31/8/2024`, amb algunes especialitats 507/627; no és 2025–2026.
- [Girona, ofertes 2022–2023](https://it.scribd.com/document/656651472/GIR-SEC-dificil-cobertura-oferta-vacants-1): termini de sol·licituds `27/02/2023` i codis `...S/2022-2023`; no és 2025–2026.
- [Tarragona, ofertes curs 2021–2022](https://www.scribd.com/document/527327747/TAR-SEC-dificil-cobertura-oferta-vacants-3): data inici setembre/octubre 2021; no és 2025–2026.

Aquests miralls **demostren que la còpia independent de PDF sobreescrits és possible**, però cap dels tres és un candidat vàlid per al període investigat.

## 2. Altres rastres dels SSTT que continuen pendents

- Girona: `149S/2025-2026`, especialitat **627**, Institut Sa Palomera, inici **13/10/2025**. És una fila de **resultat** de document 2025–26 indexat; sense data acreditada de la seva **oferta inicial o republicació** dins novembre-febrer.
- Tarragona: `87-43008638`, especialitat **627**, Institut Antoni Ballester; `88-43002594`, 627, Institut Baix Camp. Consten en fragments de resultats com adjudicades telemàticament **sense data d'oferta**. Cap no pot comptar encara.
- URL oficial de Girona: https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/girona/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/GIR-SEC-dificil-cobertura-vacants-cobertes.pdf
- URL oficial de Tarragona: https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/tarragona/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/TAR-SEC-dificil-cobertura-vacants-cobertes.pdf

Les dues URL **s'han sobreescrit amb contingut actual**; el text de resultats antics als índexs no certifica el binari original ni la publicació exacta. No reproduir identitats o dades de barem del personal adjudicat.

## 3. Fitxer de controls i veredicte

[**V85 — vuit controls documentals, cap sumat al cens**](cens/V85_EVIDENCIES_EXTERNALS_GIRONA_TARRAGONA_NO_COMPTADES.csv).
- **5 candidats concrets de 2025** contrastats amb V26 o V83, sense prova de publicació novembre–febrer (Girona 1, Tarragona 4).
- **3 miralls externs** datats 2021, 2023 (Girona) i 2023 (Tarragona), explícitament exclosos.
- **1 testimoni extern addicional**: GitHub, codi de monitoratge publicat en commit 06/11/2025, **sense PDF binari conservat**.
- **0 identificadors 507/627/F57/F87 nous acreditats com a publicats novembre 2025-febrer 2026**.
- **No modificar el cens V73** (36 identificadors provisionals: 21 de 507, 14 de 627, 1 F57-507), **4 dates del portal EDUBCN acreditades**.
- **0/48** combinacions territori×mes certificades exhaustives, resultat **PARTIAL**.

**PASS:** datació i contrast dels miralls i commit, deduplicació amb exclosos V26, absència de noves files sense document original dins finestra. **PENDENT:** primera publicació original o prova de republicació dels candidats; recuperar PDF 2025–26 de fonts externes no identificades i dades de la resta de SSTT.

## 4. Priorizació útil de la propera fase

Prioritzar **originals datats dels mesos novembre 2025–febrer 2026** dels SSTT Girona/Tarragona i la resta sense IDs, especialment mirrors on es pugui provar **un segell de temps independent** i contingut de l'oferta. Un *resultat* de 2025–26 o un *PDF original de setembre/octubre* sense republicació és insuficient per incrementar el cens del període. No dedicar més passades a recórrer mirror de 2021–2024 ni als mateixos resultats vius sobrescrits. 
