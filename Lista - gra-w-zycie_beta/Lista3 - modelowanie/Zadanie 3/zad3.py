import numpy as np
import scipy.stats

def create_grid(size, p0=0.1):
    """Tworzenie nowej siatki z losowymi stanami początkowymi oraz z zadanym prawdopodobieństwem p0."""
    return np.random.choice([0, 1], size=(size, size), p=[1-p0, p0])

def update_grid(grid):
    """Aktualizacja siatki na podstawie reguł automatu komórkowego."""
    size = len(grid)
    new_grid = grid.copy()
    for row in range(size):
        for col in range(size):
            total = sum([grid[(row + i) % size][(col + j) % size] for i in range(-1, 2) for j in range(-1, 2)]) - grid[row][col]
            if grid[row][col] == 1 and (total < 2 or total > 3):
                new_grid[row][col] = 0
            elif grid[row][col] == 0 and total == 3:
                new_grid[row][col] = 1
    return new_grid

def run_simulation(size, p0, Tmax):
    grid = create_grid(size, p0)
    for _ in range(Tmax):
        grid = update_grid(grid)
    return np.mean(grid)

def perform_experiments(sizes, p0, Tmax, N):
    results = {}
    errors = {}

    for size in sizes:
        densities = [run_simulation(size, p0, Tmax) for _ in range(N)]
        mean_density = np.mean(densities)
        se = scipy.stats.sem(densities)  # Obliczanie błędu standardowego
        results[size] = mean_density
        errors[size] = se

    return results, errors

# Parametry eksperymentu
sizes = [10, 100, 200, 500, 1000]
p0 = 0.6
Tmax = 1000
N = 100

# Przeprowadzenie eksperymentów
results, errors = perform_experiments(sizes, p0, Tmax, N)

# Wyświetlenie wyników
print("Rozmiar planszy | Średnia gęstość żywych komórek | Błąd standardowy")
for size in sizes:
    print(f"{size:>13} | {results[size]:>34} | {errors[size]:>15}")
