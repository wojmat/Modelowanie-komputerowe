import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load data
x, y, z = [], [], []
with open("random_walk_3D.txt", "r") as file:
    for line in file:
        parts = line.strip().split(',')
        x.append(float(parts[0]))
        y.append(float(parts[1]))
        z.append(float(parts[2]))

# Plot
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, marker='o', markersize=2)
ax.set_title("3D Random Walk")
ax.set_xlabel("X Coordinate")
ax.set_ylabel("Y Coordinate")
ax.set_zlabel("Z Coordinate")
plt.show()
