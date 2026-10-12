# AUDITORIA V25 — fonts independents, rastreig existent el novembre de 2025 i reintent d'arxius

**Execució:** 12/10/2026. Objectiu: **ofertes originals publicades entre 01/11/2025 i 28/02/2026** de difícil cobertura 507, 627, F57 i F87, als 11 SSTT i EDUBCN. El cens **no és exhaustiu**.

## 1. Nova font independent trobada: repositori de seguiment contemporani

Repositori públic de tercers: [blackcub3s/projectesDocker — scrapEnsenyament/parsejaDifCob.py](https://github.com/blackcub3s/projectesDocker/blob/main/scrapEnsenyament/parsejaDifCob.py).

El commit [3487db0 (06/11/2025)](https://github.com/blackcub3s/projectesDocker/commit/3487db0a796e1e1d2333f216c5e5ba629f50d40c), dintre del període d'estudi, introdueix una comprovació de PDF del **Barcelonès amb nom nominal `Barcelones-SEC-dificil-cobertura-oferta-vacants_31102025.pdf`**, del dia abans de l'inici del període. L'script Python descarregava PDF i cercava les especialitats **627 i 507**, entre altres, i enviava resultats a notificacions push.

URL originals documentades pel codi:
- Lleida: `LLE-SEC-dificil-cobertura-oferta-vacants.pdf`
- Terres de l'Ebre: `TEB-SEC-dificil-cobertura-oferta-vacants.pdf`
- Baix Llobregat: PDF de **serveis educatius**, no secundària ordinària.
- Tarragona: `TAR-SEC-dificil-cobertura-oferta-vacants.pdf`
- Girona: `GIR-SEC-dificil-cobertura-oferta-vacants.pdf`
- Vallès Occidental: `VOC-SEC-dificil-cobertura-oferta-vacants.pdf`
- Alt Pirineu i Aran: `APA-SEC-dificil-cobertura-oferta-vacants.pdf`
- Barcelonès: PDF nominal de 31/10/2025.
- Catalunya Central: `CCE-SEC-dificil-cobertura-oferta-vacants.pdf`, amb parsejador especial.

**Limitacions constatades en el codi i README:** l'script esborra els PDF un cop analitzats i envia notificacions externes, sense registrar les ofertes històriques en arxius del repositori. El cercador de codi GitHub només ha trobat la referència als PDF i al scraper, **cap corpus històric exportat**. L'autor documentava que li faltava l'enllaç del **Maresme–Vallès Oriental** i que esperava el del **Penedès**, a data del desenvolupament; això reflecteix una mancança del *seu scraper*, **no absència de places en aquests SSTT**.

**Resultat de la via GitHub de tercers:** font contemporània corroborada, **0 nous identificadors de plaça recuperats**.

## 2. Wayback CDX — reintent deliberat amb més temps d'espera

La documentació tècnica de Wayback recomana 40–60 segons de timeout perquè el CDX pot ser lent:
- https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md
- https://github.com/browser-use/browser-harness/blob/main/agent-workspace/domain-skills/wayback-machine/scraping.md

Es va crear i executar en runner públic el [workflow 38297150708](https://github.com/hectorPascualC/ustec-dc-historic-2025-2026/actions/runs/38297150708), amb **tres URL originals**: PDF nominal de 07/11/2025 del Barcelonès, PDF mutable de Vallès Occidental i PDF mutable de Maresme–Vallès Oriental. Paràmetres: `from=20251101`, `to=20260301`, `filter=statuscode:200`, `limit=8`, `collapse=digest`, espera fins a **65 segons**, només una petició per URL i pausa de 2 segons.

Resultat: **tres respostes HTTP 503** en aproximadament **5,2 segons** cadascuna, **zero captures**. Com que el servidor retorna un 503, augmentar el timeout no soluciona aquest tipus concret de fallada. **No és prova que no existeixin captures històriques.**

Fitxer de dades auditat: [exports_wayback/RESUM_CDX_65S.json](exports_wayback/RESUM_CDX_65S.json).

## 3. Arquivo.pt — consulta *full-text* al lloc de només buscar URL exactes

Endpoint oficial públic: `https://arquivo.pt/textsearch`, consultat amb paràmetres `q`, `from`, `to` i `siteSearch`, segons la seva documentació.

- `"dificil cobertura" "627"` entre novembre 2025 i març 2026: **0 resultats**.
- `"dificil cobertura" "507"`: **0 resultats**.
- `"GENSEC_2526"`: **0 resultats**.
- Consulta de control `educacio` amb `siteSearch=educacio.gencat.cat`, anys 2025–2026: **0 resultats**.
- Consulta general `dificil cobertura`, 2025–2026: **6 resultats**; examinats i no són convocatòries catalanes. El resultats provenen principalment de pàgines portugueses i brasilenyes, i algunes captures tenen timestamp de gener 2025.

**Conclusió:** el rastreig accessible a Arquivo.pt no ofereix un fons útil de les convocatòries catalanes en aquest mostreig; no es pot considerar exhaustiu ni fer-ne un zero d'ofertes.

## 4. Cerca documental especialitzada de territoris sense places

S'han provat cerques dirigides a PDF històrics i mirrors en sindicats, repositoris GitHub, Docsity/Scribd, Telegram públic, blogs i índexs generals; les coincidències verificades són de períodes diferents, d'altres especialitats, d'altres comunitats autònomes o de documents del curs 2026–2027. **No s'ha acreditat cap identificador nou** dintre dels territoris pendents ni s'han afegit falsos positius.

## 5. Control de qualitat, corpus i resultat

- **32 identificadors provisionals** a [cens V23](cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V23_32IDS.csv): 19 de 507, 12 de 627 i 1 F57-507.
- **23 amb rastre d'oferta original indexada** i 9 únicament amb resultat indexat. Aquestes categories **no certifiquen publicació exacta ni exhaustivitat**.
- **0 territoris-mes certificats** com a exhaustius.
- Els fitxers de resultats publicats contenen només URL, metadades i codi de plaça, **sense dades personals de candidats/adjudicataris**.
- **No s'han d'automatitzar bucles intensius contra un CDX amb 503 repetits**: es prioritzen altres fonts.
- No s'han fet despeses noves amb proveïdors de navegador.

**Veredicte V25:** PASS per verificació de l'existència d'un tercer seguiment contemporani i diagnòstic reproduïble de Wayback; **FAIL per assolir cens històric exhaustiu**. Cap plaça nova. Pendents: rastres web/sindicals originals alternatius, possibles còpies de documents guardats externament, i el creuament de places desertes i republicacions entre 12 àmbits.
