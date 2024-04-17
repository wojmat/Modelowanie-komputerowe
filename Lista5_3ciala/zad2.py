import numpy as np
import matplotlib.pyplot as plt

# Stałe i parametry symulacji
G = 1  # Stała grawitacyjna
m1 = m2 = 1.0  # Masy ciał są równe 1
R = 1  # Zakładamy, że odległość między ciałami na początku to 1
v_range = np.linspace(0.01, 1, 200) 
dt = 0.001  # Większy krok czasowy 
T = 100  

# Funkcja obliczająca siłę grawitacji
def oblicz_sile_grawitacji(m1, m2, r):
    return G * m1 * m2 / r**2

# Symulacja dla różnych prędkości początkowych
d1_d2_ratios = []
orbits = []

for v in v_range:
    x = np.array([0.0, R])
    y = np.array([0.0, 0.0])
    vx = np.array([0.0, 0.0])
    vy = np.array([-v, v])

    x_traj, y_traj = [], []
    for t in np.arange(0, T, dt):
        r = np.hypot(x[1] - x[0], y[1] - y[0])
        Fg = oblicz_sile_grawitacji(m1, m2, r)
        Fx = Fg * (x[1] - x[0]) / r
        Fy = Fg * (y[1] - y[0]) / r

        vx[1] += Fx / m2 * dt
        vy[1] += Fy / m2 * dt
        x[1] += vx[1] * dt
        y[1] += vy[1] * dt

        x_traj.append(x[1])
        y_traj.append(y[1])

    orbits.append((x_traj, y_traj))

    d1 = max(x_traj) - min(x_traj)
    d2 = max(y_traj) - min(y_traj)
    d1_d2_ratios.append(d1 / d2 if d2 else 1)

# Rysowanie wykresów
plt.figure(figsize=(8, 12))

# Wykres orbity dla każdej prędkości początkowej
plt.subplot(2, 1, 1)
for x_traj, y_traj in orbits:
    plt.plot(x_traj, y_traj)
plt.title('Orbity ciał')
plt.xlabel('x')
plt.ylabel('y')
plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.gca().set_aspect('equal', adjustable='box')

# Wykres stosunku d1/d2 w funkcji prędkości początkowej v
plt.subplot(2, 1, 2)
plt.plot(v_range, d1_d2_ratios, 'o-', markersize=3)
plt.axvline(np.sqrt(G * (m1 + m2) / R), color='r', linestyle='--', label='Teoretyczna v dla okręgu')
plt.title('Stosunek d1/d2 w zależności od prędkości początkowej')
plt.xlabel('Prędkość początkowa v')
plt.ylabel('Stosunek d1/d2')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
