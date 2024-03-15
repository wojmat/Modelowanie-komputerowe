import matplotlib.pyplot as plt

# Dane wejściowe dla 1,000,000 rzutów kostką
numery_pol = list(range(1, 41))  # numery pól od 1 do 40

# Dane liczby wizyt i procentów szans
procent_szans = [
    2.2848, 2.2983, 2.329, 2.3934, 2.3337, 2.3075, 2.2606, 2.2989, 2.3096, 2.3005,
    2.3007, 2.3128, 2.3684, 2.4917, 2.5246, 2.6322, 2.6938, 2.7955, 2.7427, 2.7031, 
    2.7275, 2.7138, 2.6655, 2.6598, 2.6694, 2.71, 2.7067, 2.6903, 2.6747, 2.6853,
    2.6834, 2.6894, 2.6116, 2.5319, 2.4754, 2.403, 2.2927, 2.1945, 2.2558, 2.2775

]

# Utworzenie histogramu
plt.figure(figsize=(14, 7))
plt.bar(numery_pol, procent_szans, color='orange', edgecolor='black')

# Dodanie etykiet i tytułu
plt.title('Histogram prawdopodobieństwa zajęcia pola w grze Monopoly dla 1,000,000 rzutów')
plt.xlabel('Numer Pola')
plt.ylabel('Procent szans (%)')

# Ustawienie zakresu osi y
plt.ylim(0, max(procent_szans))

# Wyświetlenie siatki
plt.grid(axis='y', linestyle='--', linewidth=0.5)

# Zapisanie wykresu do pliku na pulpicie
output_file = f'C:/Users/Administrator/Desktop/monopoly_histogram_1000000_rolls.png'
plt.savefig(output_file)

# Pokazanie wykresu
plt.show()
