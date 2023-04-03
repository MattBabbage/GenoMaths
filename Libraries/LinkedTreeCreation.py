from sympy import FunctionClass, Add, Mul, cos, sin, binomial, arity, S
from Libraries.NodeValue import *

def CreateRandomTree(ops, atoms, symbols, funcs=()):
    allatoms = atoms + symbols
    e = S.Zero
    types = [Add, Mul]
    topnode = CreateRandomSingleExpression(types, allatoms, funcs)
    topnode.left = CreateRandomSingleExpression(types, allatoms, funcs)
    topnode.right = CreateRandomSingleExpression(types, allatoms, funcs)
    #     topnode.left.left = CreateRandomSingleExpression(types, allatoms, funcs)
    #     topnode.left.right = CreateRandomSingleExpression(types, allatoms, funcs)
    #     topnode.right.left = CreateRandomSingleExpression(types, allatoms, funcs)
    #     topnode.right.right = CreateRandomSingleExpression(types, allatoms, funcs)
    return topnode


def CreateRandomTrees(n, ops, atoms, symbols, funcs, types):
    Trees = []
    for _ in range(n):
        allatoms = atoms + symbols
        e = S.Zero
        topnode = CreateRandomSingleExpression(types, allatoms, funcs)
        topnode.left = CreateRandomSingleExpression(types, allatoms, funcs)
        topnode.right = CreateRandomSingleExpression(types, allatoms, funcs)
        #         topnode.left.left = CreateRandomSingleExpression(types, allatoms, funcs)
        #         topnode.left.right = CreateRandomSingleExpression(types, allatoms, funcs)
        #         topnode.right.left = CreateRandomSingleExpression(types, allatoms, funcs)
        #         topnode.right.right = CreateRandomSingleExpression(types, allatoms, funcs)
        Trees.append(topnode)
    return Trees


def CreateRandomTreesDeeper(n, ops, atoms, symbols, funcs, types):
    Trees = []
    for _ in range(n):
        allatoms = atoms + symbols
        e = S.Zero
        topnode = CreateRandomSingleExpression(types, allatoms, funcs)
        topnode.left = CreateRandomSingleExpression(types, allatoms, funcs)
        topnode.right = CreateRandomSingleExpression(types, allatoms, funcs)
        topnode.left.left = CreateRandomSingleExpression(types, allatoms, funcs)
        topnode.left.right = CreateRandomSingleExpression(types, allatoms, funcs)
        topnode.right.left = CreateRandomSingleExpression(types, allatoms, funcs)
        topnode.right.right = CreateRandomSingleExpression(types, allatoms, funcs)
        Trees.append(topnode)
    return Trees


