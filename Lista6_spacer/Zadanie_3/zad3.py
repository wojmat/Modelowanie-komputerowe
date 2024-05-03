import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)  # Ustawienie ziarna dla powtarzalności wyników
n_steps = 1000
n_simulations = 10000
final_positions = []

for _ in range(n_simulations):
    steps = np.random.choice([-1, 1], size=n_steps)  # Losowanie kroków
    final_position = np.sum(steps)  # Sumowanie kroków, aby uzyskać końcową pozycję
    final_positions.append(final_position)

# Tworzenie histogramu
plt.figure(figsize=(10, 6))
plt.hist(final_positions, bins=50, color='blue', alpha=0.7)
plt.title('Histogram końcowych pozycji po 1000 krokach')
plt.xlabel('Końcowa pozycja')
plt.ylabel('Liczba wystąpień')
plt.grid(True)
plt.show()

# Obliczanie prawdopodobieństwa znalezienia się w odległości 1 i 30 jednostek
distance_1 = final_positions.count(1)
distance_30 = final_positions.count(30)

print(f"Liczba wystąpień na odległość 1 od startu: {distance_1}")
print(f"Liczba wystąpień na odległość 30 od startu: {distance_30}")
