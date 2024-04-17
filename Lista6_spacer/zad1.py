import matplotlib.pyplot as plt
import numpy as np
import random

# Ilość liczb do wygenerowania
n = 1000000

# Generowanie 1mln liczb za pomocą generatora Mersenne-Twister z numpy
x = np.random.randint(0, 1000000, n)

# Generowanie 1mln liczb za pomocą prostego generatora opartego na operacji modulo
random.seed(0)  # Ustawienie ziarna dla powtarzalności
y = [random.randrange(0, 1000000) % 1000000 for _ in range(n)]

# Histogramy
bins = 10000

# Histogram dla Mersenne-Twister
hist_x, bins_x = np.histogram(x, bins=bins)

# Histogram dla generatora opartego na operacji modulo
hist_y, bins_y = np.histogram(y, bins=bins)

# Tworzenie histogramów
plt.figure(figsize=(14, 7))
plt.hist(x, bins=bins, alpha=0.5, label='Mersenne-Twister', color='blue')
plt.hist(y, bins=bins, alpha=0.5, label='Modulo Operation', color='red')
plt.legend(loc='upper right')
plt.title('Porównanie histogramów dla 1mln liczb wygenerowanych różnymi metodami')
plt.xlabel('Zakres wartości')
plt.ylabel('Liczba wystąpień')
plt.show()

# Wyświetlanie różnicy między kubełkami
differences = np.abs(hist_x - hist_y)
print("Średnia różnica między kubełkami: ", np.mean(differences))
print("Maksymalna różnica między kubełkami: ", np.max(differences))

np.savetxt("histogram_mersenne_twister.csv", hist_x, delimiter=",")
np.savetxt("histogram_modulo.csv", hist_y, delimiter=",")
