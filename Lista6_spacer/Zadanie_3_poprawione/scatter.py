import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)  # Dla powtarzalności wyników
n_steps = 1000
n_simulations = 10000
final_positions = [np.sum(np.random.choice([-1, 1], size=n_steps)) for _ in range(n_simulations)]

# Tworzenie scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(range(n_simulations), final_positions, alpha=0.7, c='blue', edgecolors='none', s=10)
plt.title('Scatter plot końcowych pozycji po 1000 krokach')
plt.xlabel('Numer symulacji')
plt.ylabel('Końcowa pozycja')
plt.grid(True)
plt.show()
