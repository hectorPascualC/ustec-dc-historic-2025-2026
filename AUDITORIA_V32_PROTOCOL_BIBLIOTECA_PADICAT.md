# AUDITORIA V32 — represa del protocol PDF històrics de la Biblioteca i PADICAT

**Data:** 12/10/2026. **Període:** 01/11/2025–28/02/2026. **Especialitats:** 507, 627, F57, F87. **Àmbit:** 11 SSTT i Consorci Educació Barcelona.

## 1. Recuperat de la Biblioteca de ChatGPT

S'ha recuperat el document operatiu **`REFERENCIA_RECUPERACIO_HISTORICA_PDF_DC_507_627_F57_F87.md`**, v1.0 del 12/10/2026, i la carpeta **`DC Arxius Novembre2025 Febrer2026`**:

- `README_ARXIUS_DC.md`
- `recover_official_dc.py`
- `recover-historic-offers.yml`
- `probe_edubcn_history.py`
- `probe-edubcn-history.yml`

La investigació d'aquest repositori és **posterior** al protocol en algunes fases i ha arribat a 32 identificadors provisionals, no els 28 que hi consten com a estat inicial. La matriu continua sense certificació exhaustiva (**0/48**).

El protocol exigeix conservar: URL original, URL arxivada, data de captura, data **real** de publicació si està provada, SHA256 quan hi ha PDF, tipus de document (oferta/resultat) i grau d'evidència A/B/C/D/X. **Ni la data d'inici ni la data de captura es fan passar per publicació.**

## 2. PADICAT: primer intent nou des del runner de GitHub

L'Arxiu Web de Catalunya confirma un cercador de captures i preservació pública d'informació web: https://padicat.cat/ .

Codi nou: `src/probe_padicat_historic_v32.py`. Execució real: [Actions 38303598097](https://github.com/hectorPascualC/ustec-dc-historic-2025-2026/actions/runs/38303598097). Sortida: [exports_padicat/PADICAT_V32_PUBLIC_INTERFACE.json](exports_padicat/PADICAT_V32_PUBLIC_INTERFACE.json).

**Resultat:** `net::ERR_CONNECTION_RESET` a `https://padicat.cat/` des del Chromium del runner, sense cap resposta HTTP de la portada ni cerca de PDF realitzada. **Bloqueig tècnic, no prova d'absència.**

## 3. Nova ruta descoberta, provada parcialment: visor de captures PADICAT

S'ha localitzat i verificat independentment el **visor real PADICAT Wayback**, documentat per tercers i present en fonts públiques:

- [Historial d'Educació](https://wayback.padicat.cat/wayback/*/https://educacio.gencat.cat).
- [Control independent d'un web preservat](https://wayback.padicat.cat/wayback/*/efes.cat).
- L'accés al primer mostra un calendari amb anys **2021–2023** i captures de 2023. **No es mostra 2025–2026 en aquest recurs exacte**, cosa que **no prova** que altres URL o PDF no hi siguin.
- La cerca d'un PDF concret nominal del **07/11/2025** al mateix visor (`Barcelones-SEC-dificil-cobertura-oferta-vacants_07112025.pdf`) ha retornat `target_unreachable` a la passarel·la de lectura. **No se n'ha descarregat cap PDF històric.**

## 4. Endpoint CDX PADICAT localitzat en codi públic de tercers

Recuperació de la ruta exacta de l'índex, sense inventar endpoints, en dos repositoris públics:
- https://github.com/overbrowsing/wasteback-machine/blob/main/src/archives/padicat/padicat.js documenta `https://wayback.padicat.cat/cdx?url=${url}`, TimeMap i reproducció de captures.
- https://github.com/nabertronic/pastpage/blob/main/extension/src/core/providers/padicat.ts documenta el mateix host i visor.

S'han provat **3** consultes puntuals de CDX des de la passarel·la pública:
1. URL de domini `https://educacio.gencat.cat` 2025–2026.
2. PDF oficial nominal del 07/11/2025.
3. Prefix del mateix domini amb filtre de ruta DC.

**Totes tres han retornat `invalid_redirect_url` a la passarel·la**, no un llistat CDX llegible ni un zero verificat. **No es considera revisat exhaustivament PADICAT.**

## 5. Estat i següent ordre del protocol recuperat

- **P0, PDFs nominals i fragments de cercador:** V20–V23 ja han donat **17 IDs corroborats del Barcelonès** i **una plaça 627 nova al Vallès Occidental**; mantenir textos i PDF complets com a evidències diferents.
- **P1, PADICAT:** visor i CDX localitzats, però l'accés automatitzat és **inconclús**; cal provar la recuperació de captures del **recurs concret** en altres vies públiques, sense afirmar inexistència.
- **P1, Common Crawl:** en lloc de només consultar CDXJ, buscar coincidència verificable de `filename`, `offset` i `length` i recuperar el registre **WARC** amb HTTP Range; **no s'ha aconseguit cap registre per a aquestes ofertes** en les proves anteriors, per tant no fingir una descàrrega.
- **P2, revisions internes de PDF:** comprovar **incremental updates** (`%%EOF`, `/Prev`, estructures xref), i amb PDFResurrect quan hi hagi indicis; només recupera revisions dins el **mateix fitxer**, no còpies reemplaçades completament al servidor. Referència: https://github.com/enferex/pdfresurrect .
- **P3, headers i ETag:** informació forense subsidiària, no mètode autònom de recuperar bytes antics.

**Veredicte:** PASS per localitzar i reprendre el **protocol preexistent**, recuperar una URL de visor PADICAT real i documentar l'API CDX; **FAIL** per recuperar nou PDF original i per a l'objectiu del cens històric complet. **32 IDs** provisionalment documentats, **0 IDs nous** durant V32, **0/48** territori-mes exhaustius.

No s'han utilitzat credencials, fet compres, accedit a dades privades ni descarregat dades personals.
