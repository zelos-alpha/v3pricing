import numpy as np
import matplotlib.pyplot as plt


def uni_v3_pricing_amerexcu_version_analytic_solution(H, L, L1, L2, r, C, sigma):
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


if __name__ == '__main__':
    # H = 1.2617
    # L = 0.852365
    # C = 0.059
    # r = 0.04
    # sigma = 0.12
    # L1_list = np.arange(0.86, 0.99, 0.01)
    # L2_list = np.arange(1.01, 1.25, 0.01)
    # L1_list, L2_list = np.meshgrid(L1_list, L2_list)
    # # result = [uni_v3_pricing_earlyexcu_version_analytic_solution(H, L, L1_list[-1], L2, 1, r, C, sigma) for L2 in L2_list]
    # # print(result)
    # # result = [uni_v3_pricing_earlyexcu_version_analytic_solution(H, L, L1, L2_list[0], 1, r, C, sigma) for L1 in L1_list]
    # # print(result)
    # # result = uni_v3_pricing_earlyexcu_version_analytic_solution(H, L, 0.86, 1.26, 1, r, C, sigma)
    # # print(result)
    #
    # result = uni_v3_pricing_amerexcu_version_analytic_solution(H, L, L1_list, L2_list, r, C, sigma)
    # # result = []
    # # for i in L1_list:
    # #     result_value = [uni_v3_pricing_earlyexcu_version_analytic_solution(H, L, i, L2, 1, r, C, sigma) for L2 in L2_list]
    # #     result.append(result_value)
    # #     print(result_value)
    # # result_z = np.array(result)
    # # print(result_z)
    # # print(type(result_z))
    # # print(type(L1_list))
    # # resullt = np.ndarray
    # # result = [uni_v3_pricing_earlyexcu_version_analytic_solution(H, L, L1, L2, 1, r, C, sigma) for L1 in L1_list and for L2 in L2_list]
    # fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # ax.plot_surface(L1_list, L2_list, result)
    # plt.show()

    # print(uni_v3_pricing_earlyexcu_version_analytic_solution(H, L, 0.86, 1.10, 1, r, C, sigma))
    r = 0.02
    C = 0.1
    sigma = 0.1
    N = 1000
    h, l = 1.2, 0.8
    l1, l2 = 0.93, 1.1
    V0 = uni_v3_pricing_amerexcu_version_analytic_solution(h, l, l1, l2, r, C, sigma)
    print(V0)