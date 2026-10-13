# Recuperador USTEC — històric de difícil cobertura 2025–2026

Aquest repositori és **públic i sense dades personals**. Fa servir únicament el cercador històric públic d'USTEC, sense cookies, claus ni secrets. Els CSV publicats a `exports/` **anonimitzen `numero_adjudicat`**, per evitar publicar números individuals.

## Única execució / sense cost per minuts

A **Actions → Recuperar DC USTEC 2025-2026 → Run workflow**, branca `main`. El primer commit del workflow a `main` en dispara una execució automàtica. No hi ha cap programació recurrent. El runner `ubuntu-24.04` és estàndard i gratuït en repositoris públics; es limita el job a 30 minuts. Els resultats queden desats a `exports/` en el mateix repositori; **no es creen artefactes facturables d'Actions**.

## Dades que intenta recuperar

- Curs `2025-2026`; nomenaments del `01/11/2025` al `28/02/2026`.
- Especialitats 507, 627, F57 i F87.
- Totes les files, incloent-hi les `No adjudicat` si la taula permet activar-les.
- `USTEC_nomenaments_DC_explicits.csv`: només files que declaren explícitament `Difícil cobertura`.
- `AUDITORIA_EXTRACCIO.json`: pàgines descarregades, total segons la taula, advertiments, estat `complete` i URL AJAX observats.

**Important:** aquesta font recull nomenaments i intents de nomenament, no l'univers complet de publicacions d'ofertes DC; les ofertes no adjudicades, retirades o republicades poden faltar. Un `complete=true` es refereix només a l'extracció de les files retornades per USTEC.

## Diagnòstic

Si el workflow surt en vermell, revisa `exports/AUDITORIA_EXTRACCIO.json` i les pestanyes del run per veure l'error. No interpretis un CSV buit com a absència de places. Si el servidor fallés abans de generar l'auditoria, consulta els logs del run.

## Investigació documental de DC (novembre 2025 – febrer 2026)

- [Cens provisional de **36 identificadors** (V49)](cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V49_36IDS.csv): 21 de 507, 14 de 627, 1 F57-507. **No és exhaustiu**; 0/48 blocs territori-mes certificats.
- [Auditoria territorial i documental V51](AUDITORIA_V51_PADICAT_120PDFS_CENS36.md): 120 PDF històrics analitzats, quatre originals EDUBCN contrastats amb PADICAT.
- [**Auditoria V52**: resultats i correcció de jornada 627 de l'ITB](AUDITORIA_V52_EDUBCN_RESULTATS_JORNADES_2026-10-13.md).
- [**Correccions V52** dels quatre casos EDUBCN](cens/EDUBCN_4_CASOS_V52_CORRECCIONS.csv). **Aquestes correccions prevalen sobre les jornades i estats indeterminats de V49**; els 36 ID continuen sense duplicats.
