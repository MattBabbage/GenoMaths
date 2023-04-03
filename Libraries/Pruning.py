from Libraries.LinkedTree import *

def PruneTree(tree):
    if tree:
        tree.left = PruneTree(tree.left)
        tree.right = PruneTree(tree.right)
        if (tree.left == 0 and tree.right == 0):
            print(tree.left)
            print(tree.right)
            print(tree.data)
            print("This should be pruned?")
        return tree

def PruneTreeTest(tree):
    if tree:
        tree.left = PruneTreeTest(tree.left)
        tree.right = PruneTreeTest(tree.right)
        e = S.Zero
        ex = GetExpressionFromTree(tree, e, [Mul, Add, Pow, div])
        if (ex == 0):
            tree.data = 0;
            tree.left = None;
            tree.right = None;
        if (tree.left is not None and tree.right is not None):
            # print(ex)
            if (not ex.free_symbols):
                print("pruned")
                tree.data = ex;
                tree.left = None;
                tree.right = None;
    #             if isinstance(tree.left.data, float):
    #                 print("Left was float: ", ex)
    #                 if isinstance(tree.right.data, float):
    #                     print("Right was float: ", ex)
    #                     tree.data = ex;
    #                     tree.left = None;
    #                     tree.right = None;
    return tree;

def PruneTreeAndGetExpression(node, expression, types):
    if node:
        if node.data in types:
            node.left, left_expression = PruneTreeAndGetExpression(node.left, expression, types)
            node.right, right_expression = PruneTreeAndGetExpression(node.right, expression, types)
            if isinstance(left_expression, list):
                left_expression = left_expression[0]
            if isinstance(left_expression, list):
                right_expression = right_expression[0]
        #             if (expression == 0):
        #                     print(node.data)
        #                     print("pruning branch as 0")
        #                     node.data = 0
        #                     node.left = None
        # node.right = None
        else:
            expression = node.data
    if isinstance(expression, list):
        expression = expression[0]
    return node, expression