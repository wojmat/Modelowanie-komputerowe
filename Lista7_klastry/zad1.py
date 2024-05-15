import pygame
import numpy as np
import random
import matplotlib.pyplot as plt

class Cell:
    def __init__(self, x, y):
        self.position = pygame.math.Vector2(x, y)
        self.free_sides = []

def initialize(size):
    matrix = np.zeros((size, size), dtype=bool)
    start_pos = size // 2
    matrix[start_pos, start_pos] = True
    initial_cell = Cell(start_pos, start_pos)
    return matrix, [initial_cell]

def update_free_sides(cell, matrix, size):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    sides = [4, 2, 3, 1]
    x, y = int(cell.position.x), int(cell.position.y)
    cell.free_sides = [sides[i] for i, (dx, dy) in enumerate(directions)
                       if matrix[(x + dx) % size, (y + dy) % size] == 0]

def grow_cluster(living_cells, matrix, size):
    while True:
        parent_cell = random.choice(living_cells)
        update_free_sides(parent_cell, matrix, size)
        if parent_cell.free_sides:
            break
    side = random.choice(parent_cell.free_sides)
    dx, dy = {1: (0, 1), 2: (1, 0), 3: (0, -1), 4: (-1, 0)}[side]
    new_x, new_y = (int(parent_cell.position.x + dx) % size, int(parent_cell.position.y + dy) % size)
    new_cell = Cell(new_x, new_y)
    living_cells.append(new_cell)
    matrix[new_x, new_y] = True

def calculate_radius(matrix):
    active_cells = np.argwhere(matrix)
    if len(active_cells) == 0:
        return 0
    centroid = np.mean(active_cells, axis=0)
    distances = np.linalg.norm(active_cells - centroid, axis=1)
    return np.mean(distances)

def main():
    pygame.init()
    size = 301
    screen_size = 1000
    screen = pygame.display.set_mode([screen_size, screen_size])
    pygame.display.set_caption('Eden Model Simulation')

    matrix, living_cells = initialize(size)
    num_cells_list = [100, 500, 1000, 5000, 10000, 20000]
    radii = []

    running = True
    clock = pygame.time.Clock()
    cell_count = 1  # Start with the initial cell

    while running:
        # Grow the cluster in batches to reduce rendering frequency
        for _ in range(100):
            if cell_count >= num_cells_list[-1]:
                running = False
                break
            grow_cluster(living_cells, matrix, size)
            cell_count += 1
            if cell_count in num_cells_list:
                radius = calculate_radius(matrix)
                radii.append(radius)
                print(f'Number of cells: {cell_count}, Radius: {radius:.2f}')

        # Render the current state
        screen.fill((0, 0, 0))
        cell_size = screen_size / size
        for cell in living_cells:
            x, y = int(cell.position.x), int(cell.position.y)
            rect = (cell_size * x, cell_size * y, cell_size, cell_size)
            pygame.draw.rect(screen, (255, 255, 255), rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)  # Limit the frame rate to 60 FPS

    pygame.quit()

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(num_cells_list, radii, 'o-', label='Simulated data')
    plt.xlabel('Number of cells (N)')
    plt.ylabel('Radius (r)')
    plt.title('Eden Cluster Growth')
    plt.legend()
    plt.grid(True)

    # Fitting and plotting the expected scaling law
    num_cells_array = np.array(num_cells_list)
    expected_radii = num_cells_array ** 0.5
    plt.plot(num_cells_list, expected_radii, 'r--', label=r'Expected $r \sim N^{1/2}$')
    plt.legend()

    plt.show()

if __name__ == "__main__":
    main()
