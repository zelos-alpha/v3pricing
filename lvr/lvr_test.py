


# max exit time.
from math import sqrt
from numpy import log

import numpy as np
from scipy.optimize import minimize


def liq_lambda(h,l):
    return 1/(2-sqrt(l)-1/sqrt(h))


def exit_time(h,l,sigma):
    a = log(l) / sigma
    b = log(h) / sigma
    return -a * b



def max_exit_time(sigma,liq):
    # h,l meet the constraint of liq_lambda
    init_guess = np.array([1.5, .5])
    cons=(
        {"type": "eq", "fun": lambda x: liq_lambda(x[0],x[1])-liq},
        {"type":"ineq","fun":lambda x: x[0]-1},
        {"type":"ineq","fun":lambda x: 1-x[1]},
        {"type":"ineq","fun":lambda x: x[1]}
    )

    #max exit time
    res = minimize(lambda x: -exit_time(x[0],x[1],sigma), init_guess, constraints=cons)
    return res.x, -res.fun


#plot diffe

if "__main__" == __name__:
    sigma = 0.2
    liq = 5

    # h,l = 1.2,0.8
    # print("liq is,",liq_lambda(h,l))
    res = max_exit_time(sigma,liq)
    print(res)
    #
