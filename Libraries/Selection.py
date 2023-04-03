import numpy as np # linear algebra
from numpy import random
from copy import copy, deepcopy

def tournament_selection(pop, scores, k=3):
    individual = np.random.randint(len(pop))  # select random individual
    for opponent in np.random.randint(0, len(pop), k - 1):
        if scores[opponent] < scores[individual]:
            individual = deepcopy(opponent)  # if opponent wins, replace
    return pop[individual]


def roulette_selection(pop, scores):
    scores = np.clip(scores, None, 0.99)
    invscores = [(1 - prob) * 2 for prob in scores]
    selected = random.uniform(0, np.sum(invscores))
    val = 0;
    for i in range(0, len(pop)):
        if (val < selected and (val + invscores[i]) > selected):
            return pop[i]
        else:
            val = val + invscores[i]
    print("roulette selection went very wrong!")
    return pop[i]
