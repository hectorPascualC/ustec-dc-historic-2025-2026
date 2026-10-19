# Auditoria V118 — validació del recompte de versions PDFResurrect

Data: 19/10/2026. Abast: forense de 13 PDF oficials canviats de SHA, sense dades personals.

## Error reproduït (offline)
El validador del workflow local V115 pot acceptar com a PASS 13 documents si `qpdf --check`, `pdfresurrect -q` i `pdfresurrect -w` retornen codi 0, encara que `-q` informi de dues versions i `-w` no hagi deixat cap versió extraïda. Un informe sintètic de 13 entrades ho reprodueix: validador V115 = PASS incorrecte, comprovació V118 = FAIL correcte.

## Reparació proposada (pendent de publicar i executar)
Registrar de forma anonimitzada el nombre de versions indicat per `pdfresurrect -q`, verificar que és enter >= 1, que coincideix amb `extracted_count` i `len(extracted_versions)`, i que cada PDF extret es pot obrir. No conservar sortides textuals de comandes. Sintaxi `pdfresurrect file.pdf [-w][-q]` documentada al manual Debian.

## Limitacions
No s'ha executat qpdf ni PDFResurrect real sobre els 13 PDF; no s'ha recuperat cap oferta històrica. Cens provisional sense canvis: 36 ID (21×507, 14×627, 1×F57-507), 4 dates EDUBCN acreditades; 12/12 territoris; 0 PASS, 14 PARTIAL, 34 BLOCKED de 48 controls.

Font manual: https://manpages.debian.org/trixie/pdfresurrect/pdfresurrect.1.en.html
