from sympy import *
import math

x, y, z = symbols('x y z')
integ = Integral( (1 + z * sin(y) * sin(x)) * (sin(x) * cos(x)) , (x, -pi/2 , pi/2 ) )

print("result is {}".format(integ.doit()))