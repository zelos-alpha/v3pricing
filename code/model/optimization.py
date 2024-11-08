import numpy as np
from scipy.optimize import minimize, basinhopping, shgo
from sympy import ln

from UniV3PricingAme0Drift import uni_v3_pricing_amerexcu_version_analytic_solution
from code.model.UniV3StoppingTimePricingEuroExe import uni_v3_pricing_euroexcu_version_analytic_solution
from code.model.UniV3StoppingTimePricingGen import uni_v3_pricing_euroexcu_gbm_version_analytic_general_solution, \
    uni_v3_pricing_amerexcu_gbm_version_analytic_general_solution

#from .Penalty_Term_Cal import Amer_Pricing_Penalty_Term_Value_0drift_Version
np.set_printoptions(formatter={'float': lambda x: "{0:0.4f}".format(x)})


def EuroOptimize(r,C,sigma,bounds=(0.02,80)):
    lower,upper = bounds
    bounds = [(1.01, upper), ( lower,0.99)]
    ret = shgo(lambda x: -uni_v3_pricing_euroexcu_gbm_version_analytic_general_solution(1,x[0], x[1], r,0, C, sigma),
                       bounds=bounds,n=400)
    return ret.x, -ret.fun

#def uni_v3_pricing_amerexcu_gbm_version_analytic_general_solution(S, H, L, L1, L2, r, mu, C, sigma
def AmericanOptimize(r,C,sigma,bounds=(0.02,80)):
    lower,upper = bounds
    bounds = [(1.01, upper), (lower,0.99), ( lower,0.99),(1.01, upper)]
    #constraints
    cons = ({'type': 'ineq', 'fun': lambda x: x[0]-x[3]},
            {'type': 'ineq', 'fun': lambda x: x[2]-x[1]},)

    ret = shgo(lambda x: -uni_v3_pricing_amerexcu_gbm_version_analytic_general_solution(1,x[0], x[1],x[2],x[3], r, 0,C, sigma),
                       bounds=bounds,constraints=cons,n=400)
    return ret.x, -ret.fun


if __name__ == '__main__':
    # C = 0.15
    # r = 0.05
    # sigma = 0.20
    C = 0.15
    r = 0.05
    sigma = 0.8

    res, V = AmericanOptimize(r, C, sigma)
    H, L, L1, L2 = res
    #print solution
    print(f"H:{H}, L:{L}, L1:{L1}, L2:{L2}, V:{V}")

    res,V =EuroOptimize(r, C, sigma)
    H, L = res
    print(f"H:{H}, L:{L}, V:{V}")

#
# def AmericanWithOutPenaltyOptimize(r,C,sigma):
#     #H,L,L1,L2
#
#     init_guess = np.array([1.5, .5, 0.8,1.2])
#     cons = (
#         {"type": "ineq", "fun": lambda x: x[0]-1},
#         {"type": "ineq", "fun": lambda x: x[1]},
#         {"type": "ineq", "fun": lambda x: 1-x[1]},
#         {"type": "ineq", "fun": lambda x: x[2]-x[1]},
#         {"type": "ineq", "fun": lambda x: 1-x[2]},
#         {"type": "ineq", "fun": lambda x: x[0]-x[3]},
#         {"type": "ineq", "fun": lambda x: x[3]-1},
#     )
#     v_fnc = uni_v3_pricing_amerexcu_version_analytic_solution
#     def fnc(x):
#         return -v_fnc(x[0], x[1], x[2], x[3], r, C, sigma)
#     res = minimize(fnc, init_guess, constraints=cons)
#     return res.x, -res.fun
#
#
#
#
# def AmericanWithPenaltyOptimize(r,C,sigma,k = 0.005):
#     #H,L,L1,L2
#
#     init_guess = np.array([1.5, .5, 0.8,1.2])
#     cons = (
#         {"type": "ineq", "fun": lambda x: x[0]-1},
#         {"type": "ineq", "fun": lambda x: x[1]},
#         {"type": "ineq", "fun": lambda x: 1-x[1]},
#         {"type": "ineq", "fun": lambda x: x[2]-x[1]},
#         {"type": "ineq", "fun": lambda x: 1-x[2]},
#         {"type": "ineq", "fun": lambda x: x[0]-x[3]},
#         {"type": "ineq", "fun": lambda x: x[3]-1},
#     )
#     v_fnc = uni_v3_pricing_amerexcu_version_analytic_solution
#     penalty = Amer_Pricing_Penalty_Term_Value_0drift_Version
#     def fnc(x):
#         return -v_fnc(x[0], x[1], x[2], x[3], r, C, sigma) - penalty(x[1], x[0], x[2], x[3], r, k, sigma)
#     res = minimize(fnc, init_guess, constraints=cons)
#     return res.x, -res.fun
#
#
#
#
# if __name__ == '__main__':
#     C = 0.15
#     r =  0.05
#     sigma = 0.20
#     result = EuroOptimize(r, C, sigma)
#
#     h,l = result[0]
#     a = ln(l)/sigma
#     b = ln(h)/sigma
#     #expect exit time is -ab
#     expect_exit_time = -a*b
#     print("C,r,sigma:", C, r, sigma)
#     print("expect exit time is:", expect_exit_time)
#     print("H,L,V:", result)
#     # result,v = AmericanWithOutPenaltyOptimize(r, C, sigma)
#     # #print each one in the result
#     # print(result,v)