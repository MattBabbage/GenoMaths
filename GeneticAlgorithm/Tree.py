from sympy.parsing.sympy_parser import parse_expr
from graphviz import Source
from sympy import dotprint, sympify, simplify, expand
from numpy import nan
import numpy as np
import random
from copy import deepcopy
import sys
from time import time

class Tree:
    def __init__(self, node=None, equation=None, graph=None):
        self.node = node
        self.equation = equation  # parse_expr(self.node.get_equation_as_string())
        self.graph = graph  # Source(dotprint(self.equation))
        self.n_nodes = None

    def refresh_equation_from_node(self):
        self.equation = expand(simplify(parse_expr(self.node.get_equation_as_string())))

    def refresh_tree_from_equation(self, eq):
        if eq:
            self.equation = eq
        self.node.refresh_node_from_equation(self.equation)
        self.refresh_graph_from_equation()

    def refresh_graph_from_equation(self):
        self.graph = Source(dotprint(self.equation))

    def check_fitness(self, df, variables):
        e = self.equation
        # print(self.node.get_count())
        # print(e)
        errors = []
        for n_row in range(0, df.shape[0]):
            subs_array = []
            for column in range(0, df.shape[1] - 1):
                subs_array.append([variables[column], df.iloc[n_row, column]])
            st = time()
            try:
                # print(str(e))
                ea = sympify(e).subs(subs_array)
                realans = df.iloc[n_row, -1]
                errors.append(abs(realans - ea.evalf()))
                # print(time() - st)
            except:
                print(time() - st)
                print("Something went wrong with the fitness check for eq: " + str(self.equation))
                errors.append(sys.float_info.max)
                print("Set error to max float value")
        if np.mean(errors) is nan:
            print("NAN ERROR!!!")
            return 0.9999
        return np.mean(errors)

    def mutate(self, operations, variables, r_mut):

        if self.node.mutate(operations, variables, r_mut):
            self.refresh_equation_from_node()
            # self.graph.render('output_premutation.gv', view=True)
            self.refresh_graph_from_equation()
            # self.graph.render('output_postmutation.gv', view=True)
            # print("Mutated!")

    def crossover(self, mate, k_points, r_cross):
        for i in range(k_points):
            if random.random() < r_cross:
                # print(self.equation)
                # print(mate.equation)
                self.refresh_tree_from_equation(self.equation)
                mate.refresh_tree_from_equation(mate.equation)
                # self.graph.render('self_pre_cross.gv', view=True)
                # mate.graph.render('mate_pre_cross.gv', view=True)

                self_count = self.node.get_count()
                if self_count == 0:
                    self_selected = 0
                else:
                    self_selected = random.randrange(self.node.get_count())

                mate_count = mate.node.get_count()
                if mate_count == 0:
                    mate_selected = 0
                else:
                    mate_selected = random.randrange(mate.node.get_count())

                self_node, ph = deepcopy(self.node.get_node(self_selected))
                mate_node, ph = deepcopy(mate.node.get_node(mate_selected))
                # Source(dotprint(parse_expr(self_node.get_equation_as_string()))).render('self_selected_node.gv', view=True)
                # Source(dotprint(parse_expr(mate_node.get_equation_as_string()))).render('mate_selected_node.gv', view=True)
                ph = self.node.replace_node(self_selected, mate_node)
                ph = mate.node.replace_node(mate_selected, self_node)
                self.refresh_equation_from_node()
                self.refresh_graph_from_equation()
                mate.refresh_equation_from_node()
                mate.refresh_graph_from_equation()
                # self.graph.render('self_post_cross.gv', view=True)
                # mate.graph.render('mate_post_cross.gv', view=True)
        return [self, mate]