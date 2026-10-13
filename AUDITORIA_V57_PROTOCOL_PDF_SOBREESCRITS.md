# AUDITORIA V57 — Protocol de recuperació de PDF sobreescrits, contrast d'índex antic i ampliació temporal

**Data de consulta:** 13/10/2026. **Abast:** Catalunya, difícil cobertura 507/627/F57/F87, ofertes publicades 01/11/2025–28/02/2026.

## Manual metodològic seguit

Document original a la Biblioteca: `REFERENCIA_RECUPERACIO_HISTORICA_PDF_DC_507_627_F57_F87.md`, versió 1.0 de 12/10/2026. S'aplica la seva jerarquia P0: document original amb nom datat > testimoni de cerca indexat, i P1: arxius web CDX/Wayback/PADICAT/Common Crawl/Arquivo.pt. Sempre se separen data de publicació, data de captura, data d'inici i data del resultat. El protocol és una referència metodològica, no una prova d'execució. No es publica el fitxer privat de Biblioteca.

## 1. Contrast contemporani d'una URL oficial reutilitzada: Lleida

PDF oficial: https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/lleida/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/LLE-SEC-dificil-cobertura-vacants-cobertes.pdf

- El resultat de cerca obtingut amb la consulta `"LLE-SEC-dificil-cobertura-vacants-cobertes.pdf" "2025" "2026" "507"` conserva contingut etiquetat **«Curs 25-26»**, amb les files de resultat **`2025/SEC/266` (507, Institut Mollerussa)** i **`2025/SEC/259` (627, Institut Caparrella)**.
- La recuperació actual per la **mateixa URL** mostra un PDF de **«Curs 26-27»**, amb codis `2026/SEC/102`, `2026/SEC/089`, etc. Això prova la divergència entre **text indexat antic** i **recurs viu més nou**. Les dates de recerca/indexació NO acrediten la data exacta de publicació dels casos antics.
- **Atenció de control:** eines de visualització de PDF poden reutilitzar vistes inconsistents entre versions servides en el mateix URL. Per això les captures de pantalla no s'empren per establir la identitat binària del PDF anterior. No s'ha recuperat ni hashjat el binari original 25-26.
- Els dos identificadors 507/627 ja són presents a V49; **0 identificadors nous**, cap dada personal reproduïda.

## 2. Barcelona/Barcelonès — arxiu nominal i índex persistent

PDF nominal: https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/barcelones/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/BCO-SEC-dificil-cobertura-oferta-vacants_27022026.pdf

- La cerca pública encara ofereix fragments d'una versió del **27/02/2026** amb el cas **`19357285` 627, Institut Puig Castellar**, termini **01/03/2026**.
- L'URL PDF original actual retorna **HTTP 404** en la comprovació realitzada. Un 404 avui no desmenteix la publicació del PDF amb nom datat.
- La consulta independent a `cens/REPUBLICACIONS_BCO_V22_11_LOTS_VERIFICATS.csv` i `cens/INDEX_PDFS_BCO_V22_11_LOTS.csv` confirma que aquest **lot del 27/02** i els seus identificadors ja estaven inventariats. **No és nova plaça ni nou lot**; és corroboració externa.

## 3. Girona — URL mutable, sense nova recuperació

`GIR-SEC-dificil-cobertura-vacants-cobertes.pdf`: la V16 havia descrit un rastre d'indexació 25-26 i un contingut actual 26-27. Les cerques d'aquesta ronda no han recuperat un PDF original 25-26 ni una nova fila amb prova temporal; **cap identificador afegit**.

## 4. Ampliació de la finestra de captura PADICAT

Per no limitar captures a febrer/març de 2026, s'han provat consultes CDX de **01/03/2026 a 13/10/2026** sobre URLs oficials originals de Lleida, Girona, Maresme–Vallès Oriental i Barcelonès. Resultats:
- 6 consultes amb URL `https://...` completa han rebut `invalid_redirect_url` al client de consulta, **error tècnic**, no «0 captures».
- 3 consultes amb representació normalitzada del domini sense esquema han rebut `empty_content`, sense registre de captura recuperable. Això **no és una certificació d'absència de captura**.

Segueix essent prioritària la recuperació real dels bytes des de PADICAT, Wayback, Common Crawl o altres fonts, no pas convertir snippets en PDF complets.

## 5. Auditoria

- Cens: **36 identificadors** provisionals (21 de 507, 14 de 627, 1 F57-507).
- **0 nous identificadors**, **0** binaris de PDF territorial 2025-26 recuperats en aquesta ronda.
- **0/48** blocs territori-mes acreditats com a exhaustius.
- **PASS**: control creuat de sobreescriptura textual Lleida i supervivència d'indexació PDF nominal Barcelonès.
- **PARTIAL/BLOCKED**: ampliació de captures en fonts PADICAT.
- **FAIL**: cens territorial complet; no es poden certificar places no publicades, desertes o retirades.

Registre de contrast: `exports_official/V57_CONTRAST_PDFS_SOBREESCRITS.csv`.

No es conserven noms, DNI, barems ni adreces de docents.
