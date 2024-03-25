Skrypt Python "zad3.py" jest moją pierwotną próbą obliczenia błędu standardowego dla zadanych wartości w zadaniu.
Jednakże próba generowania wyników zakończyła się pomyślnie tylko dla N = 10, później czas oczekwiania stał się zdecydowanie zbyt długi.
W pliku "macierz.py" z pomocą ChatGPT starałem się jak najbardziej zoptymalizować mój pomysł obliczania tych układów, gdyż próba N = 100 dla tysiąca iteracji była bardzo zasobożerna i czasochłonna.
Zastąpiono wykorzystanie pętli for przez operacje wektorowe na macierzy sąsiadów.
Udało mi się zrealizować próby dla wielkosci układu L [10, 100, 200, 500], L = 1000 była poza zasięgiem mojego sprzętu i skryptu.