import matplotlib.pyplot as plt

# Dane wejściowe
numery_pol = list(range(1, 41))  # numery pól od 1 do 40

procent_szans = [
    3, 5, 1, 2, 2, 5, 1, 0, 3, 3,
    2, 1, 8, 1, 2, 3, 2, 2, 5, 3,
    1, 3, 4, 2, 5, 0, 2, 3, 1, 5,
    2, 2, 4, 1, 1, 1, 5, 2, 1, 1
]

# Utworzenie histogramu
plt.figure(figsize=(12, 6))
plt.bar(numery_pol, procent_szans, color='skyblue', edgecolor='black')

# Dodanie etykiet i tytułu
plt.title('Histogram prawdopodobieństwa zajęcia pola w grze Monopoly dla 100 rzutów')
plt.xlabel('Numer Pola')
plt.ylabel('Procent szans (%)')

# Ustawienie zakresu osi y
plt.ylim(0, max(procent_szans) + 1)

# Wyświetlenie siatki
plt.grid(axis='y', linestyle='--', linewidth=0.5)

# Zapisanie wykresu do pliku
output_file = f'C:/Users/Administrator/Desktop/monopoly_histogram_100_rolls.png'
plt.savefig(output_file)

# Pokazanie wykresu
plt.show()
