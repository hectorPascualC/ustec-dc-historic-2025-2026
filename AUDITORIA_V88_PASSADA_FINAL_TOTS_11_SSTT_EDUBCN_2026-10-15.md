# AUDITORIA V88 — passada integral: 11 SSTT + EDUBCN

**Tancament de la passada: 15/10/2026 (Europa/Madrid).**

**Missió:** investigar, sense exclusions territorials, les ofertes docents de difícil cobertura de les especialitats 507, 627, F57, F87 i combinacions documentades **publicades** a Catalunya entre **01/11/2025 i 28/02/2026**. Diferenciar dates de publicació, termini de sol·licitud, incorporació, resultat, repetició de l'oferta i captura d'arxiu.

**Regla de prudència:** aquesta passada és **completa quant als 12 àmbits revisats**, però **NO és un cens històric exhaustiu certificat** perquè manquen versions dels anuncis retirats/sobreescrits. Font de protocol `REFERENCIA_RECUPERACIO_HISTORICA_PDF_DC_507_627_F57_F87.md` v1.0 (Biblioteca).

## 1. Feina real executada després de V85

**V86 — revisió directa dels 30 PDF oficials dels 11 serveis territorials**
- Fonts exactes: [inventari V24](exports_territorial/SSTT_PDFS.csv), [extracció actual V86](exports_territorial/SSTT_V86_PDF_DATES_2025_11_TO_2026_02.json).
- **30/30** PDF descarregats, signatura `%PDF-`, text analitzat amb PyMuPDF i hash SHA-256; **11/11** SSTT tractats.
- Cerca de dates del rang **01/11/2025–28/02/2026** en formats `D/M/YYYY`, `DD/MM/YYYY`, `YYYY-MM-DD`, amb context de les especialitats **507/627/F57/F87**. **0 coincidències** en les versions que serveix ara la Generalitat.
- **13/30 PDF tenen SHA-256 diferent** del mateix URL al primer inventari V24 del **12/10/2026**. Això prova **diferència de bytes** i la necessitat de preservar la versió, **NO** prova que hagi canviat l'oferta ni permet retrocedir al novembre de 2025.
- Una consulta textual indexada de Baix Llobregat continua mostrant fragments `13/1/2026` a `PENDENTS_BLL-SEC...`; el PDF actual descarregat a V86 **no** conté cap data del període, mostra del perquè no s'han de confondre **snippets indexats antics** amb la versió PDF actual ni atribuir publicació sense arxiu.

**Cerques independents a tots els àmbits**
- Proves de consulta per **cada SSTT**, amb nom territorial, ruta oficial, `507`, `627`, `F57`, `F87`, `2025`, `2026`, i mesos de novembre–febrer: cercadors de pàgines web i PDF, índexs, sindicats, miralls.
- Fonts secundàries contrastades: [V85, Girona/Tarragona](AUDITORIA_V85_GIRONA_TARRAGONA_MIRALLS_2025_26.md) i [vuit exclosos](cens/V85_EVIDENCIES_EXTERNALS_GIRONA_TARRAGONA_NO_COMPTADES.csv). Els exemples recuperats eren d'octubre 2025 o cursos anteriors, sense prova de nova oferta dins la finestra.
- Exemples de fonts conegudes **que no són proves de noves places**: el catàleg estatal SEPE de professions de difícil cobertura, adjudicacions d'estiu, PDF territorials actuals 2026–27, i textos generals de normativa. No convertir la coincidència «627» en una oferta de sistemes.

**EDUBCN**
- Anàlisi històrica prèvia auditada completa per a dues captures PADICAT: **248 PDF** de gener 2026 i **309 PDF addicionals d'octubre**: **557 URL úniques**. [V82](exports_padicat/EDUBCN_V82_FULL_OCT_DELTA_2025_26.json), [V84](exports_padicat/EDUBCN_V84_2025_26_COURSE_PDF_REAUDIT.json), [V74](AUDITORIA_V74_EDUBCN_PROVA_DATA_PUBLICACIO_I_CENS_CONSOLIDAT.md).
- Quatre originals 507/627 amb data de publicació del portal acreditada per HTML+JS+API arxivats a PADICAT. **Cap prova de primera publicació absoluta** per als dos PDF ITB datats al desembre però publicats al portal al gener.
- **No** existeix una captura del febrer exhaustiva entre aquests dos inventaris.

## 2. Matriu territorial de la passada

`IDs` vol dir **identificadors provisionals documentats al cens**, no totes les places realment publicades. `PDF` és el nombre d'enllaços oficials vius revisats al V86; `Δ SHA` els bytes diferents respecte V24. `Partial` compta mesos amb alguna prova histórica útil; **no equival a mes complet**.

| SSTT / àmbit | IDs documentats | PDF actuals comprovats | Δ SHA | Mesos amb proves parcials | Mesos sense corpus suficient |
|---|---:|---:|---:|---:|---:|
| Alt Pirineu i Aran | 0 | 4 | 2 | 0 | 4 |
| Baix Llobregat | 9 | 2 | 0 | 4 | 0 |
| Barcelonès | 17 | 4 | 0 | 4 | 0 |
| Catalunya Central | 0 | 2 | 1 | 0 | 4 |
| Consorci d'Educació de Barcelona (EDUBCN) | 4 | — (API/PADICAT) | — | 2 | 2 |
| Girona | 0 | 2 | 1 | 0 | 4 |
| Lleida | 3 | 4 | 3 | 2 | 2 |
| Maresme–Vallès Oriental | 0 | 2 | 0 | 0 | 4 |
| Penedès | 1 | 2 | 1 | 1 | 3 |
| Tarragona | 0 | 4 | 2 | 0 | 4 |
| Terres de l'Ebre | 0 | 2 | 1 | 0 | 4 |
| Vallès Occidental | 2 | 2 | 2 | 1 | 3 |
| **Total** | **36** | **30** | **13** | **14** | **34** |

**0/48** blocs territori×mes complets: **14 PARTIAL**, **34 BLOCKED**. Un 0 d'ID indica que **no se n'ha recuperat cap**, mai que sigui una prova de zero convocatòries reals.

Fonts de dades calculades i testejades automàticament:
- [V87, 12 registres territorials CSV](cens/V87_REVISIO_COMPLETA_12_AMBITS.csv).
- [V87, 48 registres territori×mes CSV](cens/V87_MATRIU_48_TERRITORI_MES.csv).
- [V87, JSON amb els 13 canvis de SHA-256](exports_territorial/SSTT_V87_AUDITORIA_COMPLETA_12_AMBITS.json).
- [Script V87 de conciliació reproduïble](src/audit_12_territories_48_months_v87.py) i [execució GitHub Actions](.github/workflows/audit-full-12-areas-v87.yml).

## 3. Cens provisional i quatre dates del portal oficial corroborades

[Cens consolidat V73](cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V73_36IDS.csv): **21 de 507**, **14 de 627**, **1 combinació F57–507**.

| Codi EDUBCN | Especialitat | Data de publicació que mostrava el portal arxivat | Observació |
|---|---|---|---|
| `GENSEC_147` | 627 | **05/12/2025** | Escola del Treball, PDF original preservat |
| `GENSEC2526_167` | 507 | **21/01/2026** | Pedralbes, PDF original preservat |
| `GENSEC_2526_145` | 507 | **22/01/2026** | ITB; PDF original creat 01/12/2025, termini inicial desembre |
| `GENSEC_2526_149` | 627 | **22/01/2026** | ITB; PDF original creat 10/12/2025, jornada 0,25 |

Les dates **són les del portal de gener arxivat**, no la primera data absoluta de publicació si hi va haver convocatòria o republicació anterior. **32/36** IDs no tenen data de publicació certificada. Girona/Tarragona continuen amb evidències de resultats històrics **no datats com a publicació dins la finestra**, [V85](AUDITORIA_V85_GIRONA_TARRAGONA_MIRALLS_2025_26.md).

## 4. Auditoria de completitud, honestedat i privacitat

| Control | Conclusió |
|---|---|
| Repassada per **tots els 11 SSTT** | **PASS** en consulta de fonts oficials vives, 30/30 PDF |
| Revisió **EDUBCN** | **PASS** per al corpus de dues captures efectivament recuperat; **NO** per a tots els mesos |
| Fonts externes i resultats històrics | **PASS** com a triatge de fonts; no aporta anuncis addicionals certificats |
| Confrontació cens V73, V69, V86, V82 | **PASS**, conciliada a V87 amb **12 àrees i 48 mesos** |
| Noves ofertes dins la finestra trobades en aquesta passada | **0** |
| Prova de no-publicació en un territori/mes | **Cap** |
| Recuperació exhaustiva de totes les publicacions Catalunya 01/11–28/02 | **NO ASSOLIDA: 0/48** |

**Limitacions irreductibles d'aquesta ronda:** les URL PDF dels SSTT són mutables, 13 canvien de bytes fins i tot en pocs dies; els índexs d'arxiu consultats no conserven còpies de molts anuncis antics; els resultats poden quedar sobreescrits; un PDF escanejat podria requerir OCR; i els mesos no fotografiats per PADICAT poden contenir convocatòries efímeres. No inventar ni el nombre de vacants perdudes ni els seus centres.

**Privacitat:** no s'han publicat noms, identificadors personals ni barems de candidatures o adjudicataris. Únicament codis de places i dades de centres divulgades públicament.

**Resultat de la petició actual:** **passada pels 12 àmbits FINALITZADA i auditada**, sense cap ID nou acreditat. **La missió de cens històric absolutament exhaustiu continua oberta** mentre no es disposi de les versions originals dels anuncis retirats.

