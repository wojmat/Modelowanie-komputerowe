import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)  # Dla powtarzalności wyników
n_steps = 1000
n_simulations = 10000
final_positions = [np.sum(np.random.choice([-1, 1], size=n_steps)) for _ in range(n_simulations)]

# Tworzenie histogramu z dokładniejszym podziałem na kubełki i bez przerw
plt.figure(figsize=(10, 6))
plt.hist(final_positions, bins=np.arange(min(final_positions)-0.5, max(final_positions)+1.5, 1), color='blue', alpha=0.7)
plt.title('Histogram końcowych pozycji po 1000 krokach')
plt.xlabel('Końcowa pozycja')
plt.ylabel('Liczba wystąpień')
plt.grid(True)
plt.show()
