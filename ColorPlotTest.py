import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from Lib import *
import mpl_toolkits.mplot3d.axes3d as axes3d

# theta, phi = np.linspace(0, np.pi, 50), np.linspace(0, 2 * np.pi, 50)
# THETA, PHI = np.meshgrid(theta, phi)
# R = 5

# r, phi = np.linspace(4, 5, 50), np.linspace(0, 2 * np.pi, 100)
# R, PHI = np.meshgrid(r,phi)
# THETA = np.pi / 2

r, theta = np.linspace(4, 5, 50), np.linspace(0, 2 * np.pi, 100)
R, THETA = np.meshgrid(r,theta)
PHI = 0

X = R * np.sin(THETA) * np.cos(PHI)
Y = R * np.sin(THETA) * np.sin(PHI)
Z = R * np.cos(THETA)
print("X : {}".format(Z))
vx, vy, vz = zcloseLoopFluxDensity(X, Y, Z, 0.000001, 200000000)
Yvx, Yvy, Yvz = rotateYLoopFluxDensity(X, Y, Z, 0.000001, 200000000)
Xvx, Xvy, Xvz = rotateXLoopFluxDensity(X, Y, Z, 0.000001, 200000000)



vT = lambda v1,v2,v3: v1 + v2 + v3
#Set the Rx node normal vector
rxx, rxy, rxz = 1, 1, 1

intensity3 = abs(vT(vx, Yvx, Xvx) * rxx + vT(vy, Yvy, Xvy) * rxy + vT(vz, Yvz, Xvz) * rxz)


normal3 = intensity3 / np.nanmax(intensity3)
my_col3 = cm.jet(normal3)


fig = plt.figure()
ax3 = fig.add_subplot(1,1,1, projection='3d')
plot = ax3.plot_surface(
    X, Y, Z, rstride=1, cstride=1,
    # cmap=plt.get_cmap('jet'),
    facecolors = my_col3,
    linewidth=0, antialiased=False, alpha=0.7)
ax3.set_title("Tx:Combination of loop")
ax3.set_xlabel("x axis")
ax3.set_ylabel("y axis")
ax3.set_zlabel("z axis")
ax3.set_xlim(-5, 5)
ax3.set_ylim(-5, 5)
ax3.set_zlim(-5, 5)

plt.show()