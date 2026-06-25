# Password Generator (aplikacja konsolowa)

Prosty generator haseł w Pythonie.

Przykłady użycia komend, w zależności od pożądanych warunków jakie ma spełniać wygenerowane hasło:
	python main.py	//opcja domyślna do generowania hasła o długości 12 znaków, zawierającego wielkie i małe litery, cyfry oraz symbole
	
	python main.py --length 16
	
	python main.py --length 16 --no-symbols
	
	python main.py --length 10 --no-symbols --no-digits --no-ambiguous
	
	python main.py --length 10 --no-require --copy

Opis opcji użycia:
- --no-upper     //wyklucza wielkie litery
- --no-digits    //wyklucza cyfry
- --no-symbols   //wyklucza symbole
- --no-ambiguous //wyklucz znaki mylące (l, 1, I, 0, O)
- --no-require   //nie wymusza obecności znaku z każdej wybranej kategorii
- --copy         //skopiuje wynik do schowka (wymaga pyperclip: pip install -r requirements.txt)

Można też sprawdzić wszystkie dostępne argumenty za pomocą: python main.py --help

Dodatek:
Wyświetlana jest także informacja o sile wygenerowanego hasła (słabe, średnie, silne) w zależności od jego długości i złożoności.
Jest to tzw. entropia hasła, która jest obliczana na podstawie ilości możliwych kombinacji znaków w haśle. 
Im większa entropia, tym trudniej jest odgadnąć hasło.
