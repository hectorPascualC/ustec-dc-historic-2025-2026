# Auditoria V201 — revisió estàtica del filtre temporal V92 (10/11/2026)

Abast: 507, 627, F57, F87 i combinacions acreditades; 01/11/2025–28/02/2026, 11 SSTT + EDUBCN. No és AUTO-PUBLIC.

## Troballa verificable de codi

A `src/forensic_qpdf_pdfresurrect_v92.py` (versió consultada el 10/11/2026), `DATE_RE = re.compile(r"(?<!\\d)2025(?!\\d)")` i `possible_2025_with_code` només compten revisions amb el literal `2025`. Per tant, una revisió extreta que només contingui dates de gener/febrer de **2026** i codis 507/627/F57/F87 pot quedar fora del comptador de candidats, encara que sigui rellevant. Això és un **fals negatiu potencial del filtre**, no evidència que existeixi una revisió antiga. El codi també limita l'extracció de text a les primeres 40 pàgines, fet que exigeix comprovar l'abast abans d'interpretar zeros.

La dependència `exports_territorial/SSTT_V91_CHANGED_INPUT.csv` continua sense localitzar-se per la ruta exacta esperada a la branca per defecte (404 ja documentat V200); una cerca de codi per `SSTT_V91_CHANGED_INPUT` no ha retornat coincidències. No s'ha executat el processament qpdf/PDFResurrect: **0/13**; no hi ha SHA-256 de noves descàrregues, PDF històric recuperat ni WARC Range verificat.

## Recomanació de correcció

Separar l'indicador temporal en `contains_2025`, `contains_2026` i `within_target_period` (data real contextualitzada 01/11/2025–28/02/2026), i conservar el text i l'evidència de cada revisió sense pujar dades personals. Validar les 13 URL i els SHA de V91 abans de córrer V92; executar qpdf i PDFResurrect en un runner amb dependències. No assimilar una revisió incremental PDF a una publicació al servidor.

Cens sense canvis acreditats: 36 IDs provisionals (21×507, 14×627, 1×F57-507) + 1 candidat; quatre registres EDUBCN amb data de portal; 12/12 territoris, 48 controls: 0 PASS / 14 PARTIAL / 34 BLOCKED, 0 exhaustius. Veredicte PARTIAL.
