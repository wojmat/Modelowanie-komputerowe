import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Constants
G = 1  # Gravitational constant
m1, m2 = 1.0, 1.0  # Masses of the bodies
v_range = np.linspace(0.01, 1, 100)  # Range of initial velocities

# Simulation parameters
dt = 0.0001  # Time step
T = 10       # Total simulation time

def compute_gravitational_forces(x, y, m):
    """Compute gravitational forces between two bodies."""
    Fx = np.zeros_like(x)
    Fy = np.zeros_like(y)
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    r = np.sqrt(dx**2 + dy**2)
    Fg = G * m1 * m2 / r**2
    Fx[0] = Fg * dx / r
    Fy[0] = Fg * dy / r
    Fx[1] = -Fx[0]
    Fy[1] = -Fy[0]
    return Fx, Fy

# Store simulation results for plotting
d1_d2_ratios = []
selected_trajectories = [20, 40, 60, 80]  # Indices of v_range to plot for clarity

plt.figure(figsize=(10, 5))

# Plot the trajectories for selected velocities
for idx, v in enumerate(v_range):
    x = np.array([0.0, 1.0])
    y = np.array([0.0, 0.0])
    vx = np.array([0.0, 0.0])
    vy = np.array([-v, v])
    
    x_positions = []
    y_positions = []

    for t in np.arange(0, T, dt):
        Fx, Fy = compute_gravitational_forces(x, y, m)
        vx += Fx / np.array([m1, m2]) * dt
        vy += Fy / np.array([m1, m2]) * dt
        x += vx * dt
        y += vy * dt

        if idx in selected_trajectories:
            x_positions.append(x.copy())
            y_positions.append(y.copy())

    d1 = np.max(x_positions) - np.min(x_positions)
    d2 = np.max(y_positions) - np.min(y_positions)
    d1_d2_ratio = d1 / d2 if d2 != 0 else 0
    d1_d2_ratios.append(d1_d2_ratio)

    if idx in selected_trajectories:
        x_positions = np.array(x_positions)
        y_positions = np.array(y_positions)
        plt.plot(x_positions[:, 0], y_positions[:, 0], label=f'v={v:.2f}')

plt.xlabel('X position')
plt.ylabel('Y position')
plt.title('Selected Trajectories of Body 1')
plt.legend()
plt.grid(True)

# Plot d1/d2 ratio
plt.figure(figsize=(10, 5))
plt.plot(v_range, d1_d2_ratios, 'o-', markersize=2)
expected_v = np.sqrt(G * m2**2 / (m1 + m2))
plt.axvline(x=expected_v, color='r', linestyle='--', label=f'Expected v={expected_v:.2f} for circular orbit')
plt.xlabel('Initial velocity v')
plt.ylabel('Ratio d1/d2')
plt.title('Ellipse Dimension Ratio vs. Initial Velocity')
plt.legend()
plt.grid(True)
plt.show()
