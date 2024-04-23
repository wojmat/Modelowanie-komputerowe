import numpy as np
import matplotlib.pyplot as plt

# Parametry symulacji
G = 1.0  # Stała grawitacyjna
k = 1.0  # Stała sprężystości
m = 10  # Masa każdego z ciał
dt = 0.01  # Krok czasowy
t_max = 10  # Czas symulacji
steps = int(t_max / dt)

# Pozycje i prędkości początkowe
positions = np.array([
    [3.4722222222222197, 4.555555555555556],
    [1.3749999999999982, -2.847222222222224],
    [-4.819444444444439, -1.7777777777777795]
])
velocities = np.zeros_like(positions)  # Początkowe prędkości zerowe

# Obliczanie sił w zależności od potencjału
def compute_forces(pos, use_gravitational=True):
    n = len(pos)
    forces = np.zeros_like(pos)
    for i in range(n):
        for j in range(i + 1, n):
            r = pos[j] - pos[i]
            dist = np.linalg.norm(r)
            if use_gravitational:
                force = G * m**2 * r / dist**3  # Siła grawitacyjna zależna od odległości
            else:
                force = k * r  # Siła sprężystości proporcjonalna do odległości
            forces[i] += force
            forces[j] -= force
    return forces

# Symulacja dla obu potencjałów
for use_grav in [True, False]:
    pos = np.copy(positions)
    vel = np.zeros_like(positions)
    traj = []  # Trajektoria - lista zawierająca kolejne położenia
    vel_traj = []  # Trajektoria prędkości - lista zawierająca kolejne prędkości

    for step in range(steps):
        forces = compute_forces(pos, use_gravitational=use_grav)
        vel += forces / m * dt
        pos += vel * dt
        traj.append(pos.copy())
        vel_traj.append(vel.copy())

    traj = np.array(traj)
    vel_traj = np.array(vel_traj)

    # Generowanie macierzy rekurencji
    nit = len(traj)
    R = np.zeros((nit, nit))
    for i in range(nit):
        for j in range(nit):
            R[i, j] = np.linalg.norm(traj[i] - traj[j])

    # Wykresy
    plt.figure(figsize=(10, 5))
    for i in range(3):
        plt.plot(traj[:, i, 0], traj[:, i, 1], label=f'Ciało {i+1}')
    plt.title(f'Trajektorie {"Grawitacyjny" if use_grav else "Sprężynowy"} Potencjał')
    plt.xlabel('Pozycja X')
    plt.ylabel('Pozycja Y')
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 5))
    for i in range(3):
        plt.plot(vel_traj[:, i, 0], vel_traj[:, i, 1], label=f'Prędkość Ciała {i+1}')
    plt.title(f'Prędkość {"Grawitacyjny" if use_grav else "Sprężynowy"} Potencjał')
    plt.xlabel('Prędkość X')
    plt.ylabel('Prędkość Y')
    plt.legend()
    plt.show()

    # Wykres rekurencji
    plt.figure(figsize=(6, 6))
    plt.imshow(R, origin='lower', cmap='hot', interpolation='none')
    plt.colorbar()
    plt.title(f'Wykres Rekurencji {"Grawitacyjny" if use_grav else "Sprężynowy"} Potencjał')
    plt.xlabel('Indeks i')
    plt.ylabel('Indeks j')
    plt.show()
