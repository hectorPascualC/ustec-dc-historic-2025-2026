# Recuperació històrica de PUBLICACIONS de difícil cobertura (DC)

## Abast

**De l'01/11/2025 al 28/02/2026**, especialitats **507**, **627**, **F57**, **F87** (i aparicions combinades), a onze SSTT i al Consorci d'Educació de Barcelona.

Aquesta branca de recerca no pretén substituir les publicacions oficials per nomenaments ordinaris. La font USTEC es va investigar abans i **no retorna files de procediment `dif`**. Aquest fet no implica que no es convoquessin places DC a la Generalitat.

## Fases automàtiques implementades

1. **Rastreig d'URL d'ofertes i resultats** històrics confirmats anteriorment (Barcelonès, Baix Llobregat i Penedès) i cerca per prefix de documents dels onze SSTT.
2. **Consulta d'arxius públics**: Wayback CDX, Arquivo.pt URL search i índexs Common Crawl dels quatre períodes principals. Logs de consultes fallides, límits i estat HTTP.
3. **Recuperació i lectura de documents**: valida el `%PDF-`, SHA-256, pàgines i referències a identificadors/especialitats. Evita publicar PDFs o dades personals.
4. **Creuament** amb 28 identificadors històrics coneguts; distingeix documents d'**oferta**, **resultat** i **indeterminats**.
5. **Auditoria independent** amb avisos d'incompletesa. L'absència en un arxiu no es considera una prova de zero places. Les dates de captura **no són**, per si soles, dates de publicació.

## Fitxers de sortida

Un cop executat [el workflow](.github/workflows/recover-historic-offers.yml), `exports_official/` conté:

- `ARXIU_CONSULTES.csv`: peticions, estat, nombre de resultats i errors.
- `ARXIU_CAPTURES.csv`: metadades de captures, que **no** impliquen document recuperat.
- `DESCARREGUES.csv`: PDF recuperats o errors (sense fitxers personals).
- `DOCUMENTS_VERIFICATS.csv`: només PDFs de contingut vàlid, SHA-256, pàgines i codis.
- `EXTRACCIO_DOCUMENTS.csv`: identificadors/especialitats detectats per pàgina; evidència *candidata*, pendent de validar context i data original.
- `AUDITORIA_ARCHIUS_DC.json`: abast, novetats, errors, 48 controls territori-mes i veredicte.

## Execució i costos

Workflow amb execució única per `workflow_dispatch` o una modificació del codi o del workflow. Sense cron. Únicament el runner estàndard de GitHub Actions en repositori **públic**; cap compte de pagament, secret, servei comercial o artefacte facturable. Els CSV es comiten al repositori públic. El processament i la cerca de dades històriques **no garanteix un cens exhaustiu**.

**No introduïu dades personals, correus de professorat ni credencials al repositori públic.**