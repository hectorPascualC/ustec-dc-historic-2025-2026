# AUDITORIA V83 — 557 URL PDF preservades a PADICAT i contrast dels SSTT Girona/Tarragona

**Comprovació 14/10/2026.** **Missió:** cens d'ofertes docents de difícil cobertura de les especialitats **507, 627, F57, F87** publicades entre **01/11/2025 i 28/02/2026**, onze SSTT més EDUBCN. Protocol editorial i documental: `REFERENCIA_RECUPERACIO_HISTORICA_PDF_DC_507_627_F57_F87.md` (Biblioteca).

## 1. Nou corpus de PDF de l'octubre (V81)

S'han consultat dos prefixos reals del Consorci d'Educació de Barcelona a PADICAT per al període posterior al gener:

- `https://www.edubcn.cat/rcs_gene/seleccio/`
- `https://www.edubcn.cat/rcs_gene/extra/03_nomenaments_dificil_cobertura/`

[V81, dades](exports_padicat/EDUBCN_V81_POST_JAN_ARCHIVED_PDFS.json): 393 captures de recursos dins aquestes carpetes entre febrer i octubre, **390 URL de PDF úniques** amb HTTP 200 indexat. **65** PDF amb noms candidats inspeccionats, **0** amb prova de nova oferta 2025–2026. Limitació V81: comparava els 390 URL només amb els **33 originals GENSEC** de la V45, no amb tot el corpus de 248 PDF de gener; per tant, la xifra «390 no continguts al conjunt de 33» no és «390 nous respecte a gener».

## 2. V82: comparar corpus gener/o​ctubre complets i validar el delta real

[**Resultat V82**](exports_padicat/EDUBCN_V82_FULL_OCT_DELTA_2025_26.json) | [Script reproduïble](src/edubcn_archive_oct_delta_full_v82.py) | [workflow](.github/workflows/edubcn-oct-delta-v82.yml).

| Control | Resultat |
|---|---:|
| PADICAT 29/01/2026, CDX registres totals (inclou no PDF) | **252** |
| PADICAT 29/01/2026, URL PDF úniques HTTP 200 | **248** |
| PADICAT 04/10/2026, CDX registres totals | **390** |
| PADICAT 04/10/2026, URL PDF úniques HTTP 200 | **388** |
| URL presents a les dues dates | **79** |
| URL amb mateix nom però digest d'arxiu modificat | **0** |
| PDF nous a l'octubre respecte del corpus de gener | **309** |
| Descàrregues reals del delta, amb validació PDF i SHA256 | **309/309** |
| Errors en inspecció de contingut | **0** |
| Documents nous amb coincidència textual de **507/627/F57/F87 + curs 2025-26 + DC** | **0** |
| Total URL PDF úniques gener ∪ octubre | **557** |

**Control aritmètic:** 248 + 388 - 79 = **557**, i 388 - 79 = **309**. Els 248 PDF de gener ja s'havien auditat totes les pàgines a [V55](AUDITORIA_V55_TANCAMENT_CORPUS_PADICAT_EDUBCN_248PDF.md) i [V56](exports_padicat/EDUBCN_V56_FULL_PAGES.json), amb quatre ofertes 507/627 originals ja censades i cap més.

La V82 ha analitzat **tots** els PDF amb URL nova o digest diferent a la captura del 4 d'octubre, no només els 65 seleccionats per nom a V81. Els 309 PDF nous mostren **0 candidats detectats**. Això és un PASS de completitud **sobre el corpus comparat d'aquestes dues captures**, no sobre els anuncis històrics que podrien haver aparegut i desaparegut **entre** aquestes captures o en un altre servidor/ruta. La detecció és per text de PDF: OCR d'imatges escanejades **no** efectuat; un PDF sense les paraules cercades podria escapar a les regles, per tant el recompte 0 és «0 candidats segons l'auditoria textual», no una certificació d'inexistència absoluta.

## 3. Fonts oficials indexades Girona i Tarragona: residus de 2025–26 vs PDF actual

Una nova cerca específica de 507/627 ha retornat **fragments indexats** de PDF de resultats antics:

- **Girona**, URL mutable: `https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/girona/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/GIR-SEC-dificil-cobertura-vacants-cobertes.pdf`. L'índex històric conserva, entre d'altres, el codi **`149S/2025-2026`**, especialitat **627**, centre **Institut Sa Palomera (Blanes)**, amb **data d'inici 13/10/2025** i fi prevista 15/11/2025. **Fora del període si el criteri és data d'inici**, però la **data de publicació real no consta al fragment** i no s'ha acreditat que entrés dins de novembre–febrer. La URL actual, inspeccionada com a PDF real l'14/10/2026, retorna principalment **resultats del curs 2026–27**; no és el binari històric antic.
- **Tarragona**, URL mutable: `https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/tarragona/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/TAR-SEC-dificil-cobertura-vacants-cobertes.pdf`. L'índex antic conserva files de **627** per l'Institut Antoni Ballester (Mont-roig) i Institut Baix Camp (Reus), i de **507** per l'Institut Francesc Vidal i Barraquer; algunes files tenen estat «Adjudicada telemàticament» o «Alta titular», sense data de publicació de l'oferta. La URL actual serveix un PDF de resultats actualitzat d'un altre corpus. **No sumar aquests registres al cens de novembre–febrer sense una data certificada o algun anunci de l'interval**.

Aquests testimonis corroboren l'existència de llistats 2025–26 **anteriors al document actual** als dos SSTT, però la data de resultat/inici no és la data de publicació ni prova per si sola una nova oferta en el període. Estatus **D/C (resultat indexat)**, no **A/B original PDF antic recuperat**. No reproduir dades personals que apareixen als PDF de resultats.

## 4. Estat de l'objectiu

- Cens provisional V73: **36 identificadors** — 21 de 507, 14 de 627 i 1 F57-507.
- Noves ofertes certificades en V81/V82: **0**.
- Dates de publicació del portal històric EDUBCN verificades: **4**, sense primera publicació absoluta acreditada.
- **0/48** controls territori×mes declarats exhaustius.
- **PASS documental acotat:** les **557 URL PDF** de les dues captures EDUBCN tenen corpus de gener auditat i delta d'octubre validat.
- **PENDENT:** captures d'altres mesos —especialment febrer— i d'altres URL/dominis; anuncis oficials originals dels SSTT amb PDF sobrescrits.

**Pròxima línia més productiva:** localitzar còpies datades o resultats de novembre-febrer fora d'EDUBCN (Girona, Tarragona i altres cinc SSTT sense IDs), evitant repetir els CDX/URL que han retornat errors o zeros en comprovacions acotades. Sense publicar dades personals de candidats.
