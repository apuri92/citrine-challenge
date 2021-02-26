import numpy as np
from scipy.optimize import minimize
from constraints import Constraint
from random import random

def objective(x):
    return 0.
    # return 10*random()*x[0] - 10*random()*x[1]
    # return x[0]-0.2 + 0.01
    # return 0.8-x[0] + 0.01
    # return x[1]-0.1 + 0.01
    # return x[0]-x[1] + 0.01


def constraint1(x):
    return 1.0 - x[0] - x[1] - x[2] - x[3]

def constraint2(x):
    return x[3] / (x[0] + x[1]) - 0.1

def constraint3(x):
    return 0.15 - x[3] / (x[0] + x[1])

def constraint4(x):
    return x[2] - 0.5

def constraint5(x):
    return (x[0] + x[1]) / (x[0] + x[1] + x[3]) - 0.8

# initial guesses
constrain = Constraint('formulation.txt')
n = constrain.get_ndim()
x0 = np.zeros(n)
x0 = constrain.get_example()

# show initial objective
print('Initial SSE Objective: ' + str(objective(x0)))

# optimize
b = (0.0,1.0)
bnds = (b, b, b, b)
con1 = {'type': 'ineq', 'fun': constraint1}
con2 = {'type': 'ineq', 'fun': constraint2}
con3 = {'type': 'ineq', 'fun': constraint3}
con4 = {'type': 'ineq', 'fun': constraint4}
con5 = {'type': 'ineq', 'fun': constraint5}
cons = ([con1,con2,con3,con4,con5])

solution = minimize(objective,x0,method='SLSQP',bounds=bnds,constraints=cons)
x = solution.x

print(x0)
print(list(x))
