import random
import sympy
import numpy as np

function_string_map = {
  sympy.core.mul.Mul: "*",
  sympy.core.add.Add: "+",
  sympy.core.power.Pow: "**"
}


class Node:
    def __init__(self, data):
        self.children = []
        self.data = data

    def subtrees(self):
        if not self.children:
            return self.data
        result = (self.data, [child.subtrees() for child in self.children])
        return result

    def get_equation_as_string(self):
        if self.data is None:
            print("Issue here")
        if not self.children:
            return self.data
        result = "(" + self.data.join([child.get_equation_as_string() for child in self.children]) + ")"
        return result

    def add_children(self, operations, variables, width = 2, depth = 1, cur_depth = 1):
        if depth == 0:
            return
        # if data not operation
        if self.data not in operations:
            self.data = random.choice(operations)
        # if no children
        if len(self.children) == 0:
            child_data = random.choices(variables, k=width)
            for datum in child_data:
                self.children.append(Node(datum))
        if depth > cur_depth:
            # increment current depth
            cur_depth = cur_depth + 1
            for child in self.children:
                child.add_children(operations,variables,width,depth,cur_depth)

    def wipe_node(self):
        self.children = []
        self.data = None

    def refresh_node_from_equation(self, expr=None):
        self.wipe_node()
        self.update_from_equation(expr)

    def update_from_equation(self, expr):
        # if data not operation
        if self.data is None:
            self.data = function_string_map.get(expr.func)

        if not expr.args:
            self.data = str(expr)
            # print(expr)
        else:
            if expr.func in function_string_map.keys():
                self.data = function_string_map.get(expr.func)
                # print(function_string_map.get(expr.func))
            # print(repr(expr.func))
        for arg in expr.args:
            new_child = Node(None)
            new_child.update_from_equation(arg)
            self.children.append(new_child)

    def mutate(self, operations, variables, r_mut):
        chance_op = 0.7
        mutated = np.random.rand() < r_mut
        if mutated:
            if np.random.rand() < chance_op:
                self.data = random.choice(operations)
            else:
                self.data = random.choice(variables)
            if self.data not in operations:
                self.children = []
            if self.data not in variables and self.children == []:
                self.add_children(operations, variables, 2, 1)
        if self.children:
            for child in self.children:
                child_mutated = child.mutate(operations, variables, r_mut)
                if child_mutated:
                    mutated = True
        return mutated

    def get_count(self):
        n_children = 0
        if self.children:
            for child in self.children:
                n_children = n_children + child.get_count()
            n_children = n_children + len(self.children)
        return n_children

    def get_node(self, index, current_index=0):
        if current_index is index:
            return self, current_index
        current_index = current_index + 1
        for child in self.children:
            found_node, current_index = child.get_node(index, current_index)
            if found_node is not None:
                return found_node, current_index
        return None, current_index

    def replace_node(self, index, surrogate, current_index=0):
        if index is current_index:
            self.data = surrogate.data
            self.children = surrogate.children
            return current_index
        current_index = current_index + 1
        for child in self.children:
            current_index = child.replace_node(index, surrogate, current_index)
            if index is current_index:
                return current_index
        return current_index
# class NodeGenerator:
#     def __init__(self, operations, variables):
#         self.operations = operations
#         self.variables = variables
#
#     def generate(self, depth=1, width=2, init_depth=0):
#         new_node = Node(random.sample(self.operations, 1)[0])
#         new_node.add_children(self.operations, self.variables, width, depth)
#         return new_node


# a = Node("x")
# b = Node("+")
# c = Node("a")
# d = Node("b")
# e = Node("-")
# f = Node("c")
# g = Node("d")
# h = Node("e")
# b.children = [c, d, h]
# e.children = [f, g]
# a.children = [b, e]
#
# print(a.subtrees())
# print(a.equation())
#
# Generator = NodeGenerator(["x", "+", "-"], ["a", "b", "c"])
# GeneratedNode = Generator.generate(3, 2)
# print(GeneratedNode.subtrees())
# print(GeneratedNode.equation())
#To Do
# 1. Tree Generation
# 2. Tree -> Equation
# 3. Equation -> Tree
# 3. Depth Control?