import numpy as np
import matplotlib.pyplot as plt
import os

class Point:
    def __init__(self, m, x, y, vx, vy):
        self.m = m  # Masa punktu
        self.x = x  # Pozycja x punktu
        self.y = y  # Pozycja y punktu
        self.vx = vx  # Prędkość w kierunku x
        self.vy = vy  # Prędkość w kierunku y

def gravitational_force(p1, p2, G):
    rx = p2.x - p1.x  # Różnica pozycji x między punktami
    ry = p2.y - p1.y  # Różnica pozycji y między punktami
    distance_squared = rx ** 2 + ry ** 2  # Kwadrat odległości między punktami
    if distance_squared == 0:
        return (0, 0)  # Zapobiegaj dzieleniu przez zero, jeśli oba punkty się pokrywają
    distance_cubed = np.sqrt(distance_squared ** 3)  # Trzecia potęga odległości
    fx = G * p1.m * p2.m * rx / distance_cubed  # Składowa siły grawitacyjnej w kierunku x
    fy = G * p1.m * p2.m * ry / distance_cubed  # Składowa siły grawitacyjnej w kierunku y
    return (fx, fy)

# Ustawienia symulacji
G = 1  # Stała grawitacyjna
Vs = np.arange(0.01, 1, 0.01)  # Zakres prędkości początkowych
dt = 0.001  # Krok czasowy
t = 10  # Całkowity czas symulacji
steps = int(t / dt)  # Liczba kroków

# Katalog do zapisywania danych o pozycji i wykresów
directory = 'pozycje'
if not os.path.exists(directory):
    os.makedirs(directory)

plot_directory = 'wykresy'
if not os.path.exists(plot_directory):
    os.makedirs(plot_directory)

# Obliczenie teoretycznej v dla orbity kołowej
m1 = m2 = 1  # Masy
v_theoretical = np.sqrt((m2**2) / (m1 + m2))

ratios = []  # Lista przechowująca stosunki długości d1 do d2
for v in Vs:
    points = [Point(1, 0, 0, 0, -v), Point(1, 1, 0, 0, v)]  # Utworzenie dwóch punktów
    x1_positions = []  # Lista przechowująca pozycje x pierwszego punktu
    y1_positions = []  # Lista przechowująca pozycje y pierwszego punktu
    position_data = []  # Lista przechowująca dane o pozycji

    for i in range(steps):
        for p in range(len(points)):
            total_fx = total_fy = 0
            for s in range(len(points)):
                if p != s:
                    fx, fy = gravitational_force(points[p], points[s], G)
                    total_fx += fx
                    total_fy += fy

            ax = total_fx / points[p].m
            ay = total_fy / points[p].m
            points[p].vx += ax * dt
            points[p].vy += ay * dt
            points[p].x += points[p].vx * dt
            points[p].y += points[p].vy * dt

        x1_positions.append(points[0].x)
        y1_positions.append(points[0].y)
        position_data.append(f"{points[0].x} {points[0].y} {points[1].x} {points[1].y}")

    # Zapis danych do pliku na koniec symulacji
    file_name = f"{directory}/pozycje_v_{v:.2f}.txt"
    with open(file_name, 'w') as file:
        file.write("\n".join(position_data))

    # Obliczenie i zapisanie stosunków długości d1 do d2 dla wykresu
    d1 = max(x1_positions) - min(x1_positions)
    d2 = max(y1_positions) - min(y1_positions)
    ratio = d1 / d2
    ratios.append(ratio)

# Wykres stosunku długości d1 do d2
plt.figure(figsize=(10, 5))
plt.plot(Vs, ratios, label='Stosunek d1/d2')
plt.axvline(x=v_theoretical, color='r', linestyle='--', label=f'Teoretyczna v dla orbity kołowej = {v_theoretical:.2f}')
plt.title("Stosunek długości d1/d2 w funkcji prędkości początkowej v")
plt.xlabel("Prędkość początkowa v")
plt.ylabel("Stosunek długości d1/d2")
plt.legend()
plt.grid(True)
plot_path = f"{plot_directory}/wykres_stosunek_d1_d2.png"
plt.savefig(plot_path)
plt.close()

# Generowanie i zapisywanie wykresów dla wszystkich trajektorii po zakończeniu wszystkich symulacji
for v in Vs:
    file_name = f"{directory}/pozycje_v_{v:.2f}.txt"
    x1, y1, x2, y2 = [], [], [], []
    with open(file_name, 'r') as file:
        for line in file:
            positions = list(map(float, line.split()))
            x1.append(positions[0])
            y1.append(positions[1])
            x2.append(positions[2])
            y2.append(positions[3])

    plt.figure(figsize=(10, 5))
    plt.plot(x1, y1, label='Ciało 1')
    plt.plot(x2, y2, label='Ciało 2')
    plt.title(f"Trajektoria dla prędkości początkowej v={v:.2f}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plot_path = f"{plot_directory}/trajektoria_v_{v:.2f}.png"
    plt.savefig(plot_path)  # Zapisz wykres
    plt.close()
