# Auditoria V21 — nous intents de recuperació, indexació residual i comprovació d'EDUBCN

Data de revisió: 12/10/2026. Abast: ofertes **507, 627, F57, F87** (incloses combinacions) efectivament publicades de 01/11/2025 a 28/02/2026 en 11 SSTT + EDUBCN. **Cens exhaustiu NO certificat**.

## 1. Nou recuperador dels PDF originals de dates fixes del Barcelonès

S'ha desenvolupat i executat el programa `src/scan_fixed_bcn_pdfs.py` amb `pymupdf`, comprovació de l'encapçalament real `%PDF`, SHA256, desduplicació i comparació contra els 31 IDs de V20. S'han provat les **17 dates setmanals dels divendres** des de 07/11/2025 fins 27/02/2026 i **4 noms de fitxer** alternatius per data: **68 URL** del domini oficial.

Resultat auditat del [workflow real](https://github.com/hectorPascualC/ustec-dc-historic-2025-2026/actions/runs/38292173068):

- **68 respostes HTTP 404**, inclosos noms de fitxer que anteriorment varen estar indexats i amb text disponible en resultats del cercador.
- **0 PDF descarregats en viu**, **0 casos nous** procedents d'aquest recuperador i **0 territoris-mes certificats**.
- Les 68 URL i codis de resposta estan desats a [exports_bco/BCO_CONSULTES.csv](exports_bco/BCO_CONSULTES.csv); [auditoria JSON](exports_bco/BCO_AUDITORIA.json).
- Això **no demostra inexistència històrica de les ofertes**; indica que el servidor viu **ja no conserva aquells recursos a les URL originals**.

## 2. Recuperació de metadades en còpies indexades del cercador

Tot i el 404 en viu, el servei d'indexació conserva **text extret de còpies antigues**:

**Barcelonès — lot del 05/12/2025**: PDF de 14 pàgines, expedients 507:
- `19143261`: Institut Provençana, 0,50, termini 08/12/2025, inici 09/12/2025, final prevista 30/06/2026, pàgina 2/14.
- `19276920`: Institut La Pineda, sencera, termini 08/12/2025, inici 09/12/2025, final prevista 22/12/2025, pàgina 3/14.
- `19089426`: Institut Provençana, sencera, termini 08/12/2025, inici 09/12/2025, final prevista 25/12/2025, pàgina 4/14.
- Aquestes **3 places ja eren a V20**.

**Barcelonès — lot del 09/01/2026**: PDF de 12 pàgines:
- `19297807`: Institut Provençana, 507 sencera, termini 11/01/2026, inici 12/01/2026, final prevista 29/01/2026, pàgina 1/12.
- `19089426`: Institut Provençana, 507 sencera, termini 11/01/2026, inici 12/01/2026, final prevista 30/01/2026, pàgina 2/12.
- `19276920`: Institut La Pineda, 507 sencera, termini 11/01/2026, inici 12/01/2026, final prevista 31/01/2026, pàgina 3/12.
- `19143261`: Institut Provençana, 507 mitja, termini 11/01/2026, inici 12/01/2026, final prevista 30/06/2026, pàgina 4/12.
- Aquestes **4 places ja eren a V20**.

Aquestes **7 aparicions de només 4 identificadors únics** queden desades a [cens/REPUBLICACIONS_BCO_DESEMBRE2025_GENER2026_V21.csv](cens/REPUBLICACIONS_BCO_DESEMBRE2025_GENER2026_V21.csv).

Les dates del nom del PDF i els terminis **no certifiquen** la data efectiva de publicació. El text indexat recuperat no és una còpia PDF immutable descarregable. Es tracta de **traça documental secundària**, no d'un arxiu original preservat.

Fonts:
- https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/barcelones/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/Barcelones-SEC-dificil-cobertura-oferta-vacants_05122025.pdf
- https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/barcelones/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/Barcelones-SEC-dificil-cobertura-oferta-vacants_09012026.pdf

## 3. Investigació del JavaScript públic d'EDUBCN

[Execució](https://github.com/hectorPascualC/ustec-dc-historic-2025-2026/actions/runs/38292475977) del programa `src/probe_edubcn_js_endpoints.py`; fitxer JavaScript públic 470.923 bytes, HTTP 200.

- L'AngularJS configura `API_URL: "/pdc_rest"`.
- El model de convocatòries executa `api.query({what:"convocatories",lang:t.language})`, que correspon al backend ja verificat `/pdc_rest/convocatories/ca`.
- En el codi de frontend analitzat **no hi ha** cap paràmetre de data històrica ni cap ruta explícita `archive` / `historic` per recuperar el curs 2025–2026.
- **No és prova que el servidor no disposi de cap API privada/històrica**, sinó que la pàgina pública actual *no la invoca*.
- [Audit JSON de codi i fragments](exports_edubcn/EDUBCN_JS_ENDPOINTS.json).

## 4. Cerca addicional en els 9 casos coneguts només per resultats

S'han provat cerques específiques per identificador (entre altres `19217376`, `19258737`, `19336990`, `19072798`, `19239349`, `2025/SEC/266`, `2025/SEC/259`, `2025/SEC/PFI/245`, `19224754`). Els resultats indexats no han revelat cap nova **oferta original verificada**. Continuen amb classificació `resultat_indexat`.

## 5. Veredicte i següent hipòtesi

**31 identificadors únics sense canvis respecte V20**, dels quals 22 amb traça d'oferta indexada i 9 amb resultat sol. **0 de 48 territori-mes certificats**.

**FAIL: cens exhaustiu pendent.** L'accés a PDFs retirats via el servidor original és inviable amb les 68 URL provades; aquesta limitació documentada fa que reintentar noms de fitxer en directe no sigui una estratègia suficient. La línia més raonable és **índexs textuals conservats per tercers, repositoris sindicals de còpies i fonts alternatives territorials**, sense considerar els 404 com a zeros de places.

La informació personal de docents i candidats no es conserva als CSV públics.

## 6. Comprovació de les col·leccions i límits dels arxius (no certifica absències)

S'ha llegit el fitxer públic [Common Crawl collinfo.json](https://index.commoncrawl.org/collinfo.json) i verificat que els quatre identificadors usats en la primera passada històrica **SÍ existeixen**:
`CC-MAIN-2025-47` (06–19/11/2025), `CC-MAIN-2025-51` (04–17/12/2025), `CC-MAIN-2026-04` (12–25/01/2026) i `CC-MAIN-2026-08` (06–19/02/2026).

Per tant els HTTP 503 de la consulta anterior **no es poden atribuir a noms de col·lecció inventats**, sinó que són compatibles amb **limitació de freqüència o indisponibilitat del CDX**. La documentació oficial de Common Crawl indica que el servidor és molt limitat, que un 503 és senyal per reduir el ritme i que es pot bloquejar temporalment la IP fins a 24 hores.

Fonts: [Common Crawl FAQ](https://commoncrawl.org/faq), [inventari de col·leccions](https://index.commoncrawl.org/collinfo.json). Les consultes alternatives puntuals a `archive.org/wayback/available` i al CDX han rebut redireccions no compatibles en la lectura remota; **no hi ha còpia històrica acreditada**.

**Decisió:** no saturar els arxius públics amb retries massius; cap prova d'absència de places es dedueix dels 404/503/errors de consulta.
