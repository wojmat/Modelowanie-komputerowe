import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)  # For repeatability
n_steps = 1000
n_simulations = 10000
final_positions = []

for _ in range(n_simulations):
    steps = np.random.choice([-1, 1], size=n_steps)  # Random steps
    final_position = np.sum(steps)  # Adding steps to get the final position
    final_positions.append(final_position)

# Creating a histogram
plt.figure(figsize=(10, 6))
plt.hist(final_positions, bins=50, color='blue', alpha=0.7)
plt.title('Histogram końcowych pozycji po 1000 krokach')
plt.xlabel('Końcowa pozycja')
plt.ylabel('Liczba wystąpień')
plt.grid(True)
plt.show()
