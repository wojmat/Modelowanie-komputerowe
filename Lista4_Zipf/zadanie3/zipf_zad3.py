import matplotlib.pyplot as plt
import numpy as np

def analyze_city_populations(file_path):
    cities = []
    populations = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.split()  # Dzielenie wiersza na części
            if len(parts) >= 2:
                city = ' '.join(parts[:-1])  # Wszystko poza ostatnim elementem to nazwa miasta
                population = parts[-1]  # Ostatni element to populacja
                try:
                    # Próba konwersji populacji na int i zapisanie danych
                    population = int(population.replace(',', ''))
                    cities.append(city)
                    populations.append(population)
                except ValueError:
                    # Pominięcie wierszy, których nie można przekształcić w int
                    continue

    # Generowanie danych do wykresu
    ranks = np.arange(1, len(cities) + 1)
    values = np.array(populations)

    # Logarytmowanie danych
    log_ranks = np.log(ranks)
    log_values = np.log(values)

    # Dopasowanie liniowe w przestrzeni log-log
    slope, intercept = np.polyfit(log_ranks, log_values, 1)
    b = -slope  # Wykładnik prawa Zipfa
    c = np.exp(intercept)  # Stała c po przekształceniu z logarytmu

    # Obliczanie dopasowanych wartości
    fitted_values = c * ranks**(-b)

    # Rysowanie wykresów
    plt.figure(figsize=(10, 6))
    plt.loglog(ranks, values, marker='o', linestyle='none', label='Obserwowane dane')
    plt.loglog(ranks, fitted_values, label=f'Dopasowanie: $c \\times r^{{-b}}$\n$c = {c:.2f}, b = {-b:.2f}$', linestyle='--')
    plt.xlabel('Ranga', fontsize=12)
    plt.ylabel('Populacja', fontsize=12)
    plt.title('Prawo Zipfa dla populacji miast', fontsize=16)
    plt.legend()
    plt.show()

# Wywołanie funkcji z ścieżką do pliku zawierającego dane o miastach
analyze_city_populations('miasta.txt')
