import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

soa = np.array([[0, 0, 1, 1, -2, 0], [0, 0, 2, 1, 1, 0],
                [0, 0, 3, 2, 1, 0], [0, 0, 4, 0.5, 0.7, 0]])

Testmesh = np.arange(-0.8, 1, 0.1)
print("Mesh Test is {}".format(Testmesh))


X, Y, Z, U, V, W = zip(*soa)
print("X = {}, Y = {}, Z = {}, U = {}, V = {}, W = {}".format(X, Y, Z, U, V, W))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.quiver(X, Y, Z, U, V, W)
ax.set_xlim([-5, 5])
ax.set_ylim([-5, 5])
ax.set_zlim([-5, 5])
plt.show()