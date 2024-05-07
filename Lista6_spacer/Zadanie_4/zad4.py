import numpy as np

def simulate_random_walk(dimension, steps):
    position = np.zeros(dimension)
    for _ in range(steps):
        move_direction = np.random.randint(0, 2*dimension)
        axis = move_direction // 2
        direction = 1 if move_direction % 2 == 0 else -1
        position[axis] += direction
        if np.all(position == 0):
            return True
    return False

def calculate_return_probability(dimension, num_walks, walk_length):
    successes = 0
    for _ in range(num_walks):
        if simulate_random_walk(dimension, walk_length):
            successes += 1
    return successes / num_walks

for d in range(1, 4):
    probability = calculate_return_probability(d, 1000, 1000)
    print(f"Prawdopodobieństwo powrotu do punktu zerowego w {d}D: {probability:.4f}")
