import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from Lib import *

fig = plt.figure()
PHI = np.linspace(0, 2 * np.pi, 360)
THETA = np.pi / 2
R = 5

X = R * np.sin(THETA) * np.cos(PHI)
Y = R * np.sin(THETA) * np.sin(PHI)
Z = R * np.cos(THETA)

vx, vy, vz = zcloseLoopFluxDensity(X, Y, Z, 0.000001, 200000000)
Yvx, Yvy, Yvz = rotateYLoopFluxDensity(X, Y, Z, 0.000001, 200000000)
Xvx, Xvy, Xvz = rotateXLoopFluxDensity(X, Y, Z, 0.000001, 200000000)

vT = lambda v1, v2, v3: v1 + v2 + v3
rxx, rxy, rxz = 1, 1, 1

densityResult = abs(vT(vx, Yvx, Xvx) * rxx + vT(vy, Yvy, Xvy) * rxy + vT(vz, Yvz, Xvz) * rxz)
normalizeResult = densityResult / np.nanmax(densityResult)
print("The result after normalize: {}".format(normalizeResult))

# print("The degree: {}".format(np.degrees(PHI)))
# print("Shape of the PHI : {}".format(np.shape(PHI)))
# print("Shape of the result : {}".format(np.shape(normalizeResult)))


normalizeResult = normalizeResult.reshape(1,360)
x_axis = np.degrees(PHI)
x_axis = x_axis.reshape(1,360)
ax = fig.add_subplot(111)
# print("Shape of the PHI : {}".format(np.shape(PHI)))
# print("Shape of the result : {}".format(np.shape(normalizeResult)))

ax.plot(x_axis, normalizeResult, 'bo')
bluePath = mpatches.Patch(color='Blue', label='Intensity')

ax.legend(handles=[bluePath])
plt.ylabel("Density")
plt.xlabel("Degree")
plt.show()