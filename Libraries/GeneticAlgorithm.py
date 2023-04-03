import numpy as np
from sympy import *
from sympy import FunctionClass, Add, Mul, cos, sin, binomial, arity, S
from copy import copy, deepcopy
import time
from Libraries.LinkedTreeCreation import *
from Libraries.Selection import *
from Libraries.Fitness import *
from Libraries.Mutation import *
from Libraries.NodeValue import *
from Libraries.Pruning import *
from Libraries.Crossover import *

#function for timing things
def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  print("Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec))

def genetic_algorithm(symbols, fitnessfunc, n_iter, n_pop, r_cross, r_mut, df):
    #Local Vars
    types = [Mul, Add]
    atoms = [-2, -1, 0, 1, 2]  #"floatnum"
    #symbols = [x,x,x, pi]
    funcs = []
    #Tracking Lists
    best_array = []
    best_fitness = list()
    q1_fitness = list()
    average_fitness = list()
    q3_fitness = list()
    n_duplicates = list()
    timings = list()
    #Count Platau
    n_stagnent_gens = 0;
    # initial population of random bitstring
    pop = CreateRandomTreesDeeper(n_pop, 1, atoms, symbols, funcs, types)
    print("Created %i individuals", n_pop)
    #Get best in pop
    best_eval = fitnessfunc(pop[0],symbols, df, types)
    #iterate through generations
    for gen in range(n_iter):
        start_time = time.time()
        print("Generation ", gen)
        scores = []
        BestScoreLastGen = best_eval;
        #Determine Fitness Score
        print("Getting Fitness")
        for i in range(0, len(pop)):
            score = fitnessfunc(pop[i], symbols, df, types)
            scores.append(score)
        #pop, scores = [fitnessfunc(c, symbols, df, types, 20) for  c in pop]
        print("Scores: ", scores)
        #Find Fittest
        for i in range(n_pop):
#             if (gen % 20 == 0 and gen != 0):
#                 print("denom of 20, pruning trees")
#                 pop[i] = PruneTreeTest(pop[i])
            if scores[i] < best_eval:
                print("new best!")
                best, best_eval = pop[i], scores[i]
                print("Gen %i, new best = %.8f" % (gen, scores[i]))
                #origonal = (result[feature_name] * (maxans_value - minans_value)) + minans_value
                #print(((scores[i] * (maxans_value - minans_value)) + minans_value))
                f = S.Zero
                f = GetExpressionFromTree(best, f, types)
                print(f)
                best_array.append(deepcopy(best))
        #Has Platau Reached 2
        if (best_eval == BestScoreLastGen):
            n_stagnent_gens = n_stagnent_gens + 1
            print("No Improvement Counter: ", n_stagnent_gens)
        else:
            n_stagnent_gens = 0
        if (n_stagnent_gens > 150):
            return best, best_eval, best_fitness, average_fitness, q1_fitness, q3_fitness, best_array, timings;
        #Log Best and Average
        best_fitness.append(best_eval)
        q1_fitness.append(np.percentile(scores, 25))  # Q1
        average_fitness.append(np.percentile(scores, 50))  # median
        q3_fitness.append(np.percentile(scores, 75))  # Q3
        #Selection
        selected = [roulette_selection(pop, scores) for _ in range(n_pop)]
        #Randomness / Fresh Genes
        selected[-1] = CreateRandomTreesDeeper(n_pop, 1, atoms, symbols, funcs, types)[0]
        #Create Children
        children = list()
        for i in range(0, n_pop, 2):
            #two by two
            p1, p2 = selected[i], selected[i+1]
            #Crossover
            #print("Crossover")
            for c in Crossover(p1,p2,r_cross):
                #mutation
                #print("Mutation")
                mutate_tree(c, r_mut, atoms, symbols, funcs)
                if (gen % 5 == 0 and gen != 0):
                    PruneTreeTest(c)
                children.append(c)
                #PrintTree(c)
#                 e = S.Zero
#                 e = GetExpressionFromTree(c, e, types)
#                 print(e)
        pop = children
        #Elitism
        pop[0] = deepcopy(best)
        end_time = time.time()
        time_convert(end_time - start_time)
        timings.append(end_time - start_time)
        if best_eval == 0:
            return best, best_eval, best_fitness, average_fitness, q1_fitness, q3_fitness, best_array, timings;
    print("END")
    return best, best_eval, best_fitness, average_fitness, q1_fitness, q3_fitness, best_array, timings;

