
# Co robi program?
	Program losuje słówka i/lub ulice w celu treningu głowy.
	Spośród najrzadziej wylosowanych losowane są kolejne.
	Klawisz **Spacja** pokazuje następny wpis lub tłumaczenie (podstawowy klawisz programu).

# Uruchomienie programu:
	`./main.py` (prawa uruchamiania trzeba nadać) lub `python main.py`
	opcjonalny argument: liczba od 0 do 100 oznacza *procent_slowek_reszta_ulic*

# Uruchomienie programu:
	./main.py (prawa uruchamiania trzeba nadać) lub python main.py
	opcjonalny argument: liczba od 0 do 100 oznacza procent_slowek_reszta_ulic
	czyli 100 oznacza tylko slowka a 0 oznacza tylko ulice

# Obsługa:
	Skróty klawiszowe:
		- spacja - następny wpis(lub znaczenie)
		- ctrl+q/Escape - wyjście z potwierdzeniem
		CRUD:
			- F2 szukanie wpisów
			- F3 dodawanie nowych wpisów
			- F4 edycja bieżącego wpisu
			- ctrl+a/b/c ustaw tryb bieżącego wpisu
			- ctrl+0 - cofnij ilość wylosowań bieżącego wpisu
			- ctrl+z zerowanie ilości wylosowań/trybów dla słówek/ulic
		- ctrl+t zmień bieżący tryb
		- ctrl+s pokaż statystyki
		- ctrl+p eksportuj jako pdf ulice/słówka
		- ctrl+*/+/- zerowanie/powiększanie/zmniejszanie rozmiaru czcionki
		- F1 - pokaż tą pomoc

# Dopiski słówek i ulic:
	Można utworzyć pliki dopiski_ulice oraz dopiski_slowka zawierające nowe wpisy(w ustawieniach określa się nazwy tych plików).
	O wykryciu tych niepustych plików informują Labele w lewym górnym rogu. 
	Nowe wpisy są liczone i wykrywany jest język nowych słówek.
	Po kliknięciu na te Labele nowe wpisy zostaną dodane do lista_slowek z tłumaczeniem '...' lub do lista_ulic
	Jest to ułatwiona forma dodawania nowych wpisów.
	Słówka dostaną rozpoznanie języka i zostaną dopisane po kliknięciu na Label.
	Puste linie są pomijane. Liczby są pomijane. Jeśli zawiera polskie znaki diakrytyczne to automatycznie pl.

## Zastosowane technologie:
	python/tkinter, git/github, vim, linux(debian), agile.
