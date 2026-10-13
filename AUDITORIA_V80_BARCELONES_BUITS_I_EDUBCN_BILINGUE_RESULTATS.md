# AUDITORIA V80 — Buit de febrer EDUBCN, setmanes perdudes al Barcelonès i datació dels resultats

**Data:** 13/10/2026. **Objectiu principal:** reconstruir ofertes DC publicades 01/11/2025–28/02/2026, especialitats 507, 627, F57, F87; 11 SSTT i CEB. Protocol de Biblioteca `REFERENCIA_RECUPERACIO_HISTORICA_PDF_DC_507_627_F57_F87.md` v1.0, amb separació de dates de primera publicació, aparició al portal, captura, inici, resultat i possible republicació.

## 1. V76 — dues captures reals de la mateixa API EDUBCN, gener i octubre

Fonts amb **hash i cos JSON complet verificats**:
- **29/01/2026 22:46:30 UTC:** https://wayback.padicat.cat/20260129224630id_/https://www.edubcn.cat/pdc_rest/convocatories/ca
- **04/10/2026 09:35:14 UTC:** https://wayback.padicat.cat/20261004093514id_/https://www.edubcn.cat/pdc_rest/convocatories/ca

La captura de gener conté **49 registres públics** i quatre de les especialitats objectiu amb **`DATA` entre 01/11/2025 i 28/02/2026**. La d'octubre conté **145 registres**, **0** amb `DATA` en aquell mateix interval; per tant, la segona fotografia no és una còpia exhaustiva de convocatòries de febrer de 2026. Els quatre ID de gener tampoc hi són, sense que això demostri si van ser adjudicats o retirats en una data concreta.

[Extracció V76](exports_padicat/EDUBCN_V76_JAN_OCT_2026_TARGET_DIFF.json). **Cap ID nou**.

## 2. V77 — sis setmanes sense PDF datat al corpus BCO

Els onze lots indexats a V61 cobreixen onze divendres entre 07/11/2025 i 27/02/2026, però no se'n disposa en dates **21/11/2025, 12/12/2025, 19/12/2025, 26/12/2025, 02/01/2026, 09/01/2026**.

S'han generat **tres noms alternatius plausibles** per a cadascun d'aquests sis divendres, utilitzant els patrons històrics oficials Barcelonès-SEC i BCO-SEC, i s'han comprovat els **18 URL** en domini original.

**Resultat:** **18/18 HTTP 404**, 0 PDF originals accessibles a aquestes rutes; 0 errors de transport; 0 identificadors nous.

[Verificació exacta dels 18 URL V77](exports_official/BCO_V77_GAPS_PDF_FILENAME_PROBES.json). **Important:** eren hipòtesis de noms de fitxer; no s'afirma que els sis documents existissin ni tampoc que no hi hagués cap publicació aquelles setmanes. Un 404 del servidor viu no demostra cap absència a finals 2025.

## 3. V78 — quatre captures bilingües independents d'EDUBCN

Dues llengües i dues dates, totes quatre captures PADICAT comprovades:
- 29/01/2026 **català i castellà**: **49 registres cadascuna**, mateix conjunt de **49 codis**.
- 04/10/2026 **català i castellà**: **145 registres cadascuna**, **143 codis diferents**, mateix conjunt d'identificadors en les dues llengües.
- **Diferències per idioma d'identificadors: 0**, tant al gener com a l'octubre.
- Quatre ofertes objectiu amb `DATA` entre novembre i febrer, exactament `GENSEC_147`, `GENSEC2526_167`, `GENSEC_2526_145`, `GENSEC_2526_149`, sense cap cinquè cas.

Distribució mensual del camp `DATA` en les captures (totes les especialitats):
- Gener, 49 files: agost 2025 **2**, setembre **5**, octubre **5**, novembre **5**, desembre **7** i gener 2026 **25**.
- Octubre, 145 files: octubre 2024 **1** (registre residual), juliol 2026 **31**, agost **19**, setembre **90**, octubre **4**.

**Conclusió:** la captura d'octubre mostra majoritàriament un nou cicle de publicacions però conserva un registre antic aïllat: per tant, **no** hem de descriure l'API com un esborrament absolut per curs. Tampoc podem projectar els zero registres de febrer a tot el mes: **no existeix una captura del febrer en aquestes quatre respostes**.

[Auditoria V78 amb histogramas i codis](exports_padicat/EDUBCN_V78_BILINGUAL_API_HISTORIC_DIFF.json). **0 novetats**.

## 4. V79 — datació de PDF originals de resultat amb corroboració de hash arxivat

[Extracció V79](exports_padicat/EDUBCN_V79_RESULT_PDF_DATES.json) i [arxiu previ V54](exports_padicat/EDUBCN_V54_GENSEC_RESULTS.json).

| Codi | Data de publicació a la fitxa del portal | PDF resultat creat segons metadades | Estat / prova | SHA256 actual = arxiu V54 |
|---|---|---|---|---|
| `GENSEC_2526_145` (507) | 22/01/2026 | **28/01/2026 12:57:51 +01:00** | «Alta titular» | **Sí** — `c0c01a84a8a212169d03bf26e527ccc8df820448ac0a5d6bd352ba28bf8de80b` |
| `GENSEC_147` (627) | 05/12/2025 | **22/01/2026 16:29:34 +01:00** | PDF adjudicació conegut | **Sí** — `83cd099a75e2698c38e7fbe79b58140f56041542d20d4652b6b5c77736ab4c67` |

Els dos PDF de resultat consten a la captura PADICAT del **29/01/2026** i el fitxer en viu té el mateix SHA256 que el cos PDF d'arxiu V54. Per tant, tenim identitat documental corroborada, no sols metadades del web actual. Les dates internes de creació del resultat són **posteriors** a les dates `DATA` de les convocatòries. **No** demostren dia efectiu de decisió, primera publicació o adjudicació fora de borsa. El resultat «Alta titular» **no** és una plaça deserta.

## 5. Estat metodològic final i prioritats

**36 codis provisionals** al cens consolidat [V73](cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V73_36IDS.csv): **21 507, 14 627, 1 F57-507**. **4 dates de publicació del portal provades**, **0 dates de primera publicació absoluta verificades**; **0/48** blocs territori×mes acreditats exhaustius. No s'han afegit codis nous en V76–V79.

Les **dates de creació dels PDF originals** de les dues ofertes ITB continuen essent 01/12/2025 i 10/12/2025 (V75) amb terminis interns de 03/12 i 12/12 respectivament, mentre el portal les mostra 22/01/2026. La V79 **no** ha convertit aquestes pistes en una prova del primer anunci de desembre: el PDF de resultat ITB fou creat 28/01/2026, no desembre.

Pròxima investigació amb més valor: (a) **còpies externes originals** d'anuncis ITB desembre i d'ofertes curtes publicades entre els onze lots BCO; (b) índexs històrics **d'altres SSTT sense codis**; (c) fonts de resultats originals i dates que permetin vincular una oferta a publicació prèvia. No repetir mecànicament consultes a rutes conegudes 404 ni considerar absències de la fotografia com zero real de places.

**PASS:** 4 respostes d'API arxivades, comparades i conciliades; 18 candidats de URL datat comprovats amb resposta inequívoca; dos PDF de resultat validades per SHA256 arxivat. **FAIL de l'objectiu d'exhaustivitat.** Sense publicació de noms, DNI, correus, telèfons ni dades de candidatures.
