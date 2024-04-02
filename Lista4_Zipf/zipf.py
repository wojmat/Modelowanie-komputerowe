import re
from collections import Counter
import matplotlib.pyplot as plt

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
        ranks = range(1, len(frequencies) + 1)
        values = [freq for _, freq in frequencies]

        # Dodawanie serii danych do wykresu
        plt.loglog(ranks, values, label=f'{file_path}')

    plt.xlabel('Ranga')
    plt.ylabel('Częstotliwość')
    plt.title('Prawo Zipfa - porównanie tekstów')
    plt.legend()
    plt.show()

analyze_zipfs_law(['pustynia.txt', 'ksiaze.txt', 'szatan.txt'], ['wynik1.txt', 'wynik2.txt', 'wynik3.txt'])
