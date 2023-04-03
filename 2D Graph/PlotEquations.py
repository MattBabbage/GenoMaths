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
import seaborn
from sympy import *
from graphviz import Source
seaborn.set(style='ticks')

#pd.DataFrame(df).to_csv("data.csv")
df = pd.read_csv("equations.csv")

from sympy import symbols
from numpy import linspace
from sympy import lambdify

scatter_df = pd.read_csv("data.csv")
print(scatter_df)
#plt.plot(x,y, label=r"$" + f"{sp.latex(df.iloc[0, 1])}" + r"$")
plt.scatter([row[1] for row in scatter_df], [row[2] for row in scatter_df], label='Noisy Datapoints', color='b', s=10, marker="o")
plt.show()

x = symbols('x')

print(df)
print(df.shape)
cleanplot = sp.plotting.plot(show=false, legend=True)

y = sympify(df.iloc[0, 1])
print(y)
lam_x = lambdify(x, y, modules=['numpy'])
x_vals = np.array(range(-1000, 1000))
y_vals = lam_x(x_vals)
plt.plot(x_vals, y_vals, 'k--', label= str(df.iloc[0, 1]) + " (Goal) ")

for i in range(1, df.shape[0]):
    y = sympify(df.iloc[i, 1])
    lam_x = lambdify(x, y, modules=['numpy'])
    x_vals = np.array(range(-1000, 1000))
    y_vals = lam_x(x_vals)
    plt.plot(x_vals, y_vals, label=str(df.iloc[i, 1]))
    src1 = Source(dotprint(y))
    src1.render()

plt.axvline(x=0, c="grey")
plt.axhline(y=0, c="grey")
plt.legend()
plt.show()




    # q = [3, 5]
    # #t, i = sp.symbols('t,i')
    # x = np.array(range(-1000, 1000))
    # y = (-15 * x ** 2 + x ** 3 + 20)
    # y = sympify(df.iloc[i, 1])
    # print(y)
    # p1 = sp.plotting.plot(y,show=false, label = df.iloc[i, 0], legend=True)
    # cleanplot.extend(p1)

#cleanplot.show()
    # plt.plot(x, y, label=r"$" + f"{sp.latex(y)}" + r"$")
    # plt.legend()
    # plt.show()

# q = [3,5]
# t,i = sp.symbols('t,i')
# x = np.array(range(-1000,1000))
# y= (-15 * x ** 2 + x ** 3 + 20)
# plt.plot(x,y, label=r"$" + f"{sp.latex(df[5])}" + r"$")
# plt.legend()
# plt.show()