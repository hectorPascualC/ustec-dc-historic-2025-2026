# Auditoria V31 — tancament de la via e-TAULER històric (12/10/2026)

## Objectiu

Recuperar les **ofertes originals de difícil cobertura** publicades entre **01/11/2025 i 28/02/2026** a Catalunya per a **507, 627, F57, F87** i combinacions, diferenciant les publicacions de resultats i nomenaments ordinaris.

## Nova font contrastada: històric oficial e-TAULER

- Tauler públic Generalitat: https://tauler.seu-e.cat/inici?idEns=1
- El navegador Playwright del runner públic de GitHub confirma filtratge real `state="2"` a `POST /api/edictes`, després de seleccionar «Històric» i prémer «Mostrar resultats».
- Cerca literal `difícil cobertura`: **1** anunci, edicte **574245** (dates visibles **27/06/2025–31/08/2025**), **fora del període** i sense codis 507/627/F57/F87 visibles. Exclòs.
- Segona passada amb **15 sinònims docents**: `personal docent` retorna **20** anuncis, `nomenaments` **16**, `informàtica` **14**, `difícil` **1**. Les consultes que mostraven targetes velles amb un comptatge no actualitzat s'han marcat **inconcluses**, no com a zeros.
- Un POST directe fora del navegador, fins i tot indicant `idEns=1`, retorna **HTTP 400**; no és una resposta vàlida sobre si existeixen anuncis.
- Els anuncis històrics poden no contenir les convocatòries DC dels portals territorials. No s'infereixen zeros de places.

## Tres edictes «personal docent» amb dates dins el període

Els tres s'han **obert individualment en l'històric real**, i s'han inspeccionat només indicadors de text, sense publicar cap nom ni contingut personal:

| Edicte | Dates visibles a la targeta | Detectat DC/507/627/F57/F87 al detall | Annex |
|---|---|---|---|
| [612543](https://tauler.seu-e.cat/detall?idEns=1&idEdicte=612543) | 16/02/2026–13/03/2026 | **No** | Enllaç no descarregable com a PDF per la ruta d'auditoria |
| [611454](https://tauler.seu-e.cat/detall?idEns=1&idEdicte=611454) | 10/02/2026–09/03/2026 | **No** | Enllaç no descarregable com a PDF per la ruta d'auditoria |
| [602230](https://tauler.seu-e.cat/detall?idEns=1&idEdicte=602230) | 09/12/2025–09/01/2026 | **No** | Enllaç no descarregable com a PDF per la ruta d'auditoria |

En aquests tres detalls no consta literalment «difícil cobertura», «vacants» ni els codis d'interès. Un únic enllaç amb aparença de document en cada fitxa s'ha resolt a **`/null`**, resposta HTTP 200 però **HTML/no PDF**. Això **no permet certificar el contingut dels annexos**: no s'han recuperat PDF originals ni s'ha provat que els anuncis no tinguin annexos. Els tres **no s'incorporen** al cens perquè no existeix evidència de l'especialitat i procediment DC, però no s'afirma una exclusió administrativa definitiva.

## Fitxers i auditories reproduïbles

- [V27: filtratge històric real i únic anunci literal](AUDITORIA_V27_ETAULER_HISTORIC.md)
- [V28/V29: quinze variants i incidències del REST](AUDITORIA_V28_V29_ETAULER_ALTERNATIUS.md)
- [V30: fitxes individuals, sense text personal](exports_etauler/ETAULER_V30_CANDIDATES.json)
- [V31: diagnòstic dels enllaços i absència de PDF recuperable](exports_etauler/ETAULER_V31_ATTACHED_PDFS.json)
- [Codi V31 per reproduir la prova](src/inspect_etauler_attachments_v31.py)
- [Execució V31](https://github.com/hectorPascualC/ustec-dc-historic-2025-2026/actions/runs/38302516139)
- [Cens provisional 32 ID](cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V23_32IDS.csv)

## Veredicte

**PASS metodològic:** s'ha investigat una font administrativa històrica independent i verificat el filtre de l'API, 15 variants terminològiques, un edicte fora de període i tres fitxes individuals del període sense coincidència amb les especialitats DC.

**FAIL d'exhaustivitat:** no hi ha cap **ID de plaça nou** recuperat; es mantenen **32 identificadors provisionals** (19×507, 12×627, 1×F57-507), **23** amb rastre d'oferta i **9** només amb resultat, i **0/48 combinacions territori-mes** certificades. Els annexos de les tres fitxes no s'han pogut llegir com a PDF; això és una limitació tècnica i **no una prova d'absència d'ofertes**. La investigació online del cens global continua oberta.
