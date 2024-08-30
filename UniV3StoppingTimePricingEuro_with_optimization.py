import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from sympy import ln


def uni_v3_pricing_euroexecu_version_analytic_solution_LP_part(H, L, r, C, sigma):
    # 这个版本的S默认为1
    para_a = np.log(L)/sigma
    para_b = np.log(H)/sigma
    lambda_para = 1/(2-np.sqrt(L)-(1/np.sqrt(H)))
    part1_1 = lambda_para*(np.sqrt(H)-np.sqrt(L))
    part1_2 = np.sinh(-para_a*np.sqrt(2*r))/np.sinh((para_b-para_a)*np.sqrt(2*r))
    part2_1 = lambda_para*L*((1/np.sqrt(L))-(1/np.sqrt(H)))
    part2_2 = np.sinh(para_b*np.sqrt(2*r))/np.sinh((para_b-para_a)*np.sqrt(2*r))
    part1 = part1_1*part1_2
    part2 = part2_1*part2_2
    result = part1+part2
    #print(part1_1, part1_2, part2_1, part2_2)
    return result


def uni_v3_pricing_euroexecu_version_analytic_solution_fee_part(H, L, r, C, sigma):
    # 这个版本的S默认为1
    para_a = np.log(L)/sigma
    para_b = np.log(H)/sigma
    part3_1 = para_b*np.sinh(para_a*np.sqrt(2*r))+para_a*np.sinh(para_b*np.sqrt(2*r))
    part3_2 = np.sqrt(2*r)*(1+np.cosh((para_b-para_a)*np.sqrt(2*r)))
    part3 = -part3_1/part3_2
    result = C*part3
    return result

def uni_v3_pricing_euroexcu_version_analytic_solution(H,L,r,C,sigma):
    fee =  uni_v3_pricing_euroexecu_version_analytic_solution_fee_part(H, L, r, C, sigma)
    LP = uni_v3_pricing_euroexecu_version_analytic_solution_LP_part(H, L, r, C, sigma)
    return fee+LP


# given r,C,sigma,get optimal H,L, and the value of V
def uni_v3_pricing_euroexcu_version_analytic_solution_optimize(r, C, sigma):
    # init guess = H,L
    init_guess = np.array([1.5, .5])
    cons = (
        {"type": "ineq", "fun": lambda x: x[0]-1.1},
        {"type": "ineq", "fun": lambda x: x[1]},
        {"type": "ineq", "fun": lambda x: 0.9-x[1]},
        # {"type": "ineq", "fun": lambda x: x[0]-x[1]-0.3},
    )
    res = minimize(lambda x: -uni_v3_pricing_euroexcu_version_analytic_solution(x[0], x[1], r, C, sigma), init_guess, constraints=cons)
    return res.x, -res.fun


def demo_optimization():
    C = 0.04
    r =  0.03
    sigma = 0.2
    result = uni_v3_pricing_euroexcu_version_analytic_solution_optimize(r, C, sigma)

    h,l = result[0]
    a = ln(l)/sigma
    b = ln(h)/sigma
    #expect exit time is -ab
    expect_exit_time = -a*b
    print("C,r,sigma:", C, r, sigma)
    print("expect exit time is:", expect_exit_time)
    print("H,L,V:", result)




def plot_v_for_different_sigma():
    C = 0.05
    r = 0.02
    sigma_list = np.linspace(0.1, 0.5, 50)
    result = [uni_v3_pricing_euroexcu_version_analytic_solution_optimize(r, C, sigma) for sigma in sigma_list]
    #h,l,v
    h_list = [i[0][0] for i in result]
    l_list = [i[0][1] for i in result]
    v_list = [i[1] for i in result]

    # first subplot: hl vs sigma ,second subplot: v vs sigma，third plot expect exit time vs sigma
    fig, axs = plt.subplots(3)
    axs[0].plot(sigma_list, h_list, label="H")
    axs[0].plot(sigma_list, l_list, label="L")
    axs[0].set_xlabel("sigma")
    axs[0].set_ylabel("H,L")
    axs[0].legend()
    axs[1].plot(sigma_list, v_list, label="V")
    axs[1].set_xlabel("sigma")
    axs[1].set_ylabel("V")
    axs[1].legend()

    expect_exit_time = [-ln(l)/sigma*ln(h)/sigma for l,h,sigma in zip(l_list,h_list,sigma_list)]


    axs[2].plot(sigma_list, expect_exit_time, label="expect exit time")
    axs[2].set_xlabel("sigma")
    axs[2].set_ylabel("expect exit time")
    axs[2].legend()
    plt.show()


    # print
    for i,sigma in enumerate(sigma_list):
        print(f"sigma:{sigma}, H:{h_list[i]}, L:{l_list[i]}, V:{v_list[i]}")


if __name__ == '__main__':
    #plot_v_for_different_sigma()
    # H = 1.2617
    # L = 0.852365
    # C = 0.001
    # r = 0.04
    # sigma = 0.12
    # L_list = np.arange(0.90, 0.99, 0.01)
    # H_list = np.arange(1.01, 1.10, 0.01)
    # L_list, H_list = np.meshgrid(L_list, H_list)
    # result = [uni_v3_pricing_earlyexcu_version_analytic_solution(H, L, L1_list[-1], L2, 1, r, C, sigma) for L2 in L2_list]
    # print(result)
    # result = [uni_v3_pricing_earlyexcu_version_analytic_solution(H, L, L1, L2_list[0], 1, r, C, sigma) for L1 in L1_list]
    # print(result)
    # result = uni_v3_pricing_earlyexcu_version_analytic_solution(H, L, 0.86, 1.26, 1, r, C, sigma)
    # print(result)

    # result = uni_v3_pricing_euroexcu_version_analytic_solution(H_list, L_list, r, C, sigma)
    # result = []
    # for i in L1_list:
    #     result_value = [uni_v3_pricing_earlyexcu_version_analytic_solution(H, L, i, L2, 1, r, C, sigma) for L2 in L2_list]
    #     result.append(result_value)
    #     print(result_value)
    # result_z = np.array(result)
    # print(result_z)
    # print(type(result_z))
    # print(type(L1_list))
    # resullt = np.ndarray
    # result = [uni_v3_pricing_earlyexcu_version_analytic_solution(H, L, L1, L2, 1, r, C, sigma) for L1 in L1_list and for L2 in L2_list]
    # fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # ax.plot_surface(L_list, H_list, result)
    # plt.show()
    #
    # print(uni_v3_pricing_earlyexcu_version_analytic_solution(H, L, 0.86, 1.10, 1, r, C, sigma))


    demo_optimization()

