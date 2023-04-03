import numpy as np # linear algebra
from sympy import *
from sympy import FunctionClass, Add, Mul, cos, sin, binomial, arity, S
from Libraries.LinkedTree import *

# Making a fitness function for 1 tree only
def fitness(tree, symbols, df, types):
    e = S.Zero
    e = GetExpressionFromTree(tree, e, types)
    errors = []
    for n_row in range(0, df.shape[0]):
        subs_array = []
        for column in range(0, df.shape[1] - 1):
            subs_array.append([symbols[column], df.iloc[n_row, column]])
        ea = sympify(e).subs(subs_array)
        errors.append(abs(df.iloc[n_row, -1] - ea.evalf()))
    if (np.mean(errors) is nan):
        print("NAN ERROR!!!")
        print(e)
        print(errors)
        return 0.9999
    return np.mean(errors)

# # Fitness of pop
# def get_fitness(pop, df):
#     x = Symbol('x')
#     y = Symbol('y')
#     scores = []
#     for e in eqs:
#         errors = []
#         for d in df:
#             ea = sympify(e).subs([(x, d[0]), (y, d[1])])
#             errors.append(abs(d[2] - ea.evalf()))
#         scores.append(np.mean(errors))
#     return scores

# Making a fitness function for 1 tree only
def randomdata_fitness(tree, symbols, df, types, d_size):
    # print("depth = ", tree.GetMaxDepth(tree))
    df = df.sample(n=d_size);
    e = S.Zero
    e = GetExpressionFromTree(tree, e, types)
    errors = []
    for n_row in range(0, df.shape[0]):
        subs_array = []
        for column in range(0, df.shape[1] - 1):
            subs_array.append([symbols[column], df.iloc[n_row, column]])
        ea = sympify(e).subs(subs_array)
        errors.append(abs(df.iloc[n_row, -1] - ea.evalf()))
        # print(errors)
    return np.mean(errors)


def fitness2d(tree, df, types):
    x = Symbol('x')
    e = S.Zero
    try:
        e = GetExpressionFromTree(tree, e, types)
        errors = []
        for d in df:
            ea = sympify(e).subs([(x, d[0])])
            errors.append(abs(d[1] - ea.evalf()))
        return np.mean(errors)
    except:
        return 1000000