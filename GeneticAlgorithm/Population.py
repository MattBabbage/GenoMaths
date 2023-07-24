import sympy.core.numbers

from Node import Node
from Tree import Tree
from TreeGenerator import TreeGenerator
import random
from sympy.parsing.sympy_parser import parse_expr
from graphviz import Source
from sympy import dotprint
import numpy as np
from copy import deepcopy
import math
from time import time

class Population:
    def __init__(self, n_pop, operations, variables):
        self.operations = operations
        self.variables = variables
        self.n_pop = n_pop
        self.individual_generator = TreeGenerator(self.operations, self.variables)
        # List of individuals
        self.individuals = self.individual_generator.gen_trees(2, 2, n_pop)
        self.all_fitness = []
        # Statistics about population
        self.fittest_score = None
        self.fittest_equation = None
        self.fittest_individual = None

    def check_fitness(self, df):
        try:
            self.all_fitness = []
            for individual in self.individuals:
                individual_fit = individual.check_fitness(df, self.variables)
                if individual_fit != individual_fit:
                    print("Nan Nan")
                # if isinstance(individual_fit, sympy.core.numbers.nan):
                #     print("Nan Nan 1")

                self.all_fitness.append(individual_fit)

                if individual_fit is not sympy.core.numbers.nan:
                    if individual_fit == individual_fit: # Filters out NaN fitness
                        if self.fittest_score is None:
                            self.fittest_individual = []
                            self.fittest_score = deepcopy(individual_fit)
                            self.fittest_equation = deepcopy(individual.equation)
                            self.fittest_individual = deepcopy(individual)
                            print("first fittest score: " + str(self.fittest_score) + " Equation: " + str(self.fittest_equation))

                        if individual_fit < self.fittest_score:
                            self.fittest_individual = []
                            self.fittest_score = deepcopy(individual_fit)
                            self.fittest_equation = deepcopy(individual.equation)
                            self.fittest_individual = deepcopy(individual)
                            print("New fittest score! " + str(self.fittest_score) + " Equation: " + str(self.fittest_equation))
            #self.print_all()
        except:
            print("exception occured")

    def mutate(self, r_mut):
        for i in self.individuals:
            i.mutate(self.operations, self.variables, r_mut)

    def roulette_selection(self):
        new_individuals = []
        x = np.array(self.all_fitness)
        for index in range(len(self.all_fitness)):
            if isinstance(x[index], sympy.core.numbers.Infinity) or isinstance(x[index], type(sympy.core.numbers.nan)):
                print("Found nan or infinity - its not so bad :)")
                list_of_reals = []
                for num in x:
                    if num.is_real:
                        list_of_reals.append(num)
                x[index] = np.max(list_of_reals)



        # x = list(map(lambda idx: idx.replace(sympy.core.numbers.Infinity, (np.max(x))), x))
        norm_fitness = (x-np.min(x))/(np.max(x)-np.min(x))
        inv_norm_fit = [(1 - fit) for fit in norm_fitness]

        # if they are all the same fitness, set inv norm fitness to all be the same
        if all(a==inv_norm_fit[0] for a in inv_norm_fit):
            inv_norm_fit = np.full(len(inv_norm_fit), 1)

        # cumulative_fitness = sum(self.all_fitness)
        # scores = [x / cumulative_fitness for x in self.all_fitness] # np.clip(self.all_fitness, None, 0.99)
        # a = np.sum(scores)
        # invscores = [(1 - prob) for prob in scores]
        for n_indiv in range(len(self.individuals)):
            selected = random.uniform(0, np.sum(inv_norm_fit))
            val = 0
            for i in range(len(self.individuals)):
                try:
                    if (val < selected and (val + inv_norm_fit[i]) > selected):
                        new_individuals.append(deepcopy(self.individuals[i]))
                        break
                    else:
                        val = val + inv_norm_fit[i]
                except:
                    print("An exception occurred")
        self.individuals = new_individuals

    def crossover(self, k_points, r_cross):
        try:
            child_individuals = []
            random.shuffle(self.individuals)  # Mix them up (just incase selection did not)
            i_p_half_pop = math.floor(self.n_pop / 2) # get idx at half pop (incrementing will allow pairing)
            for idx in range(math.floor(self.n_pop / 2)):
                child_individuals.extend(self.individuals[idx].crossover(self.individuals[i_p_half_pop], k_points, r_cross))
                i_p_half_pop = i_p_half_pop + 1
            self.individuals = child_individuals
        except:
            print("What happened?")

    def print_all(self):
        for i in range(len(self.individuals)):
            print(str(i) + " score: " + str(self.all_fitness[i]) + " equation: " + str(self.individuals[i].equation))

population = Population(5, ["*", "+", "-"], ["a", "b", "c", "pi"])


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