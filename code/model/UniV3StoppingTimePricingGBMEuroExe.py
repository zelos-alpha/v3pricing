import numpy as np
import matplotlib.pyplot as plt


def uni_v3_pricing_euroexcu_gbm_version_analytic_solution(H, L, r, mu, C, sigma):
    # 这个版本的S默认为1
    para_a = np.log(L)/sigma
    para_b = np.log(H)/sigma
    lambda_para = 1/(2-np.sqrt(L)-(1/np.sqrt(H)))
    part1_1 = lambda_para*(np.sqrt(H)-np.sqrt(L))
    part1_2 = np.exp(para_b*mu)*np.sinh(-para_a*np.sqrt(2*r+mu**2))/np.sinh((para_b-para_a)*np.sqrt(2*r+mu**2))
    part2_1 = lambda_para*L*((1/np.sqrt(L))-(1/np.sqrt(H)))
    part2_2 = np.exp(para_a*mu)*np.sinh(para_b*np.sqrt(2*r+mu**2))/np.sinh((para_b-para_a)*np.sqrt(2*r+mu**2))
    part3_1_1_1 = para_b*np.exp(para_a*mu)*np.cosh(para_b*np.sqrt(2*r+mu**2))
    part3_1_1_2 = para_a*np.exp(para_b*mu)*np.cosh(para_a*np.sqrt(2*r+mu**2))
    part3_1_1 = part3_1_1_1-part3_1_1_2
    part3_1_2 = np.sqrt(2*r+mu**2)*np.sinh((para_b-para_a)*np.sqrt(2*r+mu**2))
    part3_2_1_1 = np.exp(para_a*mu)*np.sinh(para_b*np.sqrt(2*r+mu**2))
    part3_2_1_2 = np.exp(para_b*mu)*np.sinh(para_a*np.sqrt(2*r+mu**2))
    part3_2_1 = (para_b-para_a)*(part3_2_1_1-part3_2_1_2)
    part3_2_2 = np.sqrt(2*r+mu**2)*np.tanh((para_b-para_a)*np.sqrt(2*r+mu**2))*np.sinh((para_b-para_a)*np.sqrt(2*r+mu**2))
    part3_1 = part3_1_1/part3_1_2
    part3_2 = part3_2_1/part3_2_2
    part1 = part1_1*part1_2
    part2 = part2_1*part2_2
    part3 = part3_1-part3_2
    result = part1+part2-C*part3
    return result


if __name__ == '__main__':
    H = 1.2617
    L = 0.852365
    C = 0.07
    r = 0.04
    sigma = 0.12
    L_list = np.arange(0.90, 0.99, 0.01)
    H_list = np.arange(1.01, 1.10, 0.01)
    L_list, H_list = np.meshgrid(L_list, H_list)

    result = uni_v3_pricing_euroexcu_gbm_version_analytic_solution(H_list, L_list, r, 0, C, sigma)
    # print(result)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.plot_surface(L_list, H_list, result)
    plt.show()

    # print(uni_v3_pricing_earlyexcu_version_analytic_solution(H, L, 0.86, 1.10, 1, r, C, sigma))
