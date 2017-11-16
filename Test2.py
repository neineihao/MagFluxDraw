import numpy as np

x, y, z = 0, -3, 0
r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
sinTheta = np.sqrt(x ** 2 + y ** 2) / r
cosTheta = z / r
cosPhi = x / np.sqrt(x ** 2 + y ** 2)
sinPhi = y / np.sqrt(x ** 2 + y ** 2)

print("Sin theta = {}".format(sinTheta))

Ax, Ay, Az = 0, -cosTheta * r, -sinTheta * r

print("When X, Y, Z = {},{},{}".format(x,y,z))
print("The vector will be {},{},{}".format(Ax,Ay,Az))