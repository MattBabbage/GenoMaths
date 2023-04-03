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

minval = -100
maxval = 100

a = (x ** 4 + x ** 3 + x ** 2 + x + 1)
df = []
n_data_points = 200
for i in range(0, n_data_points):
    noise_val = random.normal(loc=0, scale=10)
    noise_ans = random.normal(loc=0, scale=10)
    sub1 = randint(minval, maxval)
    b = sympify(a).subs([(x, sub1)])
    ans = b.evalf()
    df.append([sub1 + noise_val, ans + noise_ans])

#Show Data with noise
print(df)
q = [3,5]
t,i = sp.symbols('t,i')
x = np.array(range(minval,maxval))
y= (x ** 4 + x ** 3 + x ** 2 + x + 1)
plt.plot(x,y, label=r"$" + f"{sp.latex(a)}" + r"$")
plt.scatter([row[0] for row in df], [row[1] for row in df], label='Noisy Datapoints', color='b', s=10, marker="o")
plt.legend()
plt.show()

a = np.asarray(df)
np.savetxt("data.csv", a, delimiter=",")
#pd.DataFrame(df).to_csv("data.csv")
df = pd.read_csv("data.csv")
print(df)

x = symbols('x')
symbol_list = [x, x]
fittest, score, best_array, average_array, q1_array, q3_array, fittest_array, timings = genetic_algorithm(symbol_list, fitness, 60, 40, 0.8, 0.2, df)
pd.DataFrame([best_array, average_array, q1_array, q3_array, timings]).to_csv("output.csv")

types = [Mul, Add]
ex_array = []
#Add Goal
ex_array.append(x ** 4 + x ** 3 + x ** 2 + x + 1)
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