# Auditoria V177 — control de cadena V92 i cerca P0 (22/10/2026)

Abast: convocatòries publicades entre 01/11/2025 i 28/02/2026; 507, 627, F57, F87; 11 SSTT + EDUBCN. Sense dades personals.

## Verificació de codi i arquitectura
GitHub HEAD conegut b548c4021d2537a33f00f45d1c0647043ea71b99; auditoria V173 blob 8a974e66e62326f8f023b043d9f3caa84ae7c380. Scripts llegits: src/forensic_13_changed_v91.py (genera 13 URLs i conserva old_sha256/sha256_v86), src/forensic_qpdf_pdfresurrect_v92.py (sense comparació amb hash antics; només 40 pàgines; validació incorrecta de PDF sense text; subprocess output_excerpt no filtrat). Workflow V91 llegit; no hi ha workflow V92 a l'inventari.

Intent real de crear .github/workflows/forensic-qpdf-pdfresurrect-v92.yml amb checkout, apt qpdf/pdfresurrect, generador V91, script V92 i artefacte només metadades: BLOCKED per comprovacions de seguretat. Cap commit ni run V92. La documentació de pdfresurrect confirma -w com a extracció de revisions a disc; aquestes revisions NO són versions de servidor.

## P0 i límits
Cerca web independent per termes 507/627/F87, mesos gener-febrer i PDFs oficials datats: no s'ha acreditat cap ID nou. L'índex encara mostra el PDF Barcelonès _16012026.pdf amb 19143261/507 i termini 18/01/2026 (ja conegut V95); la URL actual retorna 404. Altres resultats: PDF BCO 06/03/2026 fora de finestra; mirall de Tarragona publicat 31/10/2025 amb inici octubre, exclòs sense prova de publicació novembre-febrer. Cap d'aquests resultats prova primera publicació dins la finestra.

## Estat
36 IDs provisionals (21x507,14x627,1xF57-507), 1 candidat separat, 4 registres EDUBCN amb data de portal (05/12/2025,21/01/2026,22/01/2026 x2). 12/12 àmbits, 48 controls 0 PASS /14 PARTIAL/34 BLOCKED; 0 exhaustius. V91 run 39415173344 SUCCESS històric; V92 0/13. 0 PDF binaris nous, 0 SHA nous, 0 WARC Range, 0 primeres dates acreditades.

Següent via: publicar V92 quan estigui autoritzat, validar el runner amb 13 URLs i hashes antics, i recuperar bytes històrics per font pública alternativa a Firecrawl.
