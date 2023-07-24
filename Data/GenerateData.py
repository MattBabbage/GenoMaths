import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sympy import Symbol
from sympy import symbols
from sympy import sympify
from random import *
from matplotlib import pyplot as plt
import numpy as np

x, y, z = symbols("x,y,z")

eq = y + x**2 + y**3
df = []
n_data_points = 200
minval = -10
maxval = 10

for i in range(0, n_data_points):
    noise_val_1 = np.random.normal(loc=0, scale=0)
    noise_val_2 = np.random.normal(loc=0, scale=0)
    noise_ans = np.random.normal(loc=0, scale=0)
    sub1 = randint(minval, maxval)
    sub2 = randint(minval, maxval)
    b = sympify(eq).subs([(x, sub1),(y, sub2)])
    ans = b.evalf()
    df.append([sub1 + noise_val_1, sub2 + noise_val_2, ans + noise_ans])

fig = plt.figure(figsize=(12, 12))

line = fig.add_subplot(projection='3d')

x = np.arange(minval, maxval, 1)
y = np.arange(minval, maxval, 1)

x, y = np.meshgrid(x, y)

Z = y + x**2 + y**3
line.plot_surface(x, y, Z)

line.scatter([row[0] for row in df], [row[1] for row in df], [row[2] for row in df])
plt.show()

np.savetxt("train.csv", df, header="x,y,z", delimiter=",", fmt="%i", comments='')
# columns = ['x', 'y', 'z']
# pdf = pd.DataFrame(df)
# pdf = pdf[columns]
# pdf.to_csv("equations.csv")
#
#
train_df = pd.read_csv("train.csv")
print("end")