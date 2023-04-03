from numpy import random
from Libraries.LinkedTreeCreation import *
from Libraries.LinkedTree import *
import numpy as np # linear algebra
from sympy import *
from random import choice, randint
from sympy import FunctionClass, Add, Mul, cos, sin, binomial, arity, S

def args(n, atoms, funcs):
    a = funcs + atoms
    g = []
    for _ in range(n):
        ai = choice(a)
        if (ai == "floatnum"):
            g.append(np.random.rand())
        else:
            if isinstance(ai, FunctionClass):
                g.append(ai(*args(arity(ai), atoms, funcs)))
            else:
                g.append(ai)
    return g

def expr(ops, atoms, funcs=()):
    types = [Add, Mul, Pow]
    atoms = tuple(atoms)
    while 1:
        e = S.Zero
        while e.count_ops() < ops:
            c1 = choice(types)
            print("c1: ", c1)
            _ = c1(*args(randint(1, 3), atoms, funcs))
            print("_: ", _)
            c2 = choice(types)
            print("c2: ", c2)
            e = c2(e, _)
            print("e: ", e)
            if e is S.NaN:
                print("FAIL")
                break
        else:
            print("SUCCESS")
            return e

def GenerateRandomVariable(atoms, funcs):
    a = funcs + atoms
    g = []
    ai = choice(atoms + funcs)
    # print("selected op: ", ai)
    if isinstance(ai, FunctionClass):
        # print("op is function, get op to put in function")
        g.append(ai(*args(arity(ai), atoms, funcs)))
        # print(g)
    else:
        if (ai == "floatnum"):
            g.append(np.random.rand())
        else:
            g.append(ai)
        # print(g)
    return g

# def GetNEquations(num):
#     eq_array = []
#     for _ in range(0, num):
#         e = CreateRandomTree(1, (-1, 0, 1), (x, y), (cos, sin, tan))
#         e = GetExpressionFromTree(topnode, e, types)
#         print("Made EQ: {}".format(e))
#         eq_array.append(e);
#     return eq_array

def AddRandomLayer(node):
    # Get to a leaf
    if (node.left == None):
        print("Found Leaf!")
    if node is Node:
        AddRandomLayer(node.left)
        # Now, since the left subtree and the root has been printed, call inorder on right subtree recursively until we reach a leaf node.
        AddRandomLayer(node.right)

def DoesNodeContainOps(node, atoms, status, types):
    if node:
        status = DoesNodeContainOps(node.left, atoms, status, types)
        for i in range(0, len(atoms)):
            if node.data not in types:
                if atoms[i] in node.data.free_symbols:
                    status[i] = true
        status = DoesNodeContainOps(node.right, atoms, status, types)
    return status

def CreateRandomSingleExpression(types, atoms, funcs=()):
    RNode = Node(choice(types))  # + GenerateRandomVariable(atoms, funcs)
    RNode.left = Node(GenerateRandomVariable(atoms, funcs))
    RNode.right = Node(GenerateRandomVariable(atoms, funcs))
    return RNode
