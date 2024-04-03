import numpy as np

N = 2  
G = 1

x = np.zeros(N)
y = np.zeros(N)
vx = np.zeros(N)
vy = np.zeros(N)

m = np.ones(N)

x[1] = 1 
vy[1] = np.sqrt(G)  

dt = 0.01  
czas_symulacji = 10 

for t in np.arange(0, czas_symulacji, dt):
    for i in range(N):
        Fx, Fy = 0, 0  
        
        for j in range(N):
            if i != j:
                dx = x[j] - x[i]
                dy = y[j] - y[i]
                r = np.sqrt(dx**2 + dy**2)
                
                Fg = G * m[i] * m[j] / r**3
                Fx += Fg * dx
                Fy += Fg * dy

                
        if r > 0:  # Unikamy dzielenia przez 0
            ax = Fx / m[i]
            ay = Fy / m[i]

            # Aktualizacja danych
            if i != 0:
                vx[i] += ax * dt
                vy[i] += ay * dt
                x[i] += vx[i] * dt
                y[i] += vy[i] * dt
