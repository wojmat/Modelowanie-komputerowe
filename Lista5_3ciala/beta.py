import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Stałe
G = 1  # Stała grawitacyjna
m = np.array([1.0, 1.0])  # Masy ciał
v_range = np.linspace(0.01, 1, 100)  # Zakres prędkości początkowych

# Parametry symulacji
dt = 0.0001  # Krok czasowy
T = 10       # Całkowity czas symulacji

def oblicz_sily_grawitacyjne(x, y, m):
    """Oblicz siły grawitacyjne między dwoma ciałami."""
    Fx = np.zeros_like(x)
    Fy = np.zeros_like(y)
    for i in range(len(x)):
        for j in range(i + 1, len(x)):
            dx = x[j] - x[i]
            dy = y[j] - y[i]
            r = np.sqrt(dx**2 + dy**2)
            Fg = G * m[i] * m[j] / r**2
            Fx[i] -= Fg * dx / r
            Fy[i] -= Fg * dy / r
            Fx[j] += Fg * dx / r
            Fy[j] += Fg * dy / r
    return Fx, Fy

# Przechowuj wyniki symulacji do wykresów
wszystkie_trajektorie = []
wspolczynniki_d1_d2 = []

for v in v_range:
    x = np.array([0.0, 1.0])
    y = np.array([0.0, 0.0])
    vx = np.array([0.0, 0.0])
    vy = np.array([-v, v])

    trajektoria_danych = []

    for t in np.arange(0, T, dt):
        Fx, Fy = oblicz_sily_grawitacyjne(x, y, m)
        vx += Fx / m * dt
        vy += Fy / m * dt
        x += vx * dt
        y += vy * dt

        trajektoria_danych.append([x[0], y[0], x[1], y[1]])

    trajektoria_danych = np.array(trajektoria_danych)
    wszystkie_trajektorie.append(trajektoria_danych)

    d1 = np.max(trajektoria_danych[:, 0]) - np.min(trajektoria_danych[:, 0])
    d2 = np.max(trajektoria_danych[:, 1]) - np.min(trajektoria_danych[:, 1])
    wspolczynnik_d1_d2 = d1 / d2 if d2 != 0 else 0
    wspolczynniki_d1_d2.append(wspolczynnik_d1_d2)

# Wykres trajektorii i stosunków d1/d2
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
for trajektoria in wszystkie_trajektorie:
    plt.plot(trajektoria[:, 0], trajektoria[:, 1], label=f'Trajektoria ciała 1 przy v={v:.2f}')
    plt.plot(trajektoria[:, 2], trajektoria[:, 3], label=f'Trajektoria ciała 2 przy v={v:.2f}', linestyle='--')
plt.xlabel('Pozycja X')
plt.ylabel('Pozycja Y')
plt.title('Trajektoria dwóch ciał')

plt.subplot(1, 2, 2)
plt.plot(v_range, wspolczynniki_d1_d2, 'o-', markersize=2)
oczekiwane_v = np.sqrt(G * (m[0] + m[1]))
plt.axvline(x=oczekiwane_v, color='r', linestyle='--', label=f'Oczekiwane v={oczekiwane_v:.2f} dla orbity okrężnej')
plt.xlabel('Prędkość początkowa v')
plt.ylabel('Stosunek d1/d2')
plt.title('Stosunek wymiarów elipsy vs. prędkość początkowa')
plt.legend()
plt.show()
