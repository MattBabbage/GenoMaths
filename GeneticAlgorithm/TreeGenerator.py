from Node import Node
from Tree import Tree
import random
from sympy.parsing.sympy_parser import parse_expr
from graphviz import Source
from sympy import dotprint


class TreeGenerator:
    def __init__(self, operations, variables):
        self.operations = operations
        self.variables = variables

    def gen_tree(self, depth=1, width=2, init_depth=0):
        new_node = Node(random.choice(self.operations))
        new_node.add_children(self.operations, self.variables, width, depth)
        new_equation = parse_expr(new_node.get_equation_as_string())
        return Tree(new_node, new_equation, Source(dotprint(new_equation)))

    def gen_trees(self, depth=1, width=2, n_trees=1, init_depth=0):
        trees = []
        for i in range(n_trees):
            new_node = Node(random.choice(self.operations))
            new_node.add_children(self.operations, self.variables, width, depth)
            new_equation = parse_expr(new_node.get_equation_as_string())
            trees.append(Tree(new_node, new_equation, Source(dotprint(new_equation))))
        return trees

    def gen_tree_from_equation(self, eq):
        created_tree = Tree(Node(None), eq, Source(dotprint(eq)))
        created_tree.node.refresh_node_from_equation(eq)
        return created_tree


# function_string_map = {
#   sympy.core.mul.Mul: "*",
#   sympy.core.add.Add: "+"
# }
#
# def pre(expr):
#     if not expr.args:
#         print(expr)
#     else:
#         if expr.func in function_string_map.keys():
#             print(function_string_map.get(expr.func))
#         # print(repr(expr.func))
#     for arg in expr.args:
#         pre(arg)

# generator = TreeGenerator(["*", "+", "-"], ["a", "b", "c", "pi"])
# new_tree = generator.gen_tree(2, 2)
# print(new_tree.node.subtrees())
# print(new_tree.node.get_equation_as_string())
# print(new_tree.equation)
# print(sympify(new_tree.equation))
# pre(new_tree.equation)
# new_tree.graph.render('output.gv', view=True)
#
#
# new_tree_2 = generator.gen_tree(2, 2)
# print(new_tree_2.node.subtrees())
# print(new_tree_2.node.get_equation_as_string())
# print(new_tree_2.equation)
# print(sympify(new_tree_2.equation))
# pre(new_tree_2.equation)
# new_tree_2.graph.render('output2.gv', view=True)
#
#
# new_tree_2.node.refresh_node_from_equation(new_tree.equation)
# new_tree_2.refresh_equation_from_node()
# new_tree_2.refresh_graph_from_equation()
# print(new_tree_2.equation)
# new_tree_2.graph.render('output3.gv', view=True)
#
# new_tree_3 = generator.gen_tree_from_equation(new_tree_2.equation)
# print(new_tree_3.equation)
# new_tree_3.graph.render('output4.gv', view=True)