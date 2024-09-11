# 这个文件的作用是因为MC_for_uniswapV3这个脚本中，出现了公式和MC怎么都匹配不上的问题。
# 通过对C的改变，我发现C的改变对两边结果影响程度不一样
# 所以在这个脚本中我会做如下实验
# 把定价中的LP项折现和手续费项折现拆开，看看这两部分是不是有其中一部分能够和MC匹配。
import matplotlib.pyplot as plt
# fix matplotlib on mac
import matplotlib
import numpy as np
from numpy import exp, sqrt, log as ln

from MC.prob_mc_simulation import get_one_path_is_hit_a_and_time, v3_l_value, v3_h_value

matplotlib.use('TkAgg')



def one_path_value_LP_part(h, l, l1, l2, c, r, sigma,dt=0.0001):
    hit_a,t= get_one_path_is_hit_a_and_time(ln(l1)/sigma,ln(l2)/sigma,dt)
    if hit_a:
        return v3_l_value(h,l,l1)*exp(-r*t)
    else:
        return v3_h_value(h,l,l2)*exp(-r*t)


def one_path_value_fee_part(h, l, l1, l2, c, r, sigma,dt=0.0001):
    hit_a, t= get_one_path_is_hit_a_and_time(ln(l1)/sigma,ln(l2)/sigma,dt)
    # print(final_value)
    return t*c*exp(-r*t)


def one_path_value(h, l, l1, l2, c, r, sigma,dt=0.0001):
    hit_a,t= get_one_path_is_hit_a_and_time(ln(l1)/sigma,ln(l2)/sigma,dt)
    if hit_a:
        return v3_l_value(h,l,l1)*exp(-r*t)+t*c*exp(-r*t)
    else:
        return v3_h_value(h,l,l2)*exp(-r*t)+t*c*exp(-r*t)


def uni_v3_pricing_amerexecu_version_analytic_solution_LP_part(H, L, L1, L2, r, C, sigma):
    # 这个版本的S默认为1
    para_a = np.log(L1)/sigma
    para_b = np.log(L2)/sigma
    lambda_para = 1/(2-np.sqrt(L)-(1/np.sqrt(H)))
    part1_1 = lambda_para*(2*np.sqrt(L2)-np.sqrt(L)-(L2/np.sqrt(H)))
    part1_2 = np.sinh(-para_a*np.sqrt(2*r))/np.sinh((para_b-para_a)*np.sqrt(2*r))
    part2_1 = lambda_para*(2*np.sqrt(L1)-np.sqrt(L)-(L1/np.sqrt(H)))
    part2_2 = np.sinh(para_b*np.sqrt(2*r))/np.sinh((para_b-para_a)*np.sqrt(2*r))
    part1 = part1_1*part1_2
    part2 = part2_1*part2_2
    result = part1+part2
    # print(part1_1, part1_2, part2_1, part2_2)
    return result


def uni_v3_pricing_euroexecu_version_analytic_solution_fee_part(H, L, L1, L2, r, C, sigma):
    # 这个版本的S默认为1
    para_a = np.log(L1)/sigma
    para_b = np.log(L2)/sigma
    part3_1 = para_b*np.sinh(para_a*np.sqrt(2*r))+para_a*np.sinh(para_b*np.sqrt(2*r))
    part3_2 = np.sqrt(2*r)*(1+np.cosh((para_b-para_a)*np.sqrt(2*r)))
    part3 = -part3_1/part3_2
    result = C*part3
    return result


def plot_hist( dt = 1 / 52000):
    r = 0.04
    C = 0.03
    sigma = 0.4
    N = 1000
    h,l = 1.2, 0.8
    l1, l2 = 0.91, 1.17
    v = uni_v3_pricing_amerexecu_version_analytic_solution_LP_part(h, l, l1, l2, r, C, sigma)
    # print(ln(l)/sigma,ln(h)/sigma)

    v_values = [one_path_value_LP_part(h, l, l1, l2, C, r, sigma, dt) for _ in range(N)]
    # print(v3_h_value(h, l), v3_l_value(h, l))
    #print(v_values)
    # plt.hist(v_values,bins=100)
    # # plot the optimal v with label
    # plt.axvline(v, color='r', linestyle='dashed', linewidth=1)
    # # plot the mean value with label
    # plt.axvline(np.mean(v_values), color='g', linestyle='dashed', linewidth=1)
    #
    # plt.legend(["optimal v","mean v"])
    print("lp part analytic_solution is ",v)
    print("MC lp part is ",np.mean(v_values))

    # with r,c,sigma,h,l  on tilte
    # plt.title(f"r={r},C={C},sigma={sigma},h={h},l={l}")
    # plt.show()
    v1 = uni_v3_pricing_euroexecu_version_analytic_solution_fee_part(h, l, l1, l2, r, C, sigma)
    v_values1 = [one_path_value_fee_part(h, l, l1, l2, C, r, sigma, dt) for _ in range(N)]

    print("fee part analytic_solution is ",v1)
    print("MC fee part is ",np.mean(v_values1))

    print("total value is ",v+v1)
    print("MC total value is ",np.mean(v_values)+np.mean(v_values1))



"""
dt = 1 / 52000
lp part analytic_solution is  0.9798990101587357
MC lp part is  0.9793631459299904
fee part analytic_solution is  0.0027583849235332802
MC fee part is  0.002896738735424908
total value is  0.982657395082269
MC total value is  0.9822598846654154
"""

from UniV3PricingAme0Drift import uni_v3_pricing_amerexcu_version_analytic_solution
def compare_MC_and_analytic():
    r = 0.02
    C =  0.045
    sigma = 0.25
    N = 100
    h,l =  15881.454 , 0.1904
    l1, l2 =0.1904, 3.3762
    v = uni_v3_pricing_amerexcu_version_analytic_solution(h, l, l1, l2, r, C, sigma)
    print("analytic_solution is ",v)
    # MC is
    dt = 1 / 52000
    v_values = [one_path_value(h, l, l1, l2, C, r, sigma, dt) for _ in range(N)]
    print("MC is ",np.mean(v_values))
    print("diff is ",(v-np.mean(v_values))/v)


if __name__ == "__main__":
    compare_MC_and_analytic()
