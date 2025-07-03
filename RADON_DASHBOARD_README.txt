
RADON DASHBOARD – PLIKI I INSTRUKCJE

📁 Pliki wymagane w folderze:
-------------------------------------
1. radon_data.csv
   – plik z danymi pomiarowymi (patrz: struktura poniżej)

2. logo_pw.png
   – logo Politechniki Warszawskiej (kwadratowe)

3. logo_ahs.png
   – logo Akademeia High School (kwadratowe)

4. disclaimer_content.html
   – plik HTML z treścią disclaimera (PL/EN) i przełącznikami językowymi

5. radon_dashboard.py
   – główny skrypt Pythona generujący interaktywny dashboard


📦 Wymagane biblioteki Pythona:
-------------------------------------
Zainstaluj w terminalu:
pip install pandas folium plotly branca matplotlib

Jeśli używasz Jupyter/Colab:
!pip install pandas folium plotly branca matplotlib


🧾 Struktura danych w pliku CSV (radon_data.csv):
---------------------------------------------------
Plik powinien mieć nagłówki (w pierwszym wierszu):

- well_id                – unikalny identyfikator punktu (np. PAD-1)
- well_name              – opis/nazwa punktu (np. Sadyba 2)
- district               – dzielnica Warszawy
- radon                  – stężenie radonu (liczba zmiennoprzecinkowa)
- uncertainty            – niepewność pomiaru (opcjonalnie)
- unit                   – jednostka (np. Bq/L)
- longitude              – współrzędna geograficzna (E)
- latitude               – współrzędna geograficzna (N)
- comment                – dodatkowe uwagi (opcjonalnie)
- recent/historical      – 'recent' dla nowych, 'historical' dla archiwalnych

Uwaga: współrzędne powinny być zapisane z kropką, np.:
latitude: 52.21634
longitude: 21.03228


🖼️ Efekt działania:
----------------------
Po uruchomieniu pliku radon_dashboard.py zostanie wygenerowany plik:
    radon_dashboard.html

Zawiera:
- mapę punktów pomiarowych i mapę cieplną
- warstwy do przełączania (lewy górny róg)
- interaktywny wykres Plotly z suwakiem (maks. 30 punktów)
- podpięty disclaimer z przełącznikiem PL/EN (prawy górny róg)
- całość działa offline – wystarczy otworzyć HTML w przeglądarce
