import pygame
import numpy as np
import random as rand
import matplotlib.pyplot as plt

class Walker:
    def __init__(self, x, y, w):
        self.where_from = int(w)
        self.x = x
        self.y = y

def initialize(size):
    matrix = np.zeros((size, size), dtype=bool)
    center = size // 2
    matrix[center, center] = True
    return matrix, [[center, center]]

def add_walker(size):
    where_from = rand.randint(1, 4)
    if where_from == 1:
        return Walker(rand.randint(1, size - 1), 1, 1)
    elif where_from == 2:
        return Walker(size - 1, rand.randint(1, size - 1), 2)
    elif where_from == 3:
        return Walker(rand.randint(1, size - 1), size - 1, 3)
    elif where_from == 4:
        return Walker(1, rand.randint(1, size - 1), 4)

def update_walker_position(walker):
    random_walk = rand.randint(0, 1)
    if walker.where_from == 1:
        walker.y += 1
        walker.x += 1 if random_walk == 0 else -1
    elif walker.where_from == 2:
        walker.x -= 1
        walker.y += 1 if random_walk == 0 else -1
    elif walker.where_from == 3:
        walker.y -= 1
        walker.x += 1 if random_walk == 0 else -1
    elif walker.where_from == 4:
        walker.x += 1
        walker.y += 1 if random_walk == 0 else -1

def is_near_cluster(walker, matrix, size):
    x, y = walker.x, walker.y
    return (matrix[(x + 1) % size, y] or
            matrix[x - 1, y] or
            matrix[x, (y + 1) % size] or
            matrix[x, y - 1])

def calculate_radius(DLA):
    xmin = ymin = float('inf')
    xmax = ymax = float('-inf')
    for x, y in DLA:
        if x < xmin:
            xmin = x
        if x > xmax:
            xmax = x
        if y < ymin:
            ymin = y
        if y > ymax:
            ymax = y
    r = (xmax - xmin + ymax - ymin) / 4
    center = ((xmin + xmax) // 2, (ymin + ymax) // 2)
    return r, center

def main():
    size = 301
    screen_size = 1000
    pygame.init()
    screen = pygame.display.set_mode([screen_size, screen_size])
    pygame.display.set_caption('DLA Model Simulation')

    matrix, DLA = initialize(size)
    walkers = []
    cell_amount = 0

    running = True
    clock = pygame.time.Clock()
    
    num_particles_list = [100, 500, 1000, 5000, 10000, 20000]
    radii = []
    
    while running:
        for _ in range(100):  # Batch processing for performance
            walkers.append(add_walker(size))
            for walker in walkers[:]:
                update_walker_position(walker)
                if walker.x < 0 or walker.x >= size or walker.y < 0 or walker.y >= size:
                    walkers.remove(walker)
                    continue
                if is_near_cluster(walker, matrix, size):
                    matrix[walker.x, walker.y] = True
                    DLA.append([walker.x, walker.y])
                    walkers.remove(walker)
                    cell_amount += 1
                    if cell_amount in num_particles_list:
                        radius, center = calculate_radius(DLA)
                        radii.append(radius)
                        print(f'Number of particles: {cell_amount}, Radius: {radius:.2f}')
                    if cell_amount >= num_particles_list[-1]:
                        running = False
                        break
        
        screen.fill((0, 0, 0))
        for x, y in DLA:
            rect = (screen_size / size * x, screen_size / size * y, screen_size / size, screen_size / size)
            pygame.draw.rect(screen, (255, 255, 255), rect)

        if DLA:
            radius, center = calculate_radius(DLA)
            center = (screen_size / size * center[0], screen_size / size * center[1])
            pygame.draw.circle(screen, (255, 0, 0), center, radius * screen_size / size, 2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)

    pygame.quit()

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(num_particles_list, radii, 'o-', label='Simulated data')
    plt.xlabel('Number of particles (N)')
    plt.ylabel('Radius (r)')
    plt.title('DLA Cluster Growth')
    plt.legend()
    plt.grid(True)

    # Fitting and plotting the expected scaling law
    num_particles_array = np.array(num_particles_list)
    expected_radii = num_particles_array ** (1 / 1.7)
    plt.plot(num_particles_list, expected_radii, 'r--', label=r'Expected $r \sim N^{1/1.7}$')
    plt.legend()

    plt.show()

if __name__ == "__main__":
    main()
