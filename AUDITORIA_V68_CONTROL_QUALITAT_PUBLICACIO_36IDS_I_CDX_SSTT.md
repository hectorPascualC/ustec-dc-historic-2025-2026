# AUDITORIA V68 — Qualitat de la prova, fonts alternatives i errors Common Crawl (13/10/2026)

## 1. Mandat i criteri

Protocol de Biblioteca: `REFERENCIA_RECUPERACIO_HISTORICA_PDF_DC_507_627_F57_F87.md` v1.0. Recuperació d'ofertes DC i republicacions **publicades** entre 01/11/2025 i 28/02/2026 de 507, 627, F57, F87, 11 SSTT i EDUBCN. **Resultat/adjudicació/data d'inici/captura arxiu/nom PDF no són automàticament data de publicació.**

La base és `cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V49_36IDS.csv`, llegida directament el 13/10/2026.

## 2. Auditoria formal dels 36 identificadors (sense inventar noves places)

| Tipus d'evidència en CSV V49 | Nombre de registres | Límits |
|---|---:|---|
| `oferta_indexada` | **22** | Text d'oferta atribuït a índex antic, generalment PDF original no preservat |
| `oferta_indexada_i_resultat_indexat` | **1** | Dos testimonis textuals, no dues places |
| `resultat_indexat` | **9** | Indici d'adjudicació DC; falta anunci original |
| `api_historic_capturat_i_pdf_original_verificat` | **4** | Ofertes de Consorci Barcelona, PDF original + captura API PADICAT 29/01/2026; data de publicació original encara per corroborar |
| **Total** | **36** | 21 de 507, 14 de 627, 1 F57-507 |

**Camp `data_publicacio_certificada`: 0/36 omplerts.** No s'han de presentar aquests 36 com a *36 publicacions exactes certificades* de novembre–febrer. **12/36** tenen dada al camp `data_termini_coneguda` i **22/36** identifiquen algun fitxer nominal als camps del cens. Són indicis, no certificacions del dia efectiu de publicació.

Distribució territorial del cens (no de totes les ofertes reals):
- Barcelonès 17
- Baix Llobregat 9
- EDUBCN 4
- Lleida 3
- Vallès Occidental 2
- Penedès 1
- Alt Pirineu i Aran, Catalunya Central, Girona, Maresme–Vallès Oriental, Tarragona i Terres de l'Ebre: **cap ID recuperat**, que **NO** equival a absència d'ofertes.

### Contradicció temporal especial

El PDF original de `GENSEC_2526_149`, 627, **jornada 0,25**, indica **fi 31/08/2025** tot i aparèixer a la captura oficial posterior: dades contradictòries; no exportar aquesta data com fi vàlida de la substitució. [V52](AUDITORIA_V52_EDUBCN_RESULTATS_JORNADES_2026-10-13.md).

## 3. V66: consulta de carpetes oficials reals, Common Crawl

Font: [V66](exports_commoncrawl/COMMONCRAWL_V66_TERRITORIAL_PREFIXES.json), [script](src/commoncrawl_territorial_prefixes_v66.py).

Sis carpetes públiques derivades d'enllaços oficials coneguts: secundària a Alt Pirineu i Aran, Maresme–Vallès Oriental, Tarragona i Terres de l'Ebre; ruta PFI–IFE d'Alt Pirineu i Aran; ruta complementària `Provisio-vacants-SPD/` de Catalunya Central (PDF de difícil cobertura verificat en cerca pública, però el cas 507 recuperat era d'agost 2025, **fora d'interval**).

- **30** consultes d'índex previstes (5 col·leccions × 6 carpetes).
- **3** executades, les tres primeres a la carpeta secundària d'Alt Pirineu i Aran: HTTP **504, 502, 502**.
- Aturada de prudència després de tres errors consecutius.
- **0** consultes que hagin acreditat *sense captures*: tots els tres són **BLOCKED**.
- **0** URLs de PDF indexades noves. Les altres **27** consultes continuen **NO EXECUTADES**, no negatives.

## 4. V67: cerca alternativa amb prefixos de noms originals més ajustats

Font: [V67](exports_commoncrawl/COMMONCRAWL_V67_SSTT_PRECISE_PDF_PREFIXES.json), [script](src/commoncrawl_precise_filenames_v67.py).

Prefixos de PDF amb noms habituals que consten als enllaços oficials de V24; sis SSTT sense ID, col·leccions `CC-MAIN-2025-51` i `CC-MAIN-2026-08`.

- **12** consultes previstes, **7** executades, **5** NO EXECUTADES perquè es van acumular errors.
- **Una** consulta de Girona, `CC-MAIN-2025-51`: HTTP **404**, sense captures per aquell prefix d'URL en *aquell índex*, **no cens zero**.
- **Sis** consultes: 502/503/504 → **BLOCKED**, no captures absents.
- Cap captura ni PDF històric descarregat.

**Conseqüència:** la via Common Crawl via API pública de col·leccions presenta fallades de disponibilitat intermitents/sistemàtiques, fins i tot amb prefixos molt acotats. No s'han certificat els sis territoris.

## 5. Altres vies independents examinades aquesta ronda

- **Cercadors externs**: han retornat PDF indexats històrics de Catalunya Central `Provisio-vacants-SPD/ofertes-provisio-SPD.pdf` (fragment 507 amb data agost 2025), Tarragona/Lleida amb snippets 2025–2026 i PDF reusats; els documents en viu poden servir ara contingut 2026–2027. Les dates de l'índex no són la data de publicació.
- **Catalunya Central SPD** és **un altre circuit de provisió de difícil cobertura**, com indica el títol del document, i no s'ha de descartar de la investigació territorial; la mostra trobada, tanmateix, no afegeix ID dins novembre–febrer.
- **Arxius sindicals Asinpre**: 4 arxius mensuals públics `/2025/11/`, `/2025/12/`, `/2026/01/`, `/2026/02/` consultats; a la primera pàgina de les entrades retornades no consta una publicació de DC 507/627 amb enllaç a PDF històric. Poden tenir pàgines addicionals: NO exhaustiu.
- **Control falsos positius**: fonts del SEPE sobre ocupacions generals de difícil cobertura, ofertes d'agost/setembre 2025 i documents de 2026–2027 no es transformen en places del període.

## 6. Control final

| Indicador | Resultat |
|---|---|
| Nous identificadors vàlids | **0** |
| Total cens provisional | **36** |
| Dates de publicació exactes certificades al CSV V49 | **0/36** |
| PDF històrics territorials binaris nous | **0** |
| Controls territori-mes declarats exhaustius | **0/48** |
| V66 consultes bloquejades / no executades | **3 / 27** |
| V67 consultes bloquejades / no executades | **6 / 5** |
| Veredicte de la missió global | **PARCIAL — OBJECTIU EXHAUSTIU NO ACONSEGUIT** |

El resultat negatiu/erroni d'un servei extern no demostra cap zero de convocatòries. No es publiquen noms ni identificadors personals de persones candidates. No convertir IDs de documents de resultat en publicacions d'oferta datades.

## Següent via prioritària verificable

Prioritzar captures històriques d'**HTML oficial amb enllaços datats** i **còpies d'altres dominis o noms de fitxer**, així com més rastres de **resultats/republicacions** del circuit SPD i PFI. No repetir consultes de Common Crawl que només han donat errors 5xx sense nova via d'accés.
