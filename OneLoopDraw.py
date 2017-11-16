from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from Lib import *




#=================coefficient==================================
theta, phi = np.linspace(0, np.pi, 10), np.linspace(0, 2 * np.pi, 20)
# theta, phi = np.linspace(0, 2 * np.pi, 10), np.linspace( np.pi / 2, np.pi / 2, 10)
THETA, PHI = np.meshgrid(theta, phi)
R = 3

vectorlength = 0.5
yRotate = 90
xRotate = 90
#==============================================================

X = R * np.sin(THETA) * np.cos(PHI)
Y = R * np.sin(THETA) * np.sin(PHI)
Z = R * np.cos(THETA)

vx, vy, vz = zcloseLoopFluxDensity(X, Y, Z, 0.1, 200000000)

vx2, vy2, vz2 = vectorRotate(vx, vy, vz, 'y', 90)
X2, Y2, Z2 = vectorRotate(X, Y, Z, 'y', 90)

vx3, vy3, vz3 = vectorRotate(vx, vy, vz, 'x', 90)
X3, Y3, Z3 = vectorRotate(X, Y, Z, 'x', 90)

tvx, tvy, tvz = rotateXLoopFluxDensity(X, Y, Z, 0.1, 200000000)



#====================Plot The Data=============================
#==============================================================
fig = plt.figure()
ax = fig.add_subplot(2,2,1, projection='3d')
ax.quiver(X, Y, Z, vx, vy, vz, length=vectorlength, normalize=True)
ax.set_xlabel("x axis")
ax.set_ylabel("y axis")
ax.set_zlabel("z axis")
ax.set_title("Distribution of magnetic flux density")
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_zlim(-3, 3)

axtest = fig.add_subplot(2,2,2, projection='3d')
axtest.set_title("Rotation {} degree along x".format(yRotate))
axtest.quiver(X, Y, Z, vx3, vy3, vz3, length=vectorlength, normalize=True)
axtest.set_xlabel("x axis")
axtest.set_ylabel("y axis")
axtest.set_zlabel("z axis")

#
# ax2 = fig.add_subplot(2,2,3, projection='3d')
# ax2.set_title("Rotation {} degree along y".format(yRotate))
# ax2.quiver(X2, Y2, Z2, vx2, vy2, vz2, length=vectorlength, normalize=True)
# ax2.set_xlabel("x axis")
# ax2.set_ylabel("y axis")
# ax2.set_zlabel("z axis")
#
# ax3 = fig.add_subplot(2,2,4, projection='3d')
# ax3.set_title("Rotation {} degree along x".format(yRotate))
# ax3.quiver(X3, Y3, Z3, vx3, vy3, vz3, length=vectorlength, normalize=True)
# ax3.set_xlabel("x axis")
# ax3.set_ylabel("y axis")
# ax3.set_zlabel("z axis")




ax4 = fig.add_subplot(2,2,3, projection='3d')
ax4.set_title("Rotate both vector and position")
ax4.quiver(X, Y, Z, tvx, tvy, tvz, length=vectorlength, normalize=True)
ax4.set_xlabel("x axis")
ax4.set_ylabel("y axis")
ax4.set_zlabel("z axis")

plt.show()

#==============================================================
#==============================================================
