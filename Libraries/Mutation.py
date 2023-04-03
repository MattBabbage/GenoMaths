import numpy as np
from sympy import *
from random import choice, randint
from sympy import FunctionClass, Add, Mul, cos, sin, binomial, arity, S
from numpy import random
from Libraries.NodeValue import *

def mutate_tree(root, r_mut, atoms, symbols, funcs=()):
    if root:
        root.left = mutate_tree(root.left, r_mut, atoms, symbols, funcs)
        if np.random.rand() < r_mut:
            # mutate
            if np.random.rand() < 0.75:
                # some of the time mutate a single variable
                root = mutate_node(root, atoms, symbols, funcs)
            else:
                # The rest we want to move the useful genes and add more
                root = move_node(root, atoms, symbols, funcs)
            # print("mutate returned")
        root.right = mutate_tree(root.right, r_mut, atoms, symbols, funcs)
    return root


def mutate_node(root, atoms, symbols, funcs=()):
    # if leaf
    # print("mutating data: ", root.data)
    allatoms = atoms + symbols
    if (root.data not in [Mul, Add, Pow, Mod]):
        #         if isinstance(root.data, float):
        #             if np.random.rand() < 0.5:
        #                 #some of the time mutate a single variable
        #                 root.data = root.data + random.normal(0.0, 0.1)
        #             else:
        root.data = GenerateRandomVariable(atoms, funcs)[0]
        # print("mutated data: ", root.data)
    if (root.data in [Mul, Add, Pow, Mod]):
        root.data = choice([Mul, Add])
        # print("mutated data: ", root.data)
    return root

#New mutation
def move_node(root, atoms, symbols, funcs=()):
    # if leaf
    # print("mutating data: ", root.data)
    allatoms = atoms + symbols
    newnode = CreateRandomSingleExpression([Mul, Add], allatoms, funcs)
    if np.random.rand() < 0.5:
        newnode.left = root
        newnode.right = Node(GenerateRandomVariable(allatoms, funcs))
    else:
        newnode.left = Node(GenerateRandomVariable(allatoms, funcs))
        newnode.right = root
    return newnode