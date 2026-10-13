# AUDITORIA V51 — PADICAT EDUBCN: 36 casos, 4 originals històrics autenticats

**Data:** 13/10/2026. **Àmbit de l'estudi:** ofertes DC 507/627/F57/F87 a Catalunya publicades entre 01/11/2025 i 28/02/2026. **Cobertura territorial completa:** encara no certificada.

## 1. Resultat principal: reconstrucció d'una API administrativa de gener 2026

PADICAT conserva:
- HTML del Consorci d'Educació de Barcelona capturat **29/01/2026, 22:46:29**;
- JSON de la seva API `pdc_rest/convocatories/ca` capturat **29/01/2026, 22:46:30 UTC**, amb **49 convocatòries**;
- PDF originals (binari) de les convocatòries pertinents capturats la mateixa nit.

API original: https://wayback.padicat.cat/20260129224630id_/https://www.edubcn.cat/pdc_rest/convocatories/ca

**Quatre noves convocatòries** respecte del cens V23 de 32 casos:

| Codi de registre oficial | DATA de l'API | Especialitat | Centre | Jornada al PDF original | Termini registrat |
|---|---|---|---|---|---|
| `GENSEC_147` | 05/12/2025 | 627 | Institut Escola del Treball | Sencera | 09/12/2025 13 h |
| `GENSEC2526_167` | 21/01/2026 | 507 | Institut Pedralbes | Sencera | 23/01/2026 11 h |
| `GENSEC_2526_145` | 22/01/2026 | 507 ciberseguretat | Institut Tecnològic de Barcelona | Sencera | Fins que es cobreixi la substitució |
| `GENSEC_2526_149` | 22/01/2026 | 627 | Institut Tecnològic de Barcelona | No verificada | Fins que es cobreixi la substitució |

**Conservem literalment els codis tal com apareixen en l'API històrica**, encara que hi hagi diferents variants `GENSEC`/`GESEC`. El codi `GENSEC_147` de l'Escola del Treball **consta en el cens general, però queda exclòs de la shortlist personal**.

La columna DATA és **la data indicada per l'API**. No equival a data/hora exacta de publicació documental. Els PDF de l'Institut Tecnològic tenen metadades internes de desembre de 2025; això **pot** reflectir una redacció o republicació anterior, però **no certifica una data de publicació anterior**. Per als quatre casos, els codis, perfils i PDF complets coincideixen i són anteriors a la captura del 29/01.

## 2. Auditoria de la immutabilitat dels PDF

Els **4 PDF d'oferta** estan arxivats a PADICAT i encara responen al domini original EDUBCN. Els SHA-256 dels binaris arxivats són **idèntics** als dels actuals per als quatre documents, i tots contenen codi de convocatòria i especialitat pertinents.

PDF resultats originals: també s'han verificat amb HTTP 200 **2** resultats, per als codis `GENSEC_2526_145` i `GENSEC_147`. Que existeixi un PDF de resultat **no implica adjudicació fora de borsa**; els noms de docents i adjudicataris no s'han incorporat als informes.

Documents originals:
- https://www.edubcn.cat/rcs_gene/seleccio/GENSEC_2526_145_Inst_Tecnologic_507.pdf
- https://www.edubcn.cat/rcs_gene/seleccio/GENSEC_2526_149_Inst_Tecnologic_627.pdf
- https://www.edubcn.cat/rcs_gene/seleccio/GESEC2526_167_INS_PEDRALBES_507_INFORMATICA.pdf
- https://www.edubcn.cat/rcs_gene/seleccio/GESEC2526_147_INS_ESCOLA_DEL_TREBALL_627.pdf

## 3. Ampliació de les cerques a tota la carpeta antiga d'EDUBCN

- Inventari mensual PADICAT (novembre 2025–febrer 2026): **252 registres** al gener per al prefix `/rcs_gene/seleccio/` amb el protocol HTTPS; el mateix conjunt apareix quan es consulta el prefix HTTP per normalització de l'índex. **No sumar-los com 504 documents diferents**.
- Dels PDF d'oferta, la comprovació V45 va recuperar **33 originals** relacionats amb GENSEC de la fotografia de gener. Només **4** corresponen als codis objectiu.
- La comprovació independent de PDFs no identificats al nom com GENSEC (V47 complementari) va llegir **87 fitxers** i **no hi trobà especialitats objectiu**.
- Un altre escaneig de contingut dels **49 documents candidats amb noms GENSEC/MUNSEC/PFI i similars** ha recuperat **49 PDF**, trobant únicament els **mateixos quatre codis**, sense cap identificador nou.
- A la carpeta de PDFs arxivada no apareixen captures al novembre ni al desembre 2025, ni al febrer 2026 en les rutes i condicions consultades. Això **no implica absència de publicacions durant aquests mesos**, només absència de captures en aquestes consultes.

Fonts de verificació:
- [49 registres de l'API i els 4 casos](exports_padicat/EDUBCN_20260129_V41_TARGET_OFFERS.json)
- [Auditoria PDF originals i dos resultats](exports_padicat/EDUBCN_V43_PDF_RESULTS.json)
- [Índex dels 12 intents per mesos, 252 captures sense duplicar](exports_padicat/EDUBCN_V44_MONTHLY_PDF_DIRECTORY.json)
- [33 PDF d'oferta originals recuperats](exports_padicat/EDUBCN_PADICAT_V45_ALL_PDFS.json)
- [87 PDF de noms no evidents, sense noves especialitats](exports_padicat/EDUBCN_PADICAT_V47_NONCODED_PDFS.json)
- [49 PDF candidats GENSEC/MUNSEC/PFI analitzats](exports_padicat/EDUBCN_V47_ARCHIVED_PDF_BODIES.json)

## 4. Cens territorial i control d'exhaustivitat

**Nou cens V46: 36 identificadors únics**, amb:
- **21** de 507,
- **14** de 627,
- **1** F57-507.

Distribució dels identificadors recuperats: Barcelonès territorial (17), Baix Llobregat (9), Lleida (3), Penedès (1), Vallès Occidental (2), Consorci d'Educació Barcelona (4).

**27** identificadors tenen alguna traça d'oferta (23 de V23 + 4 originals de l'API arxivada), i **9** consten només com a resultats indexats. Una traça d'oferta de cercador no té el mateix grau de prova que un PDF original amb hash.

[CSV V46 de 36 casos](cens/HISTORIC_DC_507_627_F57_F87_NOV2025_FEB2026_V46_36IDS_VERIFICATS.csv).

## 5. Pendents

- **0 de 48** blocs territori-mes certificats exhaustius: ni les fotografies de l'API ni els PDF arxivats cobreixen totes les dates i retirades.
- PADICAT no ha retornat, en els prefixos de fitxers provats, PDF territorials originals del 2025–26 d'altres SSTT; els valors buits **no són 0 convocatòries reals**.
- El febrer 2026 d'EDUBCN continua fora de la captura 29/01 i no pot quedar exclòs per aquests resultats. Cal investigar altres índexs, còpies o URL antigues originals.
- Cap dada personal d'aspirants/adjudicataris s'ha afegit al cens o a aquest informe.

**Veredicte:** **PASS** recuperació documental dels 4 nous casos + verificació criptogràfica de PDF originals; **FAIL** cens de totes les convocatòries de Catalunya nov2025–feb2026.
