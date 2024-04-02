import re
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

def analyze_zipfs_law(file_paths, output_files):
    plt.figure(figsize=(10, 6))

    for file_path, output_file in zip(file_paths, output_files):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read().lower()

        # Usuwanie znaków interpunkcyjnych
        text = re.sub(r'[^\w\s]', '', text)
        words = text.split()
        count = Counter(words)
        frequencies = sorted(count.items(), key=lambda x: x[1], reverse=True)

        # Zapisywanie statystyk do pliku tekstowego
        with open(output_file, 'w', encoding='utf-8') as f:
            for word, frequency in frequencies:
                f.write(f"{word}: {frequency}\n")

        # Generowanie danych do wykresu
        ranks = np.arange(1, len(frequencies) + 1)
        values = np.array([freq for _, freq in frequencies])

        # Logarytmowanie danych
        log_ranks = np.log(ranks)
        log_values = np.log(values)

        # Dopasowanie liniowe w przestrzeni log-log
        slope, intercept = np.polyfit(log_ranks, log_values, 1)
        b = -slope  # Wykładnik prawa Zipfa
        c = np.exp(intercept)  # Stała c po przekształceniu z logarytmu

        # Obliczanie dopasowanych wartości
        fitted_values = c * ranks**(-b)

        # Dodawanie serii danych do wykresu
        plt.loglog(ranks, values, marker='o', linestyle='none', label=f'Obserwowane - {file_path}')
        plt.loglog(ranks, fitted_values, label=f'c*r^b - {file_path}\n$y = {c:.2f} \\times r^{{{-b:.2f}}}$', linestyle='--')

    plt.xlabel('Ranga', fontsize = 12)
    plt.ylabel('Częstotliwość', fontsize = 12)
    plt.title('Prawo Zipfa', fontsize = 16)
    plt.legend()
    plt.show()

analyze_zipfs_law(['pustynia.txt', 'ksiaze.txt', 'szatan.txt'], ['wynik1.txt', 'wynik2.txt', 'wynik3.txt'])
