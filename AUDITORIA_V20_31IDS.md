# Auditoria històrica V20 — 31 identificadors DC (01/11/2025–28/02/2026)

Data de revisió: 12/10/2026. **No és un cens exhaustiu certificat**.

## Objectiu i delimitació
Reconstruir les **ofertes originals publicades** i republicacions de difícil cobertura (DC) de les especialitats 507, 627, F57, F87 i combinacions documentades, entre l'1 de novembre de 2025 i el 28 de febrer de 2026. Àmbit: 11 serveis territorials i Consorci EDUBCN. La data de termini o inici **no** certifica la data exacta de publicació. Una fila de resultat d'adjudicació sola **no** és prova de la convocatòria original.

## Corpus V20
- **31 identificadors únics**: **19** d'especialitat `507`, **11** de `627` i **1** de `F57-507`.
- Territorial: **17 Barcelonès**, **9 Baix Llobregat**, **3 Lleida**, **1 Penedès** i **1 Vallès Occidental**. La manca de dades dels altres àmbits **no implica zero ofertes**.
- **22** amb text d'oferta històrica indexada; **9** coneguts només per resultat o adjudicació indexats.
- **0/48 combinacions territori-mes** acreditades com a exhaustives.

## Tres casos NOVES recuperats des de V8 (no apareixien entre els 28 ID inicials)

### 1) `19331041` — Institut Obert de Catalunya (Barcelonès), 507, sencera
- Oferta oficial historitzada, sense còpia immutable descarregable.
- Figura al llistat nominal `BCO-SEC-dificil-cobertura-oferta-vacants06022026.pdf`, **pàg. 7/26**, termini **08/02/2026**, inici **10/02/2026**, fi prevista **30/06/2026**.
- Republicacions constatades amb el **mateix ID**: `...13022026.pdf`, **pàg. 5/29**, termini **15/02/2026**, inici **17/02/2026**; i `...20022026.pdf`, **pàg. 3/33**, termini **22/02/2026**, inici **24/02/2026**.
- També figura en el llistat **27/02/2026**, amb termini **01/03/2026**, inici **03/03/2026**; això és una altra aparició del MATEIX identificador, no una nova plaça.
- Requisits visibles: competències digitals avançades, Moodle, presencialitat a la seu de l'IOC.
- Fonts:
  - https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/barcelones/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/BCO-SEC-dificil-cobertura-oferta-vacants06022026.pdf
  - https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/barcelones/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/BCO-SEC-dificil-cobertura-oferta-vacants13022026.pdf
  - https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/barcelones/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/BCO-SEC-dificil-cobertura-oferta-vacants20022026.pdf

### 2) `507-25/11 (1)` — Institut La Ferreria (Vallès Occidental), 507, sencera
- **Oferta original**, recuperada en una indexació històrica del PDF oficial de VOC. **Pàgina 13/26** del document original indexat, encara que la URL pública actual ja apunta a una altra versió.
- Text indexat: identificador **507-25/11 (1)**, especialitat 507, **TERMINI OBERT**, centre **Institut La Ferreria** (Montcada i Reixac), jornada **sencera**, inici **immediat**, fi **09/12/2025**.
- Les observacions admeten diverses titulacions de grau superior de l'àmbit TIC; no es pot deduir adjudicació ni sortida fora de borsa.
- `25/11` apareix al codi de plaça, però **no es tracta d'una prova independent de l'instant de publicació**.
- Font: https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/valles-occidental/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/VOC-SEC-dificil-cobertura-oferta-vacants.pdf

### 3) `19365399` — Institut La Pineda (Barcelonès), 507, sencera
- Oferta del llistat nominal `BCO-SEC-dificil-cobertura-oferta-vacants_27022026.pdf`, **pàgina 6/31**.
- Termini candidatura **01/03/2026**, inici **03/03/2026**, final **30/06/2026**.
- **Primera aparició documentada en un fitxer amb data 27/02/2026**, que cau dins la finestra. No s'ha trobat en els PDF del **13/02** ni del **20/02**. **No confondre** termini posterior (1 de març) amb publicació posterior.
- Data real de publicació 27/02 encara **no certificada per un registre immutable**.
- Font: https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/barcelones/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/BCO-SEC-dificil-cobertura-oferta-vacants_27022026.pdf

## Altres comprovacions i exclusions
- Històric de Lleida: existeixen versions indexades amb resultats 2025–2026, però l'URL és **mutable** i també serveix un fitxer 2026–2027. La data d'inici al resultat, per si sola, no valida la publicació de l'oferta. No hem afegit nous identificadors de Lleida en aquesta passada.
- EDUBCN: el REST actual `/pdc_rest/convocatories/ca` no és un històric complet. Els rastres d'ofertes `GENSEC_2526_125` i `GENSEC_2526_126` del 27/10/2025 queden **fora** de la finestra, si no s'acredita una republicació posterior.
- La convocatòria de **concurs de mèrits** de l'IOC al gener–febrer de 2026 (1 plaça 627) és **un procediment diferent**, no una DC ordinària, i s'ha exclòs.
- USTEC ofereix dades de nomenaments ordinaris, però el filtre DC del servidor retorna zero. **No es pot usar aquest zero** com a recompte de DC reals.
- El rastreig Wayback/Common Crawl/Arquivo.pt via GitHub Actions anterior va recuperar **0 captures** en 49 consultes (moltes amb errors 503/timeout). No prova inexistència de fitxers.

## Auditoria final
**FAIL / cens exhaustiu no completat.** S'han **afegit 3 ID verificables com a rastres d'oferta**, s'han contrastat republicacions i exclusions, i el corpus de **31 ID** està deduplicat. Resten **9 casos només de resultat** i **12 àmbits territorials no certificats**. Calen més fonts originals, incloent places desertes, retirades i publicacions no indexades.

La base de dades V20 és [cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V20_31IDS.csv](cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V20_31IDS.csv).
