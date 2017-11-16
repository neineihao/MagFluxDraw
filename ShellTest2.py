import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import mpl_toolkits.mplot3d.axes3d as axes3d

theta, phi = np.linspace(0, 2 * np.pi, 40), np.linspace(0, np.pi, 40)
THETA, PHI = np.meshgrid(theta, phi)
R = 10
X = R * np.sin(PHI) * np.cos(THETA)
Y = R * np.sin(PHI) * np.sin(THETA)
Z = R * np.cos(PHI)
fig = plt.figure()
ax = fig.add_subplot(1,1,1, projection='3d')



normalx = X/np.amax(X)

print("x after normalize : {}".format(normalx))

my_col = cm.jet(normalx)


plot = ax.plot_surface(
    X, Y, Z, rstride=1, cstride=1,
    # cmap=plt.get_cmap('jet'),
    facecolors = my_col,
    linewidth=0, antialiased=False, alpha=0.5)

plt.show()