# Auditoria V28–V29 — ampliació terminològica i verificació de l'e-TAULER històric

**Data:** 12/10/2026. **Període objecte:** 01/11/2025–28/02/2026. **Especialitats:** 507, 627, F57, F87 i combinacions documentades. **Àmbit:** Generalitat (11 SSTT + EDUBCN).

## Mètode contrastat

S'ha executat el navegador públic de la Generalitat [e-TAULER](https://tauler.seu-e.cat/inici?idEns=1) amb la casella històrica `state=2` seleccionada i **aplicada amb el botó “Mostrar resultats”**. El registre de xarxa confirma que les consultes de la V27 usaven `POST /api/edictes` amb `state="2"`, diferenciant-les de l'estat `1` dels anuncis actius. La nova V28 ha provat 15 expressions docents alternatives. Només es conserven recomptes, dates mostrades i indicadors de codi, no els noms ni la redacció completa dels anuncis.

## Resultats V28

| Expressió | Resposta de la pàgina | Observació |
|---|---:|---|
| `personal docent` | **20 anuncis** | Entre els primers vuit hi ha registres datats **09/12/2025, 10/02/2026 i 16/02/2026**, però **sense 507/627/F57/F87 ni expressió DC** a la targeta visible |
| `nomenaments` | **16 anuncis** | Les primeres fitxes són d'octubre de 2025 o anteriors; no acrediten una oferta DC nov–feb |
| `informàtica` | **14 anuncis** | Les primeres fitxes són de juny/juliol 2026 o anteriors a 2022; no acrediten ofertes del període |
| `difícil` | **1 anunci** | Edicte Generalitat `574245`, dates visibles **27/06/2025 i 31/08/2025**, no pertinents al període |
| `borsa docent`, `borsa de treball docent`, `substitucions`, `vacants`, `formació professional`, `sistemes informàtics`, `dificil` | Sense anuncis visibles a les captures de prova | No se n'infereix un zero administratiu històric |
| `professorat`, `professorat interí`, `cobertura`, `interinitat` | Alguns resultats poden ser **residus de consultes anteriors** | Les captures mostren targetes de 2026 actuals o del terme anterior mentre el comptador no s'actualitza; **no es presenten com a recomptes confirmats** |

La cerca V28 pren **metadades dels primers vuit anuncis per expressió**, encara que la llista pugui ser més llarga. Això no substitueix la lectura dels detalls i eventuals annexos.

**IMPORTANT:** tres registres de `personal docent` mostren dates dins la finestra, però **cap no és una oferta 507/627/F57/F87 demostrada**. Resten només com a pistes a revisar: les coincidències d'un terme genèric no es converteixen en places.

## V29: petició REST independent sense el navegador

S'ha provat `POST https://tauler.seu-e.cat/api/edictes` i amb `?idEns=1` per vuit variants amb `state=2`. Totes les peticions directes han retornat **HTTP 400**; en canvi les peticions generades pel navegador han retornat resultats amb el mateix estat.

Aquest 400 **no** és un resultat de cerca buit. Pot faltar algun camp, encapçalament o context de sessió que incorpora el frontend. La comprovació REST és **inconclusa** i no s'utilitza per afirmar cap absència.

## Fonts reproduïbles

- [Cerca històrica V27 amb el resultat individual](exports_etauler/ETAULER_UI_AUDIT.json).
- [Exploració V28 dels 15 termes](exports_etauler/ETAULER_V28_TERMINOLOGIA.json).
- [V29 respostes REST HTTP i esquema](exports_etauler/ETAULER_API_V29_SCHEMA.json).
- [Scripts V28](src/probe_etauler_synonyms_v28.py) i [V29](src/probe_etauler_api_v29.py).
- [Cens principal: 32 identificadors](cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V23_32IDS.csv).

## Auditoria de l'objectiu

**PASS:** una font pública històrica nova explorada amb filtratge real verificat, 15 denominacions addicionals contrastades, i els casos fora de període exclosos amb criteri.

**FAIL:** no s'ha recuperat cap oferta original addicional de les especialitats i del període; es mantenen **32 IDs provisionals** i **0/48** combinacions territori-mes certificades com a exhaustives. Les fonts territorials originals de 2025–2026 segueixen incompletes i aquesta font e-TAULER no garanteix conservar tots els anuncis retirats.
