import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from graphviz import Source
from Libraries.GeneticAlgorithm import *
from Libraries.Fitness import *
from Libraries.LinkedTree import *
import matplotlib.pyplot as plt
import sympy as sp
import numpy as np
from matplotlib import pyplot as plt

x = symbols('x')
y = symbols('y')

minval = -100
maxval = 100

z = (-15 * x ** 2 + x ** 3 + 20 - y**3)
df = []
n_data_points = 200
for i in range(0, n_data_points):
    noise_val_1 = random.normal(loc=0, scale=10)
    noise_val_2 = random.normal(loc=0, scale=10)
    noise_ans = random.normal(loc=0, scale=10)
    sub1 = randint(minval, maxval)
    sub2 = randint(minval, maxval)
    b = sympify(z).subs([(x, sub1),(y, sub2)])
    ans = b.evalf()
    df.append([sub1 + noise_val_1, sub2 + noise_val_2, ans + noise_ans])


fig = plt.figure(figsize=(12, 12))

line = fig.add_subplot(projection='3d')

x = np.arange(minval, maxval, 1)
y = np.arange(minval, maxval, 1)

x, y = np.meshgrid(x, y)
Z = -15 * x ** 2 + x ** 3 + 20 - y**3
line.plot_surface(x, y, Z, cmap = plt.cm.cividis)

line.scatter([row[0] for row in df], [row[1] for row in df], [row[2] for row in df])
plt.show()

#Reset X and Y
x = symbols('x')
y = symbols('y')

a = np.asarray(df)
np.savetxt("data.csv", a, delimiter=",")
#pd.DataFrame(df).to_csv("data.csv")
df = pd.read_csv("data.csv")
print(df)

x = symbols('x')
y = symbols('y')

symbol_list = [x, y]
fittest, score, best_array, average_array, q1_array, q3_array, fittest_array, timings = genetic_algorithm(symbol_list, fitness, 100, 20, 0.8, 0.2, df)
pd.DataFrame([best_array, average_array, q1_array, q3_array, timings]).to_csv("output.csv")

types = [Mul, Add]
ex_array = []
#Add Goal
ex_array.append(z)
#Add Attempts
for i in range(0, len(fittest_array)):
    print(i)
    e = S.Zero
    e = GetExpressionFromTree(fittest_array[i], e, types)
    ex_array.append(e)
    print(e)


pd.DataFrame(ex_array).to_csv("equations.csv")

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(best_array, 'r-')
ax.plot(q1_array, 'r-.')
ax.plot(q3_array, 'g-.')
ax.plot(average_array, 'b-.')
ax.set_xlabel('Generation')
ax.set_ylabel('Fitness')
ax.ticklabel_format(useOffset=False)
ax.set_yscale('log')
ax.axhline(y=0, color='k')
plt.gca().invert_yaxis()
plt.show()

