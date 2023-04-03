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

OverallQual = symbols('OverallQual')
GrLivArea = symbols('GrLivArea')

src1 = Source(dotprint(-0.780779862738334*OverallQual*(-0.808061842334957*GrLivArea - 0.191938157665043)*(0.284172086137939*OverallQual + 1)))
src1.render()
