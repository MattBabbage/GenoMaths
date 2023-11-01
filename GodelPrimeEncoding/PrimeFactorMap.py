import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from ulam_spiral import make_spiral
from sympy import sieve, primerange, prime, primefactors, factorint, factorial
from GodelEncoding import encode_string_to_godel, decode_godel_to_string, check_fitness, get_all_fitness
from sympy.abc import x

start_value = 2

# Declare a dictionary of all variables and their corresponding primes
variables = ["x"]
numbers = ["1", "2"]
operations = ["*", "+", "-"]
all_symbols = variables + numbers + operations
print(all_symbols)
print(len(all_symbols))
all_primes = list(range(1, (len(all_symbols)+1)))
print(all_primes)
# Create dictionary of variables
symbol_number_map = {all_symbols[i]: all_primes[i] for i in range(len(all_symbols))}
number_symbol_map = dict((v,k) for k,v in symbol_number_map.items())

# Create a map of all numbers which have prime factors
root_value = 400
max_value = root_value**2
print(max_value)
prime_list = list(primerange(start_value, max_value+1))
# Mask out all primes
prime_factor_list = np.array(list(set(list(range(start_value, max_value+1))).difference(prime_list)))

# Mask out all numbers with prime factors over length of all symbols (They don't have an equation calculable)
filtered_prime_factor_list = []
for num in prime_factor_list:
    prime_factors = factorint(num)
    # Check if any prime factor is greater than 'n'
    if all(factor <= len(all_symbols) for factor in prime_factors.values()):
        filtered_prime_factor_list.append(num)
filtered_prime_factor_list = np.array(filtered_prime_factor_list)

# Generate Equations from list of prime factors
gne_equation_dict = {}
for gn in filtered_prime_factor_list:
    prime_factors = factorint(gn)
    equation = str(decode_godel_to_string(gn, number_symbol_map))
    gne_equation_dict[gn] = equation


# Import Data
df = pd.read_csv("../GodelPrimeEncoding/train.csv")

# Generate fitness for each number
gne_fitness_dict = get_all_fitness(gne_equation_dict, df, variables)

# for gne in gne_equation_dict.keys():
#     print(gne)
#     gne_fitness_dict[gne] = check_fitness(gne_equation_dict[gne], df, variables)

print(gne_equation_dict)
print(gne_fitness_dict)

back_arr = np.ones(max_value)
# back_arr[filtered_prime_factor_list-1] = 0.2
for gn in gne_fitness_dict.keys():
    back_arr[gn-1] = gne_fitness_dict[gn]


# Spiral the values clockwise out from the centre
back_arr = make_spiral(back_arr.reshape((root_value,root_value)))

plt.matshow(back_arr, cmap=cm.RdYlBu_r)

plt.axis('off')
plt.savefig('ulam_spiral.png')
plt.show()
