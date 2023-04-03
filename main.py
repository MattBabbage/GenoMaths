import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from graphviz import Source
from Libraries.GeneticAlgorithm import *
from Libraries.Fitness import *
from Libraries.LinkedTree import *

L = 1
x0 = 0.5
k = 10
x = symbols('x')
logistic_expr = L / (1 + exp(-k*(x-x0)))
# Convert symbolic expression of sigmoid function to lambda function
f_logistic = lambdify(x, logistic_expr, 'numpy')
# Plot graph of sigmoid function
lower_xlim = 0
upper_xlim = 1
step = 0.1
xvec = np.arange(lower_xlim,upper_xlim, step)
yvec = f_logistic(xvec)

# plt.figure()
# plt.plot(xvec,yvec)
# plt.title('Logistic function')
# plt.show()

#f_logistic(0.9)



#read data
train_df = pd.read_csv("HousePricesExample/data/train.csv")
test_df = pd.read_csv("HousePricesExample/data/test.csv")

train_df.shape, test_df.shape

print(train_df.head(3))

print(test_df.head(3))

train_df.info()

#Need to Normalise this data to be integers where possible, delete others
del_col = []
for column in train_df.columns:
    if (train_df[column].dtype == np.float64 or train_df[column].dtype == np.int64):
        pass
    else:
        del_col.append(column)
    if train_df[column].isnull().all():
        del_col.append(column)

print(del_col)

clean_train_df = train_df.drop(del_col,axis=1)
clean_train_df.info()

#clean_train_df = clean_train_df.drop(['LotFrontage','MasVnrArea','GarageYrBlt','Id'],axis=1)

cols = ['OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF', 'FullBath', 'YearBuilt', 'SalePrice']
clean_train_df = clean_train_df[cols]

clean_train_df.info()

print(list(clean_train_df))

clean_train_df.head()
#cleaned dataset:
clean_train_df.shape

def normalize(df):
    result = df.copy()
    for feature_name in df.columns:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result

normalized_df=normalize(clean_train_df)
normalized_df.head()

normalized_df.iloc[:,-1:]
maxans_value = clean_train_df.iloc[:,-1:].max()
minans_value = clean_train_df.iloc[:,-1:].min()
print(normalized_df.iloc[1,-1:])
print((normalized_df.iloc[1,-1:] * (maxans_value - minans_value)) + minans_value)

i = 0
for _ in clean_train_df.columns:
    i += 1

n = len(clean_train_df.columns) - 1
# symbol_list = list(symbols('var_0:{}'.format(n)))

symbol_list = [symbols(v) for v in list(clean_train_df)[0:(len(clean_train_df.columns) - 1)]]
# print(symbols('var_0:{}'.format(n)))

# var_as_symbol_objects = [symbols(v) for v  in list(clean_train_df)[0:(len(clean_train_df.columns) - 1)]]
# print(var_as_symbol_objects)

print(clean_train_df.shape[1])
#print(clean_train_df[0,])
# for n_row in range(0, clean_train_df.shape[1]):
#     print(n_row)


x = symbols('x')

df = []
minval = -1000
maxval = 1000
# for num in range(2,50):
#     if all(num%i!=0 for i in range(2,num)):
#        df.append([n, num])

# a = (-15*x**2 + x**3 + 20)
# df = []

# mu, sigma = 0, 0.1 # mean and standard deviation
# s = np.random.normal(mu, sigma, 1000)

# for i in range(0,30):
#     #noise
#     s = np.random.normal(mu, sigma, 1000)
#     #valuue
#     sub1 = randint(minval,maxval)
#     b = sympify(a).subs([(x, sub1)])
#     ans = b.evalf()
#     df.append([sub1, ans])

print(df)

fittest, score, best_array, average_array, q1_array, q3_array, fittest_array, timings  = genetic_algorithm(symbol_list, fitness, 60, 10, 0.8, 0.2, normalized_df.sample(n = 50))


types = [Mul, Add, Pow]
for i in range(0, len(fittest_array)):
    print(i)
    e = S.Zero
    e = GetExpressionFromTree(fittest_array[i], e, types)
    print(e)

print("normalised score: ", score)
realvalscore = ((score * (maxans_value - minans_value)) + minans_value)
print("score: ", realvalscore)

atoms = [-1,0,0.1,0.2,0.3,0.4,0.5,0.6]
#symbols = [x,x,x, pi]
funcs = [cos, sin, tan]
v_score = fitness(fittest, symbol_list, normalized_df.sample(n = 300), types)
print("Validation score: ", v_score)
print("score: ", ((v_score * (maxans_value - minans_value)) + minans_value))

# print("max price: ", maxans_value)
# print("min price: ", minans_value)
# print("price range is: ", maxans_value - minans_value)
# print(realvalscore - minans_value / (maxans_value - minans_value))
# print()

src = Source(dotprint(e))

a = simplify(e)
src1 = Source(dotprint(a))

print(src1)

print(e)
print(a)

e = S.Zero
e = GetExpressionFromTree(fittest, e, types)
print("Best equation found: ", e)
print("With Fitness: ", score)
# print(PrintTree(fittest))
# test = PruneTreeTest(fittest)
# PrintTree(test)

