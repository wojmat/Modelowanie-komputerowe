import numpy as np
import matplotlib.pyplot as plt

# Inicjalizacja stałych
N = 2
G = 1
m = np.ones(N)  # masy
R = 1  # promień orbity

# Inicjalizacja położeń i prędkości
x = np.zeros(N)
y = np.zeros(N)
vx = np.zeros(N)
vy = np.zeros(N)

x[1] = R
vy[1] = np.sqrt(G * m[0] / R)

# Funkcja do obliczania siły grawitacji
def oblicz_sile_grawitacji(x, y, m):
    Fx = np.zeros(N)
    Fy = np.zeros(N)
    for i in range(N):
        for j in range(N):
            if i != j:
                dx = x[j] - x[i]
                dy = y[j] - y[i]
                r = np.sqrt(dx**2 + dy**2)
                Fg = G * m[i] * m[j] / r**3
                Fx[i] += Fg * dx
                Fy[i] += Fg * dy
    return Fx, Fy

# Analiza błędu dla różnych wartości Delta t
dt_values = np.arange(0.000001, 0.1, 0.001)
errors = []

for dt in dt_values:
    # Reset pozycji i prędkości
    x[1] = R
    y[1] = 0
    vx[1] = 0
    vy[1] = np.sqrt(G * m[0] / R)
    
    # Symulacja
    for t in np.arange(0, 10, dt):
        Fx, Fy = oblicz_sile_grawitacji(x, y, m)
        for i in range(1, N):  # Pomijamy aktualizację dla i = 0 (ciało nieruchome)
            vx[i] += Fx[i] / m[i] * dt
            vy[i] += Fy[i] / m[i] * dt
            x[i] += vx[i] * dt
            y[i] += vy[i] * dt

    # Obliczanie błędu
    r_final = np.sqrt((x[1] - x[0])**2 + (y[1] - y[0])**2)
    error = abs(R - r_final)
    errors.append(error)
# Wykres błędu w funkcji Delta t z logarytmiczną skalą osi X
plt.plot(dt_values, errors)
plt.xscale('log')  # Ustawienie skali logarytmicznej dla osi X
plt.yscale('log')
plt.xlabel('Delta t (logarytmicznie)')
plt.ylabel('Błąd')
plt.title('Błąd w funkcji kroku czasowego Delta t (skala logarytmiczna)')
plt.show()

# Znalezienie maksymalnej wartości Delta t dla błędu mniejszego niż 10^-5
indeksy = np.where(np.array(errors) < 1e-5)[0]
if indeksy.size > 0:  # Sprawdzenie, czy znaleziono jakiekolwiek odpowiednie wartości Delta t
    max_dt = dt_values[indeksy[-1]]
    print(f"Maksymalna wartość Delta t z błędem mniejszym niż 10^-5: {max_dt}")
else:
    print("Nie znaleziono wartości Delta t z błędem mniejszym niż 10^-5 w podanym zakresie.")
