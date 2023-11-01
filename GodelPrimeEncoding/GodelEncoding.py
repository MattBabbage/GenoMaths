import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from ulam_spiral import make_spiral
from sympy import sieve, primerange, prime, primefactors, factorint, Symbol, nan
from sympy import dotprint, sympify, simplify, expand
from sympy.parsing.sympy_parser import parse_expr
# variables = ["x"]
# variables += ["1", "2"]  # Add extra variable to the list
# operations = ["*", "+", "-"]
# all_symbols = variables + operations
# print(all_symbols)
# print(len(all_symbols))
# all_primes = list(range(1, (len(all_symbols)+1)))
# print(all_primes)
# # Create dictionary of variables
# symbol_number_map = {all_symbols[i]: all_primes[i] for i in range(len(all_symbols))}
# number_symbol_map = dict((v,k) for k,v in symbol_number_map.items())
#
# print(symbol_number_map)
# print(number_symbol_map)

# return a fitness between 0 and 1
def get_all_fitness(gn_equation_dict, df, variables):


    gn_fitness = {}
    for gn in gn_equation_dict.keys():
        gn_fitness[gn] = check_fitness(gn_equation_dict[gn], df, variables)

    # Take mean of all values which are not nan
    values_no_nan = [x for x in gn_fitness.values() if not x == nan]
    median_value = np.median(values_no_nan)
    print("median: " + str(median_value))
    # replace all above mean with nan, too big
    for gn in gn_fitness.keys():
        if gn_fitness[gn] is not nan:
            if gn_fitness[gn] > median_value:
                gn_fitness[gn] = nan

    print("prenorm: " + str(gn_fitness))
    gn_fitness = normalize(gn_fitness)
    print("postnorm: " + str(gn_fitness))

    for key in gn_fitness.keys():
        if gn_fitness[key] == 1:
            gn_fitness[key] = nan

    return gn_fitness

def normalize(d, target=1.0):
    nonan =  [x for x in d.values() if not x == nan]
    factor = target/max(nonan)
    return {key:value*factor for key,value in d.items()}

def check_fitness(equation, df, variables):
    try:
        x = Symbol('x')
        eq = sympify(parse_expr(equation))
        e = simplify(eq)
        # print(self.node.get_count())
        # print(e)
        errors = []

        for n_row in range(0, df.shape[0]):
            subs_array = []
            for column in range(0, df.shape[1] - 1):
                subs_array.append([variables[column], df.iloc[n_row, column]])

            ea = sympify(e).subs(subs_array)
            realans = df.iloc[n_row, -1]
            errors.append(abs(realans - ea.evalf()))

        return np.mean(errors)
    except:
        return nan


def encode_string_to_godel(string, symbol_number_map):
    godel_number = 1
    primelist = list(primerange(0, prime(len(string) + 1)))
    prime_count = 0
    for symbol in string:
        print(str(primelist[prime_count])+"^"+ str(symbol_number_map[symbol]))
        godel_number *= pow(primelist[prime_count], symbol_number_map[symbol])
        prime_count += 1
    return godel_number
def decode_godel_to_string(gn, number_symbol_map):
    prime_factors = factorint(gn)
    real_eq = ""
    for key in prime_factors:
        symbol = str(number_symbol_map[prime_factors[key]])
        if symbol in ["*", "+", "-"]:
            real_eq += str(number_symbol_map[prime_factors[key]])
        else:
            real_eq += "(" + str(number_symbol_map[prime_factors[key]]) + ")"
    real_eq = real_eq.replace(")(", ")*(")
    return real_eq

# equations = ["x", "x+2", "2+x"]
#
# customprimearray = []
#
# for equation in equations:
#     print("Equation: " + equation)
#     gn = encode_string_to_godel(equation, symbol_number_map)
#     customprimearray.append(gn)
#     print("Gn: " + str(gn))
#     equationcheck = decode_godel_to_string(gn, number_symbol_map)
#     print("Equation2: " + equationcheck)
#
# customprimes = np.array([customprimearray])
#
# # back2eq = decode_godel_to_string(gn, symbol_prime_map)
#
# # print(back2eq)
# # # Generate Initial Population
# # self.population = Population(n_pop, operations, variables)
#
# # edge size of the square array.
# w = 400
# # Prime numbers up to and including w**2.
# primes = np.array([n for n in range(2,w**2+1) if all(
#                         (n % m) != 0 for m in range(2,int(np.sqrt(n))+1))])
#
# # for i in range(0, 400):
# #     print(decode_godel_to_string(i, number_symbol_map))
# # Create an array of boolean values: 1 for prime, 0 for composite
# back_arr = np.zeros(w**2)
# back_arr[primes-1] = 0.2
#
# back_arr[customprimes-1] = 1
# # Spiral the values clockwise out from the centre
# back_arr = make_spiral(back_arr.reshape((w,w)))
#
# plt.matshow(back_arr, cmap=cm.magma)
#
#
# plt.axis('off')
# plt.savefig('ulam_spiral.png')
# plt.show()