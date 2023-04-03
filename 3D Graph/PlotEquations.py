import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from graphviz import Source
from Libraries.GeneticAlgorithm import *
from Libraries.Fitness import *
from Libraries.LinkedTree import *
import matplotlib.pyplot as plt
import sympy as sp
import numpy as np
from matplotlib import pyplot as plt
#Show Data with noise
from IPython.display import display
import seaborn
seaborn.set(style='ticks')
from sympy import symbols
from sympy import lambdify

minval = -100
maxval = 100

df = pd.read_csv("equations.csv")


fig = plt.figure(figsize=(12, 12))

line = fig.add_subplot(projection='3d')

x = np.arange(minval, maxval, 1)
y = np.arange(minval, maxval, 1)

x, y = np.meshgrid(x, y)
Z = -15 * x ** 2 + x ** 3 + 20 - y**3
line.plot_surface(x, y, Z, cmap=plt.cm.binary)


A = (-y - 3)*(y*(0.781366347714115*y - 2) + 7)
line.plot_surface(x, y, A, cmap=plt.cm.BuGn)

line.text2D(0.05, 0.95, "Original (Black/White) - (-15 * x ** 2 + x ** 3 + 20 - y**3)", transform=line.transAxes)
line.text2D(0.05, 0.90, "Best GA Indiv (Blue/Green) - ((-y - 3)*(y*(0.781366347714115*y - 2) + 7))", transform=line.transAxes)
plt.legend()
plt.show()

src1 = Source((-y - 3)*(y*(0.781366347714115*y - 2) + 7))
src1.render()
