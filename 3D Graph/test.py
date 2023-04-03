from sympy import *
from graphviz import Source
from IPython.display import display

x = symbols('x')
y = symbols('y')

src1 = Source(dotprint((-y - 3)*(y*(0.781366347714115*y - 2) + 7)))
src1.render()
