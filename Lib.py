import math
import numpy as np

def xyz2ThetaPhi(x, y, z):
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    sinPhi = y / np.sqrt(x ** 2 + y ** 2)
    cosPhi = x / np.sqrt(x ** 2 + y ** 2)
    sinTheta = np.sqrt(x ** 2 + y ** 2) / r
    cosTheta = z / r
    return r, sinPhi, cosPhi, sinTheta, cosTheta


# def sphV2carV(Ar, Atheta, Aphi, x, y, z, theta, phi):
#     r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
#     sinTheta = np.sin(theta)
#     cosTheta = np.cos(theta)
#     sinPhi = np.sin(phi)
#     cosPhi = np.cos(phi)
#     Ax = sinTheta * cosPhi * Ar + cosPhi * cosTheta * Atheta - sinPhi * Aphi
#     Ay = sinTheta * sinPhi * Ar + sinPhi * cosTheta * Atheta + cosPhi * Aphi
#     Az = cosTheta * Ar - sinTheta * Atheta
#
#     # print("In the Cartesian coordinates the vector will be:")
#     # print("{} * ax + {} * ay + {} * az".format(Ax, Ay, Az))
#     # print("The radios is {}".format(r))
#     return Ax, Ay, Az

def sphV2carV(Ar, Atheta, Aphi, x, y, z):
    r, sinPhi, cosPhi, sinTheta, cosTheta = xyz2ThetaPhi(x, y, z)
    Ax = sinTheta * cosPhi * Ar + cosPhi * cosTheta * Atheta - sinPhi * Aphi
    Ay = sinTheta * sinPhi * Ar + sinPhi * cosTheta * Atheta + cosPhi * Aphi
    Az = cosTheta * Ar - sinTheta * Atheta

    return Ax, Ay, Az


def zcloseLoopFluxDensity(x, y, z, b, i):
    r, sinPhi, cosPhi, sinTheta, cosTheta = xyz2ThetaPhi(x, y, z)
    # r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    # sinTheta = np.sin(theta)
    # cosTheta = np.cos(theta)
    mu = 4 * np.pi * 10 ** (-7)
    coefficient = mu * i * b ** 2 / (4 * r ** 3)
    # print("coefficient = {}".format(coefficient))
    Ar = 2 * cosTheta * coefficient
    Atheta = 1 * sinTheta * coefficient
    Aphi = 0

    Ax, Ay, Az = sphV2carV(Ar, Atheta, Aphi, x, y, z)
    return Ax, Ay, Az

def xcloseLoopFluxDensity(x, y, z, b, i, theta, phi):
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    sinTheta = np.sin(theta)
    cosTheta = np.cos(theta)
    sinPhi = np.sin(phi)
    cosPhi = np.cos(phi)
    tanTheta = np.tan(theta)
    mu = 4 * np.pi * 10 ** (-7)
    coefficient = mu * i * b ** 2 / (4 * r ** 3)
    # print("coefficient = {}".format(coefficient))
    Ar = cosPhi * coefficient
    Atheta = 0
    Aphi = sinPhi * sinTheta * coefficient

    Ax, Ay, Az = sphV2carV(Ar, Atheta, Aphi, x, y, z)
    return Ax, Ay, Az

def rotateYLoopFluxDensity(x, y, z, b, i):
    rx, ry, rz = vectorRotate(x, y, z, 'y', -90)
    Ax, Ay, Az = zcloseLoopFluxDensity(rx, ry, rz, b, i)
    rAx, rAy, rAz = vectorRotate(Ax, Ay, Az, 'y', 90)

    return rAx, rAy, rAz

def rotateXLoopFluxDensity(x, y, z, b, i):
    rx, ry, rz = vectorRotate(x, y, z, 'x', -90)
    Ax, Ay, Az = zcloseLoopFluxDensity(rx, ry, rz, b, i)
    rAx, rAy, rAz = vectorRotate(Ax, Ay, Az, 'x', 90)

    return rAx, rAy, rAz

def rotateCircleLoop(x, y, z, b, i, direction, axis, theta):
    rx, ry, rz = vectorRotate(x, y, z, axis, -theta)

    if direction == "x":
        Ax, Ay, Az = rotateXLoopFluxDensity(rx, ry, rz, b, i)
        rAx, rAy, rAz = vectorRotate(Ax, Ay, Az, axis, theta)

    elif direction == "y":
        Ax, Ay, Az = rotateYLoopFluxDensity(rx, ry, rz, b, i)
        rAx, rAy, rAz = vectorRotate(Ax, Ay, Az, axis, theta)

    elif direction == "z":
        Ax, Ay, Az = zcloseLoopFluxDensity(rx, ry, rz, b, i)
        rAx, rAy, rAz = vectorRotate(Ax, Ay, Az, axis, theta)

    else:
        print("Error, Please enter the direction of loop !!!")
        rAx = 0
        rAy = 0
        rAz = 0
    return rAx, rAy, rAz


def ycloseLoopFluxDensity(x, y, z, b, i, theta, phi):
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    sinTheta = np.sin(theta)
    cosTheta = np.cos(theta)
    sinPhi = np.sin(phi)
    cosPhi = np.cos(phi)
    mu = 4 * np.pi * 10 ** (-7)
    coefficient = mu * i * b ** 2 / (4 * r ** 3)
    Ar =  sinPhi * coefficient
    Atheta = 0
    Aphi = - cosPhi * sinTheta *  coefficient
    Ax, Ay, Az = sphV2carV(Ar, Atheta, Aphi, x, y, z,)
    return Ax, Ay, Az

def zVectorCircle(x,y,z):
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    sinPhi = y / np.sqrt(x ** 2 + y ** 2)
    cosPhi = x / np.sqrt(x ** 2 + y ** 2)
    Ax = -sinPhi
    Ay = cosPhi
    return Ax, Ay, 0

def xVectorCircle(x, y, z, theta, phi):
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    Ax, Ay, Az = np.cos(theta) * r, 0, -np.sin(theta) * r

    return Ax, Ay, Az

def yVectorCircle(x,y,z,theta,phi):
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    Ax, Ay, Az = 0, np.cos(theta) * r, -np.sin(theta) * r

    return Ax, Ay, Az

def vectorRotate(x, y, z, axis, theta):
    sin =  math.sin(math.radians(theta))
    cos =  math.cos(math.radians(theta))
    if axis == "x":
        Ax = x
        Ay = y * cos - z * sin
        Az = y * sin + z * cos
    elif axis == "y":
        Ax = x * cos + z * sin
        Ay = y
        Az = - x * sin + z * cos
    elif axis == "z":
        Ax = x * cos - y * sin
        Ay = x * sin + y * cos
        Az = z
    else:
        print("Error by enter wrong axis !!!")
        Ax = 0
        Ay = 0
        Az = 0
    return Ax, Ay, Az



if __name__ == '__main__':
    mu = 4 * math.pi * 10 ** (-7)
    print(mu)