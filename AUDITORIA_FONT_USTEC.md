# Auditoria de cobertura de la font USTEC — 12/10/2026

## Font i mètode
- Web: https://www.sindicat.net/eines/nomenaments/nomenaments2.php
- Endpoint GET identificat en execució real de GitHub Actions: `https://www.sindicat.net/eines/nomenaments/server_processing2.php`.
- La taula és DataTables amb filtratge al servidor. Columnes d'interès: especialitat (5), procediment (8), curs (9), número adjudicat (2).
- Proves API realitzades el 12/10/2026 amb filtres de procediment, curs i especialitat; no són estadístiques sobre totes les ofertes docents DC.

## Cobertura de l'API per procediment (curs 2025–2026)
| Codi procediment | Etiqueta del desplegable | Registres retornats |
|---|---|---:|
| `nt` | Nomenaments telemàtics | 60.520 |
| `ae` | Adjudicacions estiu | 7.493 |
| `dif` | Difícil cobertura | 0 |
| `urg` | Procediment urgència | 0 |
| `dir` | Selecció direcció | 0 |

El filtre `dif` també retorna 0 sense filtre de curs, en l'històric consultable d'USTEC. Això suggereix que el desplegable existeix però les dades DC no s'han incorporat a aquesta base; no demostra l'absència de convocatòries DC reals.

## Primera execució real (GitHub Actions #1)
- Nomenaments de 507/627 amb curs 2025–26: 1.757 + 1.174 registres de la consulta, 2.820 files diferents vàlides després de deduplicar.
- Entre 01/11/2025 i 28/02/2026: 987 registres diferents, tots classificats `Nomenaments telemàtics`.
- `F57` i `F87`: 0 files recuperades amb aquests codis; no són zeros certificats de places reals.
- No tenim un cens de publicacions, ofertes retirades, republicacions o DC desertes.
- L'extracció ha retornat codi de sortida 2 perquè l'auditoria marcava fonts no verificades, encara que ha publicat els CSV i l'auditoria.

## Control «Veure les NO adjudicades»
L'inspector de la pàgina confirma un **botó** `#btn-filter`, no una casella. En prémer-lo, DataTables aplica `column(2).search("0")`; el recompte filtrat de l'exemple passa de 27.336 a 3.065 (curs predeterminat 2026–2027). El control limita la vista a no adjudicades; no constitueix un registre d'ofertes DC. El recuperador V18 detecta el botó i evita el fals avís de «casella inexistent».

## Conclusió
**Aquesta font NO és el cens de difícil cobertura cercat.** No es poden sumar les files ordinàries com si fossin ofertes DC ni interpretar `dif=0` com «no es van oferir places». La investigació del cens original ha de continuar en fonts de convocatòries SSTT/EDUBCN, altres sindicats o rastres històrics, amb prova explícita de publicació i data.
