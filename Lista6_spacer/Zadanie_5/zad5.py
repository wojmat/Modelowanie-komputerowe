import numpy as np

def simulate_random_walk(steps, directions):
    if directions == 4:
        moves = np.random.choice(range(4), size=steps)
        sin_move = np.sin(moves * np.pi / 2)
        cos_move = np.cos(moves * np.pi / 2)
    elif directions == 8:
        moves = np.random.choice(range(8), size=steps)
        angle = moves * np.pi / 4
        sin_move = np.sin(angle)
        cos_move = np.cos(angle)

    x = np.cumsum(cos_move)
    y = np.cumsum(sin_move)
    msd = np.mean(x[-1]**2 + y[-1]**2)
    return msd

def calculate_diffusion_coefficient(steps, num_simulations, directions):
    msds = [simulate_random_walk(steps, directions) for _ in range(num_simulations)]
    mean_msd = np.mean(msds)
    diffusion_coefficient = mean_msd / (4 * steps)
    return diffusion_coefficient

# Parameters
steps = 10000
num_simulations = 1000

# Calculate diffusion coefficients
D_4 = calculate_diffusion_coefficient(steps, num_simulations, 4)
D_8 = calculate_diffusion_coefficient(steps, num_simulations, 8)

print(f"Współczynnik dyfuzji dla 4 kierunków: {D_4}")
print(f"Współczynnik dyfuzji dla 8 kierunków: {D_8}")
