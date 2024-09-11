import numpy as np
from scipy.optimize import minimize
from sympy import ln

from UniV3PricingAme0Drift import uni_v3_pricing_amerexcu_version_analytic_solution
from UniV3StoppingTimePricingEuro_with_optimization import uni_v3_pricing_euroexcu_version_analytic_solution
from Penalty_Term_Cal import Amer_Pricing_Penalty_Term_Value_0drift_Version


def EuroOptimize(r,C,sigma):
    init_guess = np.array([1.5, .5])
    cons = (
        {"type": "ineq", "fun": lambda x: x[0]-1.1},
        {"type": "ineq", "fun": lambda x: x[1]},
        {"type": "ineq", "fun": lambda x: 0.9-x[1]},
        # {"type": "ineq", "fun": lambda x: x[0]-x[1]-0.3},
    )
    res = minimize(lambda x: -uni_v3_pricing_euroexcu_version_analytic_solution(x[0], x[1], r, C, sigma), init_guess, constraints=cons)
    return res.x, -res.fun

def AmericanWithPenaltyOptimize(r,C,sigma,k = 0.005):
    #H,L,L1,L2

    init_guess = np.array([1.5, .5, 0.8,1.2])
    cons = (
        {"type": "ineq", "fun": lambda x: x[0]-1},
        {"type": "ineq", "fun": lambda x: x[1]},
        {"type": "ineq", "fun": lambda x: 1-x[1]},
        {"type": "ineq", "fun": lambda x: x[2]-x[1]},
        {"type": "ineq", "fun": lambda x: 1-x[2]},
        {"type": "ineq", "fun": lambda x: x[0]-x[3]},
        {"type": "ineq", "fun": lambda x: x[3]-1},
    )
    v_fnc = uni_v3_pricing_amerexcu_version_analytic_solution
    penalty = Amer_Pricing_Penalty_Term_Value_0drift_Version
    def fnc(x):
        return -v_fnc(x[0], x[1], x[2], x[3], r, C, sigma) - penalty(x[1], x[0], x[2], x[3], r, k, sigma)
    res = minimize(fnc, init_guess, constraints=cons)
    return res.x, -res.fun




if __name__ == '__main__':
    C = 0.04
    r =  0.03
    sigma = 0.2
    # result = EuroOptimize(r, C, sigma)
    #
    # h,l = result[0]
    # a = ln(l)/sigma
    # b = ln(h)/sigma
    # #expect exit time is -ab
    # expect_exit_time = -a*b
    # print("C,r,sigma:", C, r, sigma)
    # print("expect exit time is:", expect_exit_time)
    # print("H,L,V:", result)
    result = AmericanWithPenaltyOptimize(r, C, sigma)
    print(result)