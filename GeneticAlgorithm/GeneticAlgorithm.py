from Population import Population
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from copy import deepcopy
import sys
import sympy

class GeneticAlgorithm:
    def __init__(self, df):
        self.children = []
        self.train_df = df
        self.population = []
        self.fittest_scores = []
        self.q1_fitness = []
        self.q2_fitness = []
        self.q3_fitness = []
        self.elites = []
        self.elites_fitness = []
        self.n_elites = 2

    def run_generations(self, n_gens, n_pop):
        print("start")
        variables = list(self.train_df.columns[0:-1])
        variables += variables
        variables += ["-1", "0", "1", "2"] # Add extra variable to the list
        operations = ["*", "+", "-"]
        # Generate Initial Population
        self.population = Population(n_pop, operations, variables)
        # Calculate Initial Fitness
        self.population.check_fitness(train_df)
        self.save_elites()
        self.log_scores()
        # Setup loop for all generations
        for n_gen in range(n_gens):
            print("Generation " + str(n_gen))
            print("Mutation")
            self.population.mutate(0.4)
            print("Selection")
            self.population.roulette_selection()   
            print("Crossover")
            self.population.crossover(1, 0.7)
            print("Fitness")
            self.population.check_fitness(train_df)
            print("Post Fitness")
            self.population.print_all()
            self.log_scores()
            # elitism
            self.replace_unfit_with_elites()
            print("Post Replacements")
            self.population.print_all()
            # self.population.print_all()
            self.save_elites()
            # self.population.print_all()
            # self.population.check_fitness(train_df)
            if self.population.fittest_score == 0:
                print("Found Solution")
                return

    def log_scores(self):
            fitness = np.array([x for x in self.population.all_fitness if x == x])
            fitness_no_outliers = np.array([y for y in fitness if not isinstance(y, sympy.core.numbers.Infinity)])
            fitness_no_outliers = np.array([z for z in fitness_no_outliers if not isinstance(z, type(sympy.core.numbers.nan))])
            # Don't log outliers that are huge i.e. 1.85267342779706e+336 as it cant be cast as float
            fitness_no_outliers = np.clip(fitness_no_outliers, 0, 1000000)
            # fitness_no_outliers = np.array([z for z in fitness_no_outliers if not z > 1000000])
            print(fitness_no_outliers)
            # Set as float to avoid RuntimeWarning: overflow encountered in cast
            # fitness_no_outliers = np.array(fitness_no_outliers, dtype=np.float64)
            # fitness_no_outliers = self.reject_outliers(fitness_no_outliers)
            print(fitness_no_outliers)
            print("Fittest Score: " + str(self.population.fittest_score) + " Equation: " + str(
                self.population.fittest_equation))
            self.fittest_scores.append(self.population.fittest_score)
            self.q1_fitness.append(np.percentile(fitness_no_outliers, 25))
            self.q2_fitness.append(np.percentile(fitness_no_outliers, 50))
            self.q3_fitness.append(np.percentile(fitness_no_outliers, 75))


    def reject_outliers(self, data, m=3):
        return data[abs(data - np.median(data)) < m  * np.std(data)]

    def plot_fitness(self):
        fig, (ax1, ax2) = plt.subplots(1,2)
        ax1.plot(self.fittest_scores, 'r-')
        ax1.plot(self.q1_fitness, 'r-.')
        ax1.plot(self.q2_fitness, 'g-.')
        #ax1.plot(self.q3_fitness, 'b-.')
        ax1.set_xlabel('Generation')
        ax1.set_ylabel('Fitness')
        ax1.ticklabel_format(useOffset=False)
        ax1.axhline(y=0, color='k')

        ax2.plot(self.fittest_scores, 'r-')
        ax2.plot(self.q1_fitness, 'r-.')
        ax2.set_xlabel('Generation')
        ax2.set_ylabel('Fitness')
        ax2.ticklabel_format(useOffset=False)
        ax2.axhline(y=0, color='k')

        #plt.gca().invert_yaxis()cv
        plt.show()

    def save_elites(self):
        self.elites.append(self.population.fittest_individual)
        self.elites_fitness.append(self.population.fittest_score)

        fitness_with_elite = self.population.all_fitness + self.elites_fitness
        pop_with_elite = self.population.individuals + self.elites

        for index in range(len(fitness_with_elite)):
            if isinstance(fitness_with_elite[index], sympy.core.numbers.Infinity) or isinstance(fitness_with_elite[index], type(sympy.core.numbers.nan)):
                print("Found nan or infinity - its not so bad :)")
                list_of_reals = []
                for num in fitness_with_elite:
                    if num.is_real:
                        list_of_reals.append(num)
                fitness_with_elite[index] = np.max(list_of_reals) * 2

        fitness_with_elite_order_index = np.argsort(fitness_with_elite)
        # zipped_lists = zip(fitness_with_elite, range(len(fitness_with_elite), pop_with_elite))
        # sorted_pairs = sorted(zipped_lists)
        # pop_with_elite_in_order = [x for _, x in sorted(zip(fitness_with_elite, pop_with_elite))]
        self.elites = []
        self.elites_fitness = []
        for idx in fitness_with_elite_order_index[:self.n_elites]:

            #Check fitness matches guy!
            if pop_with_elite[idx].check_fitness(train_df, self.population.variables) != fitness_with_elite[idx]:
                print("Something gone very wrong here")

            self.elites.append(deepcopy(pop_with_elite[idx]))
            self.elites_fitness.append(deepcopy(fitness_with_elite[idx]))
            # self.elites = pop_with_elite_in_order[:self.n_elites]
            # self.elites_fitness = sorted(fitness_with_elite)[:self.n_elites]
        print("Elites: ")
        for i in range(len(self.elites)):
           print("Score: " + str(self.elites_fitness[i]) + " - Equation: " + str(self.elites[i].equation))


    def replace_unfit_with_elites(self):
        x = np.array(self.population.all_fitness)
        for index in range(len(self.population.all_fitness)):
            if isinstance(x[index], sympy.core.numbers.Infinity) or isinstance(x[index], type(sympy.core.numbers.nan)):
                print("Found nan or infinity - its not so bad :)")
                list_of_reals = []
                for num in x:
                    if num.is_real:
                        list_of_reals.append(num)
                x[index] = np.max(list_of_reals) * 2
        inds = np.argsort(x)[::-1]

        print("Elites: ")
        for i in range(len(self.elites)):
           print("Score: " + str(self.elites_fitness[i]) + " - Equation: " + str(self.elites[i].equation))

        print("Worst: ")
        for i in range(len(self.elites)):
           print("Score: " + str(self.population.all_fitness[inds[i]]) + " - Equation: " + str(self.population.individuals[inds[i]].equation))

        for i in range(len(self.elites)):
            self.population.individuals[inds[i]] = deepcopy(self.elites[i])
            self.population.all_fitness[inds[i]] = deepcopy(self.elites_fitness[i])


with open("../Data/GenerateData2D.py") as f:
    exec(f.read())
train_df = pd.read_csv("../Data/train.csv")
GA = GeneticAlgorithm(train_df)
GA.run_generations(100, 16)
GA.plot_fitness()
print("Done!")

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