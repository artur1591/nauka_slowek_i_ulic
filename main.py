#!/usr/bin/python3.9
import sys
import klasa_okno

#bo można podać argument procent_slowek_reszta_ulic zakres 0-100
if len(sys.argv)>1:
	App=klasa_okno.Okno(int(sys.argv[1]))
else:
	App=klasa_okno.Okno()
