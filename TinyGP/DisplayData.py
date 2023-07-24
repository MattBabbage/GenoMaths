# tiny genetic programming by © moshe sipper, www.moshesipper.com
from random import random, randint, seed
from statistics import mean
from copy import deepcopy
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import glob

cumulative_df = pd.DataFrame()

file_paths = glob.glob('*.csv')  # Modify the file path pattern according to your naming convention
num_files = len(file_paths)
cumulative_df = pd.DataFrame()  # Create an empty DataFrame

best_fitness_column_values = []
average_fitness_column_values = []
q1_fitness_column_values = []
q3_fitness_column_values = []

for file_path in file_paths:
    df = pd.read_csv(file_path)
    cumulative_df = cumulative_df.add(df, fill_value=1)  # Add the current DataFrame to the cumulative DataFrame
    best_fitness_column_values.append(df['best_fitness'].tolist())
    average_fitness_column_values.append(df['average_fitness'].tolist())
    q1_fitness_column_values.append(df['q1_fitness'].tolist())
    q3_fitness_column_values.append(df['q3_fitness'].tolist())

average_df = cumulative_df / num_files  # Calculate the average by dividing by the number of files



print(average_df)
best_fitness = average_df['best_fitness']
q1_fitness = average_df['q1_fitness']
average_fitness = average_df['average_fitness']
q3_fitness = average_df['q3_fitness']

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(best_fitness, 'r-')
ax.plot(q1_fitness, 'r-.')
ax.plot(q3_fitness, 'g-.')
ax.plot(average_fitness, 'b-.')
ax.set_xlabel('Generation')
ax.set_ylabel('Fitness')
ax.axhline(y=0, color='k')
plt.title('Average of 50 Runs')
plt.show()


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
for values in best_fitness_column_values:
    plt.plot(values,  'r-')
ax.set_xlabel('Generation')
ax.set_ylabel('Fitness')
#ax.ticklabel_format(useOffset=False)
#ax.set_yscale('log')
ax.axhline(y=0, color='k')
plt.title('Fittest of 50 Runs')
#plt.gca().invert_yaxis()
plt.show()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
for values in average_fitness_column_values:
    plt.plot(values,  'b-.')
ax.set_xlabel('Generation')
ax.set_ylabel('Fitness')
#ax.ticklabel_format(useOffset=False)
#ax.set_yscale('log')
ax.axhline(y=0, color='k')
plt.title('Averagest of 50 Runs')
#plt.gca().invert_yaxis()
plt.show()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
for values in q1_fitness_column_values:
    plt.plot(values,  'r-.')
ax.set_xlabel('Generation')
ax.set_ylabel('Fitness')
#ax.ticklabel_format(useOffset=False)
#ax.set_yscale('log')
ax.axhline(y=0, color='k')
#plt.gca().invert_yaxis()
plt.title('Q1 of 50 Runs')
plt.show()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
for values in q3_fitness_column_values:
    plt.plot(values,  'g-.')
ax.set_xlabel('Generation')
ax.set_ylabel('Fitness')
#ax.ticklabel_format(useOffset=False)
#ax.set_yscale('log')
ax.axhline(y=0, color='k')
#plt.gca().invert_yaxis()
plt.title('Q3 of 50 Runs')
plt.show()