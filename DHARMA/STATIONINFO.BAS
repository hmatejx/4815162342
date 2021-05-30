10 HOME
20 REM ====================
21 REM Display the swan map
22 REM ====================
30 IMG "DHARMA/SWANLAYOUT.PNG", 4, 0, 2.4, 9
50 HTAB 6.2: VTAB 3: PRINT "B";
60 HTAB 11: VTAB 2.5: PRINT "S";
70 HTAB 17.7: VTAB 6.33: PRINT "D";
80 HTAB 6.1: VTAB 6.33: PRINT "R";
90 HTAB 11: VTAB 6: PRINT "H";
100 HTAB 7: VTAB 8.67: PRINT "A";
110 HTAB 13: VTAB 10.5: PRINT "C";
120 HTAB 2: VTAB 10.67: PRINT "E";
130 HTAB 20.5: VTAB 13: PRINT "E";
140 HTAB 12.15: VTAB 14.4: PRINT "#"
200 REM ======================
201 REM Legend key description
202 REM ======================
209 INV = 57600
210 HTAB 25: VTAB 1: PRINT CHR$(INV + ASC("B")), " bedroom area";
220 HTAB 25: VTAB 2: PRINT CHR$(INV + ASC("S")), " storage pantry";
230 HTAB 25: VTAB 3: PRINT CHR$(INV + ASC("D")), " computer dome";
240 HTAB 25: VTAB 4: PRINT CHR$(INV + ASC("R")), " restroom";
250 HTAB 25: VTAB 5: PRINT CHR$(INV + ASC("H")), " habitat/dining";
260 HTAB 25: VTAB 6: PRINT CHR$(INV + ASC("A")), " armory";
270 HTAB 25: VTAB 7: PRINT CHR$(INV + ASC("C")), " entry corridor";
280 HTAB 25: VTAB 8: PRINT CHR$(INV + ASC("E")), " exit/escape";
290 HTAB 25: VTAB 9: PRINT CHR$(INV + ASC("#")), " e.m. anomaly";
300 REM ======================
301 REM Show basic information
302 REM ======================
310 HTAB 2: VTAB 17: PRINT "The Dharma Initiative was established";
320 HTAB 2: VTAB 18: PRINT "in the year of 1970.";
330 HTAB 2: VTAB 19: PRINT "The Swan station's task is observation";
340 HTAB 2: VTAB 20: PRINT "of electromagnetic anomalies";
350 HTAB 2: VTAB 21: PRINT "More information is available in the";
360 HTAB 2: VTAB 22: PRINT "station's orientation film.";
400 REM ===========
401 REM Exit prompt
402 REM ===========
410 BAR$ = ""
420 FOR I = 1 TO 12
430 BAR$ = BAR$ + CHR$(9552)
440 NEXT I
450 HTAB 26: VTAB 12: PRINT CHR$(9556), BAR$, CHR$(9559)
460 HTAB 26: VTAB 13: PRINT CHR$(9553), "EXIT (Y/N)? ", CHR$(9553)
470 HTAB 26: VTAB 14: PRINT CHR$(9562), BAR$, CHR$(9565)
480 HTAB 38: VTAB 13: GET K
490 IF K <> "Y" THEN GOTO 450
500 HOME