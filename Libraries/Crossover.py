import numpy as np # linear algebra
from numpy import random
from copy import copy, deepcopy
from Libraries.LinkedTree import *

def Crossover(p1, p2, r_cross):
    c1, c2 = deepcopy(p1), deepcopy(p2)
    if np.random.rand() < r_cross:
        a = CountRoots2(c1)
        an = random.randint(0,a)
        b = CountRoots2(c2)
        bn = random.randint(0,b)
        #PrintTree(c1)
        #PrintTree(c2)
        found, c1_tree, i = GetTreeNDeepInOrder(c1, an)
        found, c2_tree, i = GetTreeNDeepInOrder(c2, bn)
        c1_tree, c2_tree = deepcopy(c1_tree), deepcopy(c2_tree)
        found, c1, i  = ReplaceTreeNDeepInOrder(c1, c2_tree, an)
        #PrintTree(c1)
        found, c2, i  = ReplaceTreeNDeepInOrder(c2, c1_tree, bn)
        #PrintTree(c2)
    return [c1,c2]
