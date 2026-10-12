# Auditoria de tancament de l'execució autònoma — 12/10/2026

## Objectiu

Cens exhaustiu de les **convocatòries publicades** de difícil cobertura de 507, 627, F57 i F87 entre **01/11/2025 i 28/02/2026** per als **11 Serveis Territorials i EDUBCN**, incloent-hi places no adjudicades, retirades i republicacions. **No confondre amb nomenaments o adjudicacions.**

## Fases executades i contrastades

| Fase | Via | Resultat verificat | Objectiu global |
|---|---|---|---|
| 1 | Preparació d'identificadors històrics | Corpus previ amb **28 casos**; d'ells, 19 amb oferta indexada i 9 coneguts només per resultat. | Parcial |
| 2 | Històric USTEC | Endpoint `server_processing2.php` funciona per nomenaments; filtre `dif` retorna 0 registres inclús sense curs. Per tant **USTEC no cobreix les DC**, no s'interpreta com absència real. | Font descartada com a cens |
| 3 | Recuperació sense PDF via estadístiques de plantilla | Indicadors de personal docent, **no** publicacions; no comptabilitzats com a places DC. | No apte |
| 4 | Rastreig d'arxius històrics en GitHub Actions (runner públic) | **49 consultes**: **24 Wayback fallides**, **12 Common Crawl fallides**, **12 Arquivo.pt amb resposta 0 resultats**, **1 Arquivo.pt fallida**. | No resolt |
| 5 | Descàrrega i extracció de documents | **0 captures retornades, 0 PDF originals recuperats**, no s'ha pogut aplicar la fase d'extracció documental. | No resolt |
| 6 | Reconciliació i auditoria territorial | **0 identificadors nous**, **0/48** combinacions territori-mes certificades; els 28 originals no desapareixen ni queden invalidats per falta de captures. | No assolit |

## Controls de qualitat

- No es pot considerar **0 ofertes** cap mes o SSTT: la consulta d'arxius ha fallat o ha retornat cap captura d'URL concret, cosa que no prova inexistència de l'oferta.
- Cap data de captura ni de termini es transforma automàticament en **data de publicació**.
- Cap adjudicació o nomenament ordinari es compta com a publicació DC.
- Els resultats i les captures registren únicament **metadades públiques**, sense noms de docents.
- El workflow **ha executat i publicat** les dades; el resultat de la recerca és incomplet, no un error d'execució.
- El recompte `28` és el corpus heretat auditat, **no** un cens certificat del període.
- No hi ha cap necessitat de pagar TinyFish, Firecrawl o els minuts de GitHub de repositoris privats per aquesta prova.

## Veredicte

**FAIL / OBJECTIU EXHAUSTIU NO ASSOLIT.** L'execució autònoma ha esgotat les consultes implementades i ha deixat dades d'errors reproduïbles. No existeix evidència suficient per certificar el total de convocatòries publicades nov–feb ni les republicacions i les desertes.

## Proves reproduïbles

- Execució real de [GitHub Actions #1](https://github.com/hectorPascualC/ustec-dc-historic-2025-2026/actions/runs/38289053756)
- [Informe JSON](https://github.com/hectorPascualC/ustec-dc-historic-2025-2026/blob/main/exports_official/AUDITORIA_ARCHIUS_DC.json)
- [Consulta per consulta amb error i resposta](https://github.com/hectorPascualC/ustec-dc-historic-2025-2026/blob/main/exports_official/ARXIU_CONSULTES.csv)
- [Metodologia](https://github.com/hectorPascualC/ustec-dc-historic-2025-2026/blob/main/README_ARXIUS_DC.md)

## Limitacions pendents fora de les vies executades

Altres vies en línia encara possibles, però **no demostrades**: cerca de resultats de convocatòries EDUBCN 2025–2026 dins la base dinàmica, còpies de cercadors privats o col·leccions alternatives i accés indirecte a arxius web quan els endpoints CDX deixin de respondre amb errors. El fracàs d'aquesta passada no autoritza a afirmar que s'han esgotat totes les possibilitats online ni que els PDF antics no existeixen.
