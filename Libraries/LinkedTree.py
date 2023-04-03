from sympy import *
from sympy import FunctionClass, Add, Mul, cos, sin, binomial, arity, S

class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    # Inorder traversal
    def inorderTraversal(self, root):
        res = []
        if root:
            res = self.inorderTraversal(root.left)
            res.append(root.data)
            # print(root.data)
            res = res + self.inorderTraversal(root.right)
        return res

    def GetMaxDepth(self, root, d=0):
        if d > 100:
            print("somethings gone horribly wrong")
            return d
        if root:
            d = d + 1
            ld = self.GetMaxDepth(root.left, d)
            rd = self.GetMaxDepth(root.right, d)
            d = max(ld, rd)
        return d


def inorder(node, denote, wholestring):
    if node:
        # Recursively call inorder on the left subtree until it reaches a leaf node
        wholestring = inorder(node.left, "left", wholestring)

        # Once we reach a leaf, we print the data
        if (denote == "left" and node.left == None):
            print("(")
            wholestring = wholestring + "("

        print(node.data)
        wholestring = wholestring + str(node.data)
        if (denote == "right" and node.right == None and not isinstance(node.left, int)):
            print(")")
            wholestring = wholestring + ")"
        # Now, since the left subtree and the root has been printed, call inorder on right subtree recursively until we reach a leaf node.
        wholestring = inorder(node.right, "right", wholestring)
    return wholestring


def PrintTree(root):
    Operations = [Add, Mul, Pow, div]
    OperationsPrint = ["+", "*", "**", "/"]
    nlevels = root.GetMaxDepth(root)
    width = pow(2, nlevels + 1)

    q = [(root, 0, width, 'c')]
    levels = []

    while (q):
        node, level, x, align = q.pop(0)
        if node:
            if len(levels) <= level:
                levels.append([])

            levels[level].append([node, level, x, align])
            seg = width // (pow(2, level + 1))
            q.append((node.left, level + 1, x - seg, 'l'))
            q.append((node.right, level + 1, x + seg, 'r'))

    for i, l in enumerate(levels):
        pre = 0
        preline = 0
        linestr = ''
        pstr = ''
        seg = width // (pow(2, i + 1))
        for n in l:
            valstr = str(n[0].data)
            if (n[0].data in Operations):
                valstr = OperationsPrint[Operations.index(n[0].data)]
            if n[3] == 'r':
                linestr += ' ' * (n[2] - preline - 1 - seg - seg // 2) + '¯' * (seg + seg // 2) + '\\'
                preline = n[2]
            if n[3] == 'l':
                linestr += ' ' * (n[2] - preline - 1) + '/' + '¯' * (seg + seg // 2)
                preline = n[2] + seg + seg // 2
            pstr += ' ' * (n[2] - pre - len(valstr)) + valstr  # correct the potition acording to the number size
            pre = n[2]
        print(linestr)
        print(pstr)

def GetTreeNDeepInOrder(root, n, i = -1):
    if root:
        i = i + 1
        if i is n:
            #print("Reached Node ", n)
            return True, root, i
        found, tree, i = GetTreeNDeepInOrder(root.left, n, i)
        if found:
            return True, tree, i
        found, tree, i = GetTreeNDeepInOrder(root.right, n, i)
        if found:
            return True, tree, i
        return False, root, i
    return False, root, i

def ReplaceTreeNDeepInOrder(root, newtree, n, i = -1):
    if root:
        i = i + 1
        if i == n:
            #print("Reached Node ", n)
            root = newtree
            return True, root, i
        found, root.left, i = ReplaceTreeNDeepInOrder(root.left, newtree, n, i)
        if found:
            return True, root, i
        found, root.right, i = ReplaceTreeNDeepInOrder(root.right, newtree, n, i)
        if found:
            return True, root, i
        return False, root, i
    return False, root, i

def CountRoots(root, n):
    if root:
        # print(root.data)
        # print(n)
        n = CountRoots(root.left, n)
        n = n + 1
        n = CountRoots(root.right, n)
    return n

def CountRoots2(root):
    return len(root.inorderTraversal(root))

def GetExpressionFromTree(node, expression, types):
    if node:
        if node.data in types:
            left_expression = GetExpressionFromTree(node.left, expression, types)
            right_expression = GetExpressionFromTree(node.right, expression, types)
            if isinstance(left_expression, list):
                left_expression = left_expression[0]
            if isinstance(left_expression, list):
                right_expression = right_expression[0]
            expression = node.data(left_expression, right_expression)
            # if (expression == 0):
            # PrintTree(node)
            # print("Expression was 0, should be pruned")
        else:
            expression = node.data
    if isinstance(expression, list):
        expression = expression[0]
    return expression