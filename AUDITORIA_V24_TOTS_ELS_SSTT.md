# AUDITORIA V24 — revisió de tots els SSTT + EDUBCN

**Data de recerca:** 12/10/2026.  
**Objectiu:** cens històric de totes les ofertes originals de difícil cobertura **507, 627, F57, F87** i codis mixtos amb publicació entre **01/11/2025 i 28/02/2026**. Inclou places desertes, retirades i republicacions.

## 1. Resultat de la ronda V24 (accés real a totes les fonts oficials vives)

Workflow: https://github.com/hectorPascualC/ustec-dc-historic-2025-2026/actions/runs/38295975441

- **12 àmbits revisats** (11 serveis territorials i Consorci d'Educació de Barcelona).
- **37 pàgines oficials HTTP 200/200** (primària/segon nivell de DC, menú territorial, secundària i enllaços PFI/IFE trobats).
- **30 enllaços a PDF DC actuals**, els **30 accessibles i llegibles** en el runner públic de GitHub.
- **0 PDF actuals amb prova automàtica de coincidència entre els codis objectiu i dates del període**.
- **0 places noves acreditades** després d'aquesta ronda. **32 identificadors provisionals** continuen al cens.
- No s'ha demostrat cobertura exhaustiva de cap combinació territori-mes. **0 de 48** certificades.

**Atenció:** els 30 PDF són la **fotografia actual de les URL dels SSTT el 12/10/2026**, no les versions del novembre de 2025 a febrer de 2026. El resultat negatiu en aquestes versions **no certifica cap 0 històric**.

## 2. Taula de totes les àrees, amb comprovació efectiva de pàgines i PDF vius

| Àmbit | Pàgines accessibles | PDF DC actuals consultats | ID històrics coneguts | Cobertura exhaustiva |
|---|---:|---:|---:|---|
| Alt Pirineu i Aran | 4 | 4 | 0 | No |
| Baix Llobregat | 3 | 2 | 9 | No |
| Barcelonès | 4 | 4 | 17 | No |
| Catalunya Central | 3 | 2 | 0 | No |
| Girona | 3 | 2 | 0 | No |
| Lleida | 4 | 4 | 3 | No |
| Maresme–Vallès Oriental | 3 | 2 | 0 | No |
| Penedès | 3 | 2 | 1 | No |
| Tarragona | 3 | 4 | 0 | No |
| Terres de l'Ebre | 3 | 2 | 0 | No |
| Vallès Occidental | 3 | 2 | 2 | No |
| Consorci d'Educació de Barcelona | 1 | 0 (llistat dinàmic REST separat) | 0 | No |
| **Total** | **37** | **30** | **32** | **No** |

Tots els zeros d'ID volen dir **«cap identificador del període recuperat de manera verificable»**, no inexistència real de publicacions.

## 3. Vies d'investigació històrica diferenciades

**A) Webs i PDF actuals:** revisats sistemàticament, registres en `exports_territorial/`. Les URL estables de resultats i ofertes són **mutables** i moltes s'han sobreescrit amb curs 2026–2027.

**B) PFI/IFE:** la captura de menú territorial i subpàgines DC detecta enllaços PFI per Alt Pirineu i Aran i Lleida; altres SSTT no tenen enllaç de PFI local recuperat en aquesta passada. Això **no** permet concloure que no publiquessin ofertes F57/F87. Estan inclosos els PDF PFI enllaçats, sense inferir dates antigues.

**C) EDUBCN:** el seu llistat és una app AngularJS i no exposa PDF directes a la pàgina. Anteriorment es va verificar `/pdc_rest/convocatories/ca` amb **83 registres visibles** l'octubre 2026 i cap fila amb data nov2025–feb2026. El frontend consulta la llista viva, sense paràmetre d'històric publicat. **No prova la inexistència del registre administratiu de 2025.**

**D) Arxius públics:** l'auditoria prèvia va comprovar Wayback, Common Crawl i Arquivo.pt. Hi va haver 503/timeout i cap PDF històric recuperat; la manca de captura en aquestes peticions **no és una prova de 0**.

**E) Indexació textual residual:** els PDFs nominals del Barcelonès han aportat **11 llistats i 60 aparicions d'identificadors** entre 11/2025 i 02/2026, que corresponen a **17 IDs únics ja al cens**; el Vallès Occidental aportà l'ID nou **627-19/11** (Nicolau Copèrnic), 627 sencera, amb termini de novembre i resultat fora de borsa. Són proves de text original indexat, no PDF original immutable.

## 4. Indicis nous examinats però NO comptats

En una **versió històrica indexada** del document de resultats de Tarragona del curs 2025–2026 apareixen dues referències a **507 de l'Institut Francesc Vidal i Barraquer**, etiquetades **103-43005704** (adjudicada telemàticament) i **104-43005704** (alta del titular). També s'hi troben referències a **627** de l'Institut Antoni Ballester i l'Institut Baix Camp, marcades com a adjudicades telemàticament, **sense dates de publicació**.

S'ha localitzat una **còpia antiga penjada a Docsity el 31/10/2025** de l'oferta original de Tarragona en què ja consten les dues places 507, amb inici a **octubre de 2025**. **Aquestes referències no s'incorporen al cens de novembre-febrer** perquè no hi ha cap evidència fiable de republicació dins la finestra. La decisió evita inflar artificialment el cens a partir de resultats sense data.

Font del rastre històric de Tarragona: https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/tarragona/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/TAR-SEC-dificil-cobertura-vacants-cobertes.pdf
Còpia indexada publicada anteriorment al període: https://www.docsity.com/es/docs/dificil-cobertura-en-diferentes-contextos/14696135/

## 5. Evidència PFI de correspondència d'especialitats, fora del període

El document oficial de resultats PFI del **Vallès Occidental del juliol de 2025** identifica **F87** amb ordinària **627** a l'Institut de Badia del Vallès i **F57** amb ordinària **507** al Baix Llobregat (Torre Roja) en documents oficials de juliol de 2025. Això confirma les equivalències **per aquests registres específics**, però no suposa cap oferta posterior al novembre sense una prova de nova publicació. Aquestes places de juliol **s'exclouen** del cens temporal.

## 6. Fitxers de reproducció i auditoria

- [Matriu territorial V24, amb 32 ID provisionals](cens/MATRIU_V24_TOTS_SSTT_32IDS.csv)
- [Fitxer JSON de l'auditoria territorial](exports_territorial/AUDITORIA_PASADA_TERRITORIAL.json)
- [37 pàgines territorials provades, HTTP i URL](exports_territorial/SSTT_PAGINES.csv)
- [30 PDF actuals, codis, dates, SHA-256 i resultat](exports_territorial/SSTT_PDFS.csv)
- [Enllaços a les fonts oficials](exports_territorial/SSTT_ENLLACOS.csv)
- [Cens únic V23 de 32 ID](cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V23_32IDS.csv)
- [Auditoria V23 del nou cas Vallès Occidental](AUDITORIA_V23_32IDS_NICOLAU_COPERNIC.md)

**Veredicte:** PASS en cobertura **de la consulta a les fonts vives dels 12 àmbits**; FAIL en la certificació del **cens històric exhaustiu nov2025–feb2026**. Aquest document no declara esgotades totes les vies externes, ni equipara els 32 identificadors provisionalment corroborats amb el total de places reals.
