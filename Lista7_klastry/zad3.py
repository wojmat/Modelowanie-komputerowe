import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve

def hexagonal_neighbors():
    # Hexagonal kernel for convolution to find neighbors in a triangular grid
    return np.array([[1, 1, 1],
                     [1, 0, 1],
                     [1, 1, 1]])

def grow_snowflake(grid, rule):
    kernel = hexagonal_neighbors()
    neighbors = convolve(grid, kernel, mode='constant', cval=0)
    
    if rule == 1:
        new_grid = (grid == 1) | (neighbors >= 1)
    elif rule == 2:
        new_grid = (grid == 1) | (neighbors >= 2)
    elif rule == 3:
        new_grid = (grid == 1) | (neighbors > 0)
    else:
        raise ValueError("Invalid rule specified.")
    
    return new_grid.astype(int)

def simulate_snowflake_growth(size, steps, rule):
    grid = np.zeros((size, size), dtype=int)
    center = size // 2
    grid[center, center] = 1
    
    grids = [grid.copy()]
    for _ in range(steps):
        grid = grow_snowflake(grid, rule)
        grids.append(grid.copy())
    
    return grids

def plot_snowflake(grids):
    fig, axes = plt.subplots(1, len(grids), figsize=(15, 5))
    for i, ax in enumerate(axes):
        ax.imshow(grids[i], cmap='Blues')
        ax.axis('off')
    plt.show()

# Parameters
size = 101
steps = 6

# Simulate and plot for each rule
for rule in [1, 2, 3]:
    grids = simulate_snowflake_growth(size, steps, rule)
    plot_snowflake(grids)
