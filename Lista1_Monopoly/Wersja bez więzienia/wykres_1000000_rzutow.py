import matplotlib.pyplot as plt

# Dane wejściowe dla 1,000,000 rzutów kostką
numery_pol = list(range(1, 41))  # numery pól od 1 do 40

# Dane liczby wizyt i procentów szans
procent_szans = [
    2.4891, 2.5241, 2.4774, 2.5013, 2.5098, 2.4904, 2.4997, 2.496, 2.4854, 2.518,
    2.5076, 2.5029, 2.4887, 2.4913, 2.5024, 2.4977, 2.5411, 2.4908, 2.5023, 2.5025,
    2.4803, 2.497, 2.4966, 2.4865, 2.534, 2.5089, 2.475, 2.5333, 2.4956, 2.4779,
    2.4789, 2.511, 2.5052, 2.5143, 2.5052, 2.5028, 2.4756, 2.5069, 2.493, 2.5035
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
