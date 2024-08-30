import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, shgo


def uni_v3_pricing_amerexcu_version_analytic_solution(H,L,L1,L2, r, C, sigma):
    # 这个版本的S默认为1
    para_a = np.log(L1)/sigma
    para_b = np.log(L2)/sigma
    lambda_para = 1/(2-np.sqrt(L)-(1/np.sqrt(H)))
    part1_1 = lambda_para*(2*np.sqrt(L2)-np.sqrt(L)-(L2/np.sqrt(H)))
    part1_2 = np.sinh(-para_a*np.sqrt(2*r))/np.sinh((para_b-para_a)*np.sqrt(2*r))
    part2_1 = lambda_para*(2*np.sqrt(L1)-np.sqrt(L)-(L1/np.sqrt(H)))
    part2_2 = np.sinh(para_b*np.sqrt(2*r))/np.sinh((para_b-para_a)*np.sqrt(2*r))
    part3_1 = para_b*np.sinh(para_a*np.sqrt(2*r))+para_a*np.sinh(para_b*np.sqrt(2*r))
    part3_2 = np.sqrt(2*r)*(1+np.cosh((para_b-para_a)*np.sqrt(2*r)))
    part1 = part1_1*part1_2
    part2 = part2_1*part2_2
    part3 = -part3_1/part3_2
    result = part1+part2+C*part3
    return result


def uni_v3_pricing_amerexcu_version_analytic_optimze(r,C,sigma):

    cons = (
        {"type": "ineq", "fun": lambda x: x[0]-1},
        {"type": "ineq", "fun": lambda x: x[1]},
        {"type": "ineq", "fun": lambda x: 1-x[1]},
        {"type": "ineq", "fun": lambda x: x[2]-x[1]},
        {"type": "ineq", "fun": lambda x: 1- x[2]},
        {"type": "ineq", "fun": lambda x: x[0]-x[3]},
        {"type": "ineq", "fun": lambda x: x[3] - 1},

    )
    bounds = [(1, 2000),(0.01,0.99),(0.01,0.99),(1.01,2000) ]
    res = shgo(lambda x: uni_v3_pricing_amerexcu_version_analytic_solution(x[0], x[1], x[2], x[3], r, C, sigma),bounds, n = 100,constraints=cons)
    print(res)
    return res

if __name__ == '__main__':
    # H = 30000
    # L =  0.1904
    # C = 0.045
    # r = 0.02
    # l1, l2 =  0.1904, 3.3762
    # sigma =0.25
    # result = uni_v3_pricing_amerexcu_version_analytic_solution(H, L, l1, l2, r, C, sigma)
    #
    # from MC.prob_mc_simulation import lambda_liq
    #
    # print(result)
    #
    C = 0.034
    r = 0.02
    sigma = 0.25
    res = uni_v3_pricing_amerexcu_version_analytic_optimze(r, C, sigma)
    print(res.x)
    # print H,L,L1,L2 with round 4
    #print("H,L,L1,L2:",round(H,4),round(L,4),round(L1,4),round(L2,4), "V:",round(res[1],4))
    #
    #
    """
    C = 0.045
    r = 0.02
    sigma = 0.25
    H,L,L1,L2: 15881.454 0.1904 0.1904 3.3762 V: 1.3948
    """