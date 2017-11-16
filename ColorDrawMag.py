import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from Lib import *
import mpl_toolkits.mplot3d.axes3d as axes3d

theta, phi = np.linspace(0, np.pi, 50), np.linspace(0, 2 * np.pi, 50)
THETA, PHI = np.meshgrid(theta, phi)
R = 5
X = R * np.sin(THETA) * np.cos(PHI)
Y = R * np.sin(THETA) * np.sin(PHI)
Z = R * np.cos(THETA)
# print("X : {}".format(X))
vx, vy, vz = zcloseLoopFluxDensity(X, Y, Z, 0.000001, 200000000)
Yvx, Yvy, Yvz = rotateYLoopFluxDensity(X, Y, Z, 0.000001, 200000000)
Zvx, Zvy, Zvz = rotateXLoopFluxDensity(X, Y, Z, 0.000001, 200000000)
tvx1, tvy1, tvz1 = rotateCircleLoop(X, Y, Z, 0.000001, 200000000, 'y', 'z', 120)
tvx2, tvy2, tvz2 = rotateCircleLoop(X, Y, Z, 0.000001, 200000000, 'y', 'z', 240)


# tvx, tvy, tvz = rotateXLoopFluxDensity(X, Y, Z, 0.000001, 200000000)
# vx, vy, vz = vectorRotate(vx, vy, vz, 'x', 90)


# Xvx, Xvy, Xvz = xcloseLoopFluxDensity(X, Y, Z, 0.1, 200000000,THETA,PHI)
# Yvx, Yvy, Yvz = ycloseLoopFluxDensity(X, Y, Z, 0.1, 200000000,THETA,PHI)
# Zvx, Zvy, Zvz = zcloseLoopFluxDensity(X, Y, Z, 0.1, 200000000,THETA,PHI)
# vx2, vy2, vz2 = vectorRotate(vx, vy, vz, 'x', 90)

vT = lambda v1,v2,v3,v4: v1 + v2 + v3 + v4
#Set the Rx node normal vector
rxx, rxy, rxz = 1, 1, 1
# rxx, rxy, rxz = vectorRotate(rxx, rxy, rxz, "x", 45)
intensity = vx * rxx + vy * rxy + vz * rxz
intensity2 = Yvx * rxx + Yvy * rxy + Yvz * rxz
intensity3 = abs(vT(vx, Yvx, tvx1, tvx2) * rxx + vT(vy, Yvy, tvy1, tvy2) * rxy + vT(vz, Yvz, tvz1, tvz2) * rxz)
# intensity3 = abs(tvx * rxx + tvy * rxy + tvz * rxz)
# intensity = vT(Xvx, Yvx, Zvx) * rxx + vT(Xvy, Yvy, Zvy) * rxy

# intensity = vT(Xvx, Yvx, Zvx) * rxx + vT(Xvy, Yvy, Zvy) * rxy + vT(Zvx, Zvy, Zvz) * rxz
# print("intensity is {}".format(intensity))
# intensity = abs(intensity)
normal = intensity / np.nanmax(intensity)
my_col = cm.jet(normal)

normal2 = intensity2 / np.nanmax(intensity2)
my_col2 = cm.jet(normal2)

normal3 = intensity3 / np.nanmax(intensity3)
my_col3 = cm.jet(normal3)
#====================Plot The Data=============================
#==============================================================

fig = plt.figure()
ax = fig.add_subplot(2,2,1, projection='3d')
plot = ax.plot_surface(
    X, Y, Z, rstride=1, cstride=1,
    # cmap=plt.get_cmap('jet'),
    facecolors = my_col,
    linewidth=0, antialiased=False, alpha=0.7)

ax.set_title("Tx:Z direction loop")
ax.set_xlabel("x axis")
ax.set_ylabel("y axis")
ax.set_zlabel("z axis")

ax2 = fig.add_subplot(2,2,2, projection='3d')
plot = ax2.plot_surface(
    X, Y, Z, rstride=1, cstride=1,
    # cmap=plt.get_cmap('jet'),
    facecolors = my_col2,
    linewidth=0, antialiased=False, alpha=0.7)
ax2.set_title("Tx:X direction loop")
ax2.set_xlabel("x axis")
ax2.set_ylabel("y axis")
ax2.set_zlabel("z axis")

ax3 = fig.add_subplot(2,2,3, projection='3d')
plot = ax3.plot_surface(
    X, Y, Z, rstride=1, cstride=1,
    # cmap=plt.get_cmap('jet'),
    facecolors = my_col3,
    linewidth=0, antialiased=False, alpha=0.7)
ax3.set_title("Tx:Rotate Y along Z axis 270 degree with absolute")
ax3.set_xlabel("x axis")
ax3.set_ylabel("y axis")
ax3.set_zlabel("z axis")

plt.show()

#==============================================================
#==============================================================