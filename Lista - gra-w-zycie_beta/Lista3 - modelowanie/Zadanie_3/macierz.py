import numpy as np
import scipy.stats
import scipy.signal
from concurrent.futures import ThreadPoolExecutor # Próba wykorzystania wielowątkowości
import concurrent.futures

def create_grid(size, p0=0.1):
    """Tworzenie nowej siatki z losowymi stanami początkowymi oraz z zadanym prawdopodobieństwem p0."""
    return np.random.choice([0, 1], size=(size, size), p=[1-p0, p0])

def update_grid(grid):
    """Aktualizacja siatki na podstawie reguł automatu komórkowego z wykorzystaniem operacji splotu."""
    # Dodanie brzegów z toroidalnymi warunkami brzegowymi
    extended_grid = np.pad(grid, 1, mode='wrap')
    # Definiowanie jądra splotu dla sąsiadujących komórek
    kernel = np.array([[1, 1, 1],
                       [1, 0, 1],
                       [1, 1, 1]])
    neighbors = scipy.signal.convolve2d(extended_grid, kernel, mode='same', boundary='wrap')[1:-1, 1:-1]
    # Stosowanie reguł Gry w Życie
    new_grid = ((neighbors == 3) | ((grid == 1) & (neighbors == 2))).astype(int)
    return new_grid

def run_simulation(size, p0, Tmax):
    grid = create_grid(size, p0)
    for _ in range(Tmax):
        grid = update_grid(grid)
    return np.mean(grid)

def perform_experiment(size, p0, Tmax, N):
    """Przeprowadzanie serii eksperymentów dla jednego rozmiaru planszy."""
    return [run_simulation(size, p0, Tmax) for _ in range(N)]

def perform_experiments(sizes, p0, Tmax, N):
    """Przeprowadzanie eksperymentów dla różnych rozmiarów planszy."""
    results = {}
    errors = {}
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(perform_experiment, size, p0, Tmax, N): size for size in sizes}
        for future in concurrent.futures.as_completed(futures):
            size = futures[future]
            densities = future.result()
            mean_density = np.mean(densities)
            se = scipy.stats.sem(densities) if N > 1 else 0  # Obliczanie błędu standardowego
            results[size] = mean_density
            errors[size] = se
    return results, errors

# Parametry badania
sizes = [10, 100, 200, 500, 1000]
p0 = 0.3
Tmax = 1000
N = 100

# Przeprowadzenie badań
results, errors = perform_experiments(sizes, p0, Tmax, N)

# Wyświetlenie wyników
print("Rozmiar planszy | Średnia gęstość żywych komórek | Błąd standardowy")
for size in sizes:
    print(f"{size:>13} | {results[size]:>34} | {errors[size]:>15}")
