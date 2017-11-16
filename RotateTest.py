from Lib import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from pyquaternion import Quaternion

v = [0, 0, 1]
axis = [0, 1, 0]
theta = -np.pi/2  # radian
vX, vY, vZ = Quaternion(axis=axis, angle=theta).rotate(v)

print("rotate Vector : {}".format(vX))

fig = plt.figure()
ax = fig.add_subplot(2,1,1, projection='3d')

ax.quiver(0, 0, 0, v[0], v[1], v[2], length=1, normalize=True)
ax.quiver(0, 0, 0, vX, vY, vZ, length=1, normalize=True)
ax.set_xlabel("x axis")
ax.set_ylabel("y axis")
ax.set_zlabel("z axis")

ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_zlim(-3, 3)

plt.show()
# print(np.dot(rotation_matrix(axis,theta), v))

