import matplotlib.pyplot as plt

# Load data
x, y = [], []
with open("random_walk_2D.txt", "r") as file:
    for line in file:
        parts = line.strip().split(',')
        x.append(float(parts[0]))
        y.append(float(parts[1]))

# Plot
plt.figure(figsize=(8, 8))
plt.plot(x, y, marker='o', markersize=2)
plt.title("2D Random Walk")
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.grid(True)
plt.show()
