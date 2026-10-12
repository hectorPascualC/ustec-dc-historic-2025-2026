# AUDITORIA V26 — comprovació de registres anteriors al període i bases de dades alternatives

**Revisió:** 12/10/2026. **Objectiu del cens:** totes les ofertes originals DC de Catalunya de les especialitats 507, 627, F57, F87 i combinacions entre **01/11/2025 i 28/02/2026**, 11 SSTT i EDUBCN; incloses les places desertes, retirades o republicades.

## 1. Resultat: no s'afegeixen places sense prova temporal d'oferta

El cens [V23](cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V23_32IDS.csv) es manté en **32 identificadors diferents: 19 de 507, 12 de 627 i 1 F57-507**. **23** tenen traça d'oferta indexada i **9** són coneguts només per resultat. Aquestes evidències són parcials, no constitueixen un cens exhaustiu.

S'han revisat **11 referències addicionals de 507/627/F57/F87 que no s'han d'incorporar automàticament**, desades a [cens/V26_CANDIDATS_EXCLOSOS_I_NO_CERTIFICATS.csv](cens/V26_CANDIDATS_EXCLOSOS_I_NO_CERTIFICATS.csv), amb motiu concret i font.

### Maresme–Vallès Oriental
- `627-Lliçà` — Institut de Lliçà d'Amunt, inici en **setembre 2025**, jornada sencera.
- `507-Mataró` — Institut Thos i Codina, inici **08/09/2025**, jornada sencera.
Són resultats DC de l'inici de curs; **no consta publicació o republicació nov2025–feb2026**, i per tant no se sumen.
Font: [resultats MVO](https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/maresme-valles-oriental/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/MVO-SEC-dificil-cobertura-vacants-cobertes.pdf), segons còpia indexada del curs 2025–26; el binari actual és mutable i en consultar-lo retorna el curs següent.

### Penedès
- `19132771` — Institut Joaquim Mir, **627**, inici **07/10/2025**.
- `19143259` — Institut Eugeni d'Ors, **627**, inici **23/10/2025**.
- `19153173` — Institut Joaquim Mir, **627**, inici **08/10/2025**.
Els resultats històrics indexats tenen inici a octubre, no hi ha prova de noves ofertes o republicacions a partir de novembre.
Font: [resultats Penedès](https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/penedes/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/PEN-SEC-dificil-cobertura-vacants-cobertes.pdf), versió indexada antiga.

### Lleida i Vallès Occidental (PFI)
- `2025/SEC/PFI/020` — Institut Alfons Costafreda, **F57-507**, inici **01/09/2025**.
- `F87-01/07` — Institut de Badia del Vallès, **F87-627**, resultat d'un procés d'estiu amb inici **01/09/2025**.
Confirmen les correspondències d'especialitat **per aquests registres**, però no acredita cap oferta publicada del novembre al febrer.
Fonts: [resultats PFI Lleida](https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/lleida/personal-docent/nomenaments-telematics/dificil-cobertura/oferta-moduls-pfi-ptt/LLE-PFI-dificil-cobertura-vacants-cobertes.pdf) i [resultats PFI Vallès Occidental](https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/valles-occidental/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/VOC-SEC-Vacants-PFI.pdf).

### Tarragona
- `103-43005704` i `104-43005704` — Institut Francesc Vidal i Barraquer, **507**, apareixen en còpia de l'oferta publicada amb inici a **octubre 2025**. El resultat antic marca adjudicació telemàtica / reincorporació de titular, **sense prova posterior nov–feb**.
- Referències de fila `87-43008638` (Institut Antoni Ballester, **627**) i `88-43002594` (Institut Baix Camp, **627**) — els resultats indiquen *adjudicada telemàticament*, però **sense dates de publicació ni oferta original**. Les etiquetes de fila no s'han de tractar com ID universals de plaça.
Fonts: [document indexat d'ofertes 2025](https://www.docsity.com/es/docs/dificil-cobertura-en-diferentes-contextos/14696135/) i [resultats oficials Tarragona](https://educacio.gencat.cat/web/.content/home/departament/serveis-territorials/tarragona/personal-docent/nomenaments-telematics/dificil-cobertura/secundaria/TAR-SEC-dificil-cobertura-vacants-cobertes.pdf).

**Important:** "no incorporat" no equival a "provat que no es va republicar mai". Cal acreditar la nova data abans d'incorporar-los.

## 2. Nova via contrastada: catàleg de dades obertes de la Generalitat

S'ha examinat el [catàleg de dades obertes d'Educació](https://educacio.gencat.cat/ca/actualitat/novetats/detall/article/dades-obertes-departament-educacio).

Conjunts rellevants:
- [Plantilles del personal docent dels centres públics i serveis educatius, dataset `4fid-p2hv`](https://analisi.transparenciacatalunya.cat/d/4fid-p2hv), anual, 69,5K files: estructura de llocs i ocupació definitiva, **NO publicacions DC amb identificador i termini**.
- [Personal docent segons especialitat, vincle i forma d'ocupació, dataset `qpti-cnx7`](https://analisi.transparenciacatalunya.cat/d/qpti-cnx7), mensual: estadística de personal, **NO registre de les convocatòries DC**.
- [Personal docent de centres públics, dataset `2ip7-jdgh`](https://analisi.transparenciacatalunya.cat/d/2ip7-jdgh), característiques del personal, **NO dades de convocatòria**.

No s'ha localitzat entre els conjunts consultats una font d'ofertes DC de 2025–2026 per ID de vacant + centre + data original de publicació. **No es pot convertir una variació de plantilla en una oferta DC**. Aquest resultat és limitat als conjunts consultats, no una prova absoluta d'absència de dades administratives.

## 3. Procediments que poden confondre's amb DC

La [convocatòria de concurs de mèrits per a l'IOC](https://educacio.gencat.cat/ca/serveis-tramits/treballa-amb-nosaltres/concursos/concurs-merits-vacants-ioc/) inclou **una plaça 627**, amb inscripcions del 27/01 al 16/02/2026, però és **un procés en comissió de serveis per a personal funcionari de carrera**. No equival a oferta DC ordinària i no s'afegeix al cens. Hi ha un cas diferent, **`19331041` de 507 IOC**, ja documentat com a DC al cens, que no s'ha de confondre amb aquest concurs.

## 4. Fonts externes de cercador i restriccions

- Cerca per Google/Bing, cerca específica de diversos SSTT i comprovació dels resultats documentals en PDF. Els registres de setembre/octubre i els de 2026–27 han quedat exclosos.
- La connexió de Firecrawl ha retornat **HTTP 402 per saldo de crèdits insuficient**. No s'ha comprat saldo ni carregat cap despesa; s'ha continuat amb cerca pública i altres fonts gratuïtes.
- El codi públic de seguiment `blackcub3s/projectesDocker` de novembre 2025 continua sent una font contemporània **sense historial guardat de PDF**.
- Wayback CDX continua retornant 503 als reintents documentats de V25; no s'interpreta com a 0 captures.

## 5. Veredicte

**PASS:** 11 referències dubtoses registrades com a exclusions condicionals; fonts i dates corroborades; evitada l'entrada de nomenaments telemàtics o processos de concurs diferents.  
**FAIL:** cens exhaustiu de totes les ofertes nov2025–feb2026 de 12 àmbits; **0 de 48 blocs territori-mes certificats**. **32 ID provisionals** sense canvis.

No donar per esgotades les vies documentals dels serveis territorials; la cerca online addicional pot recuperar noves còpies, però cap absència de resultat permet certificar "no es van publicar".
