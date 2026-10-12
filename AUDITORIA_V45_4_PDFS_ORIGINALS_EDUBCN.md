# AUDITORIA V45 — recuperació històrica real de convocatòries EDUBCN a PADICAT

**Consulta:** 12/10/2026. **Període d'interès:** 01/11/2025–28/02/2026.  
**Àmbits:** 11 SSTT i Consorci d'Educació de Barcelona. **Codis:** 507, 627, F57, F87 (i combinacions justificades).  
**Veredicte:** **PASS recuperació de 4 ofertes originals 507/627; FAIL cens exhaustiu de Catalunya.**

## 1. Recuperació de la fotografia administrativa — 29/01/2026

La investigació de les **versions històriques de PDF** havia identificat a PADICAT:
- [Pàgina EDUBCN capturada el 29/01/2026, 22:46:29Z](https://wayback.padicat.cat/20260129224629id_/https://www.edubcn.cat/ca/professorat_i_pas/seleccio_rrhh/dificil_cobertura) — HTML íntegre disponible amb HTTP 200 (117.758 bytes en la prova de reproducció).
- [API original de convocatòries capturada el 29/01/2026, 22:46:30Z](https://wayback.padicat.cat/20260129224630id_/https://www.edubcn.cat/pdc_rest/convocatories/ca) — JSON original íntegre amb HTTP 200, 27.123 bytes; **49 registres**.
- Còpia de l'API en castellà capturada el 29/01/2026, 23:01:01Z, amb **49 registres** i exactament els mateixos quatre codis d'interès.
- Captura de la mateixa API en català del 04/10/2026, amb **145 registres**, però **cap registre 507/627/F57/F87 datat dins la nostra finestra** en aquella versió. No desmenteix les quatre ofertes de gener, que ja havien desaparegut del llistat.

Les consultes a PADICAT es van fer amb el CDX públic `https://wayback.padicat.cat/cdx`. Es va confirmar que el format CDXJ guarda la data **fora** de l'objecte JSON; sol·licitant `output=json` vam recuperar les marques temporals correctes. La reproducció `/wayback/<timestamp>id_/...` retornava 404, mentre que la ruta alternativa documentada `/<timestamp>id_/...` ha retornat l'HTML i la resposta JSON. Les captures són evidència que els registres existien com a molt tard el dia de la captura, **no un segell de publicació a l'hora exacta**.

## 2. Quatre convocatòries 507/627 de l'API històrica amb PDF original validat

| DATA a l'API original | Codi de convocatòria | Centre | Especialitat | Jornada comprovada | Termini |
|---|---|---|---|---|---|
| 05/12/2025 | `GENSEC_147` | Institut Escola del Treball | **627** | **Sencera** | 09/12/2025, 13 h |
| 21/01/2026 | `GENSEC2526_167` | Institut Pedralbes | **507** | **Sencera** | 23/01/2026, 11 h |
| 22/01/2026 | `GENSEC_2526_145` | Institut Tecnològic de Barcelona | **507**, ciberseguretat | **Sencera** | Fins que es cobreixi la substitució |
| 22/01/2026 | `GENSEC_2526_149` | Institut Tecnològic de Barcelona | **627** | No determinada amb prou precisió | Fins que es cobreixi la substitució |

**Fonts originals de cada PDF:**
- [Oferta GENSEC_147 Escola del Treball — 627](https://www.edubcn.cat/rcs_gene/seleccio/GESEC2526_147_INS_ESCOLA_DEL_TREBALL_627.pdf), PDF 3 pàgines, SHA256 `8a9c68a960446d7cbe84332b293a29452e6b915124a79ee17425f52e5495abb3`.
- [Oferta GENSEC2526_167 Pedralbes — 507](https://www.edubcn.cat/rcs_gene/seleccio/GESEC2526_167_INS_PEDRALBES_507_INFORMATICA.pdf), PDF 3 pàgines, SHA256 `75e4daa41bb335b5c69bab2bf1a8f7721d090a03552678f03f112b53d17e82af`.
- [Oferta GENSEC_2526_145 ITB — 507 ciberseguretat](https://www.edubcn.cat/rcs_gene/seleccio/GENSEC_2526_145_Inst_Tecnologic_507.pdf), PDF 2 pàgines, SHA256 `36b740c5ae79725d3cfa2fb30a037214047d855cdb63bb01bc9a0c50fa069573`.
- [Oferta GENSEC_2526_149 ITB — 627](https://www.edubcn.cat/rcs_gene/seleccio/GENSEC_2526_149_Inst_Tecnologic_627.pdf), PDF 3 pàgines, SHA256 `476f51b8091ccc4390699813badb467e267dc805d26f685b657a99b2ec59a325`.

Cada PDF original ha estat descarregat des de l'URL oficial amb HTTP 200; tots quatre comencen amb `%PDF-` i el text conté **el codi real de convocatòria**, l'especialitat i el curs **2025–2026**. Per tant el nivell probatori és molt superior a un fragment de cercador. L'hora de publicació de l'oferta no s'ha certificat, però el camp DATA de l'API preservada situa les quatre dins la finestra i l'arxiu de gener en confirma l'existència abans de febrer.

**Dos PDF de resultat també validats**:
- [Resultat GENSEC_2526_145 — 507](https://www.edubcn.cat/rcs_gene/seleccio/GENSEC_2526_145_Inst_Tecnologic_507_RESULTAT.pdf), PDF 1 pàgina.
- [Resultat GENSEC_147 — 627](https://www.edubcn.cat/rcs_gene/seleccio/GESEC2526_147_INS_ESCOLA_DEL_TREBALL_627_RESULTAT.pdf), PDF 1 pàgina.

**No s'infereix l'estat exacte d'adjudicació ni si va ser fora de borsa:** l'existència del document de resultat no és suficient per fer aquesta afirmació. No s'ha desat cap nom, DNI, contacte o resultat individualitzat als exports.

## 3. Reconciliació amb el corpus anterior

Els quatre codis eren **absents del cens anterior V23 de 32 identificadors**. Ara figuren al [cens V45 de 36 identificadors](cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V45_36IDS_AUDITATS.csv).

| Especialitat | Identificadors coneguts |
|---|---:|
| 507 | **21** (abans 19) |
| 627 | **14** (abans 12) |
| F57-507 | **1** |
| **Total** | **36** |

Territoris: Barcelonès **17**, Baix Llobregat **9**, Vallès Occidental **2**, Lleida **3**, Penedès **1** i **Consorci d'Educació de Barcelona 4**. Les altres sis demarcacions no tenen cap cas identificat **amb prova del període**, cosa que no significa que no hi hagués convocatòries.

Nivells provisionals del conjunt: **27 amb algun rastre d'oferta (d'aquests, 4 amb PDF íntegre validat)**; **9 coneguts només a partir de resultats indexats**. Cap dels 48 blocs territori-mes es considera exhaustiu.

## 4. Vies descartades / límits

**PADICAT V36:** 25 consultes de variants exactes `http/https` i 11 prefixos territorials, HTTP 200 en totes, tres captures HTML d'EDUBCN però cap PDF original dels SSTT en les URL i prefixos provats. **V40**, ampliant a `/pdc_rest/`, va descobrir la resposta històrica de l'API que ha fet possible la V41.

**Common Crawl V37:** 12 consultes CDX seqüencials a quatre col·leccions reals (novembre, desembre, gener i febrer). Respostes 404 i 502, **cap registre amb offset/filename/length** i, per tant, **cap WARC descarregat**. L'error 502 no indica inexistència d'oferta; no es justificava repetir-lo agressivament.

**Comparació V43:** català i castellà del 29/01 confirmen els mateixos quatre codis; l'arxiu del 04/10 té dades de períodes diferents. **No certifica que no hi hagués altres convocatòries al febrer** que ja s'haguessin retirat abans d'octubre.

**V44:** quatre PDFs d'oferta i dos de resultat verificats; tres jornades senceres detectades al text al costat de `JORNADA`, una sense prou precisió; cap consulta de dades personals.

## 5. Fitxers reproduïbles i execucions

- [Cens V45 (36 ID, preserva V23 i afegeix 4 EDUBCN)](cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V45_36IDS_AUDITATS.csv).
- [Matriu territorial V45 (12 àmbits)](cens/MATRIU_V45_TOTS_SSTT_36IDS.csv).
- [API històrica EDUBCN: 49 registres, quatre filtrats, amb hashes](exports_padicat/EDUBCN_20260129_V41_TARGET_OFFERS.json).
- [Contrast entre dues captures i dues llengües (V43)](exports_padicat/EDUBCN_V43_ARCHIVE_COMPARISON.json).
- [Audit de PDF original i de resultat (V44)](exports_padicat/EDUBCN_V44_OFFERS_RESULTS_PDF.json).
- [PADICAT CDX 25 consultes de variants (V36)](exports_padicat/PADICAT_V36_VARIANTS_PREFIX.json).
- [Respostes Common Crawl V37](exports_commoncrawl/COMMONCRAWL_V37_WARC.json).
- [Workflow d'extracció V41](.github/workflows/recover-edubcn-snapshot-v41.yml); [script Python](src/recover_edubcn_20260129_dc_v41.py).
- [Auditoria V35 del protocol recuperat de la Biblioteca](AUDITORIA_V35_REPRESA_PROTOCOL_PDF_BIBLIOTECA.md).

**Veredicte de V45: PASS per recuperar una captura JSON històrica original de gener de 2026 i quatre convocatòries oficials 507/627 amb PDF complet i SHA256; FAIL per reconstruir totes les convocatòries de novembre 2025 – febrer 2026 a tots els territoris.**
