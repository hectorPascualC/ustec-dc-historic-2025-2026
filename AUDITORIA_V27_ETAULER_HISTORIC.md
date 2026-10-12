# Auditoria V27 — històric públic e-TAULER de la Generalitat (12/10/2026)

## Objectiu i límits

Trobar noves **convocatòries originals** de difícil cobertura (DC) de les especialitats **507, 627, F57 i F87** o equivalents comprovats publicades **01/11/2025–28/02/2026**. Els nomenaments ordinaris, concursos diferents, resultats sense oferta i documents fora del període **no** se sumen.

## Nova font oficial independent de PDF territorials

- Enllaç institucional: https://web.gencat.cat/ca/seu-electronica -> **Tauler electrònic**.
- Tauler oficial de la Generalitat: https://tauler.seu-e.cat/inici?idEns=1.
- Documentació del Consorci AOC: https://www.aoc.cat/blog/2025/nou-etauler-5febrer/ confirma històric disponible des del febrer de 2025 i trasllat del domini antic `tauler.seu.cat` al nou `tauler.seu-e.cat`.
- L'històric **no preserva necessàriament tots els anuncis**: poden no aparèixer els retirats abans del venciment o els que l'ens va marcar com a contenir dades personals. El resultat d'una consulta no constitueix un cens complet de les ofertes DC.
- El frontend públic és una app de React que consulta `POST /api/edictes`. El primer contacte mostra anuncis actius destacats, i la casella `Històric` **no aplica** el filtre fins a prémer **Mostrar resultats**.
- S'ha comprovat el codi JavaScript públic del tauler i s'ha executat GitHub Actions amb Playwright. L'API envia `state="1"` per anuncis actius i **`state="2"` per històrics**. S'ha verificat explícitament el segon valor en les peticions. Això evita l'error de confondre 0 d'una consulta activa amb el resultat històric.

## Cerques validades amb filtre històric real (`state=2`)

| Terme | Anuncis retornats |
|---|---:|
| `difícil cobertura` | **1** |
| `dificil cobertura` | 0 |
| `nomenaments interí` | 0 |
| `GENSEC_2526` | 0 |
| `2025/SEC` | 0 |
| `507` | 0 |
| `627` | 0 |
| `F57` | 0 |
| `F87` | 0 |

Aquestes xifres són **només resultats d'una cerca textual del tauler**, no el nombre real d'ofertes de les especialitats. Les variants ortogràfiques i les denominacions administratives poden quedar fora d'aquests termes.

### Examen de l'únic anunci

- **ID e-TAULER:** `574245`.
- **URL original:** https://tauler.seu-e.cat/detall?idEns=1&idEdicte=574245.
- **Indicadors visibles del resultat:** conté termes d'educació i «difícil cobertura»; **no** conté els codis `507`, `627`, `F57` ni `F87`.
- **Dates visibles a la fitxa de cerca:** `27/06/2025` i `31/08/2025`. No hi ha cap evidència de publicació o republicació **01/11/2025–28/02/2026** en la informació recuperada.
- **Decisió:** *no incorporar al cens*. És un anunci de referència temporal anterior al període, i sense prova d'oferta de les especialitats exigides. No s'han emmagatzemat dades personals.
- La pàgina individual del detall no s'ha pogut llegir amb el connector textual (resposta `empty_content`). La identificació procedeix de la consulta real de la fitxa al navegador Playwright i l'ID obtingut en obrir-la.

## Reproducció

- [Codi del recuperador](src/probe_etauler_historic.py)
- [Workflow públic](.github/workflows/probe-etauler-historic.yml)
- [Execució e-TAULER amb filtre històric i resolució de l'ID](https://github.com/hectorPascualC/ustec-dc-historic-2025-2026/actions/runs/38301018231)
- [Auditoria JSON — només filtres, comptatges, dates i ID públic](exports_etauler/ETAULER_UI_AUDIT.json)
- [Cens actual de 32 places](cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V23_32IDS.csv)

## Veredicte

**PASS:** font històrica oficial addicional consultada i filtratge real `state=2` comprovat; únic resultat examinat i exclòs de manera raonada.

**FAIL respecte l'objectiu d'exhaustivitat:** **0 identificadors nous**, **32 identificadors provisionals** intactes, **0/48 combinacions territori-mes certificades**. Les ofertes només exposades temporalment en els portals territorials poden no haver estat publicades a l'e-TAULER. La manca de coincidències aquí **no és prova d'inexistència de DC**.
