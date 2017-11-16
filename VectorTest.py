import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from Lib import *
import mpl_toolkits.mplot3d.axes3d as axes3d

# theta, phi =  np.pi / 2, np.linspace(0, 2 * np.pi, 50)
# theta, phi = np.linspace(0, 2 * np.pi, 50) , np.pi / 2


#=================coefficient==================================
vectorLength = 0.3
theta, phi = np.pi / 2 , np.linspace(0, 2 * np.pi, 50)
THETA, PHI = np.meshgrid(theta, phi)
R = 3
yRotate = 90
xRotate = 90
#==============================================================


X = R * np.sin(THETA) * np.cos(PHI)
Y = R * np.sin(THETA) * np.sin(PHI)
Z = R * np.cos(THETA)
fig = plt.figure()



# X, Y, Z = vectorRotate(X, Y, Z, 'x', 90)
ax = fig.add_subplot(2,2,1, projection='3d')
plot = ax.plot_wireframe(X,Y,Z)
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_zlim(-3, 3)
ax.set_xlabel("x axis")
ax.set_ylabel("y axis")
ax.set_zlabel("z axis")
#================================================================
ax2 = fig.add_subplot(2,2,2, projection='3d')
Ax, Ay, Az = zVectorCircle(X, Y, Z)
plot = ax2.quiver(X, Y, Z, Ax, Ay, Az, length=vectorLength, normalize=True)
ax2.set_title("Original circle loop")
ax2.set_xlim(-3, 3)
ax2.set_ylim(-3, 3)
ax2.set_zlim(-3, 3)
ax2.set_xlabel("x axis")
ax2.set_ylabel("y axis")
ax2.set_zlabel("z axis")
#================================================================

rxX, rxY, rxZ = vectorRotate(X, Y, Z, 'x', xRotate)
rxAx, rxAy, rxAz = vectorRotate(Ax, Ay, Az, 'x', xRotate)
ax3 = fig.add_subplot(2,2,3, projection='3d')

plot = ax3.quiver(rxX, rxY, rxZ, rxAx, rxAy, rxAz, length=vectorLength, normalize=True)
ax3.set_title("Rotation {} degree along x".format(xRotate))
ax3.set_xlim(-3, 3)
ax3.set_ylim(-3, 3)
ax3.set_zlim(-3, 3)
ax3.set_xlabel("x axis")
ax3.set_ylabel("y axis")
ax3.set_zlabel("z axis")
#================================================================

ryX, ryY, ryZ = vectorRotate(X, Y, Z, 'y', yRotate)
ryAx, ryAy, ryAz = vectorRotate(Ax, Ay, Az, 'y', yRotate)
ax4 = fig.add_subplot(2,2,4, projection='3d')

plot = ax4.quiver(ryX, ryY, ryZ, ryAx, ryAy, ryAz, length=vectorLength, normalize=True)
ax4.set_title("Rotation {} degree along y".format(yRotate))
ax4.set_xlim(-3, 3)
ax4.set_ylim(-3, 3)
ax4.set_zlim(-3, 3)
ax4.set_xlabel("x axis")
ax4.set_ylabel("y axis")
ax4.set_zlabel("z axis")





# plot = ax.plot_surface(
#     X, Y, Z, rstride=1, cstride=1,
#     cmap=plt.get_cmap('jet'),
#     linewidth=0, antialiased=False, alpha=0.7)

plt.show()