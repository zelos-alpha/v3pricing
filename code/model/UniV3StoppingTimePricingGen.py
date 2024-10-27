import numpy as np


def uni_v3_pricing_payoff_version_analytic_solution(S, H, L):
    lambda_para=1/(2-np.sqrt(L)-(1/np.sqrt(H)))
    if S <= L:
        result = lambda_para*S*((1/np.sqrt(L))-(1/np.sqrt(H)))
    elif L < S <= H:
        result = lambda_para*(2*np.sqrt(S)-np.sqrt(L)-(S/np.sqrt(H)))
    else:
        result = lambda_para*(np.sqrt(H)-np.sqrt(L))
    return result


def uni_v3_pricing_euroexcu_gbm_version_analytic_general_solution(S, H, L, r, mu, C, sigma):
    para_x = np.log(S)/sigma
    para_a = np.log(L)/sigma
    para_b = np.log(H)/sigma
    lambda_para = 1/(2-np.sqrt(L)-(1/np.sqrt(H)))
    payoff_high = lambda_para*(np.sqrt(H)-np.sqrt(L))
    payoff_low = lambda_para*L*((1/np.sqrt(L))-(1/np.sqrt(H)))
    result = uni_v3_pricing_gbm_version_analytic_general_solution(payoff_low,
                                                                  payoff_high,
                                                                  para_a,
                                                                  para_x,
                                                                  para_b,
                                                                  r,
                                                                  mu,
                                                                  C*lambda_para)
    return result


def uni_v3_pricing_amerexcu_gbm_version_analytic_general_solution(S, H, L, L1, L2, r, mu, C, sigma):
    para_x = np.log(S)/sigma
    para_a = np.log(L1)/sigma
    para_b = np.log(L2)/sigma
    lambda_para = 1/(2-np.sqrt(L)-(1/np.sqrt(H)))
    payoff_high = lambda_para*(2*np.sqrt(L2)-np.sqrt(L)-(L2/np.sqrt(H)))
    payoff_low = lambda_para*(2*np.sqrt(L1)-np.sqrt(L)-(L1/np.sqrt(H)))
    result = uni_v3_pricing_gbm_version_analytic_general_solution(payoff_low,
                                                                  payoff_high,
                                                                  para_a,
                                                                  para_x,
                                                                  para_b,
                                                                  r,
                                                                  mu,
                                                                  C*lambda_para)
    return result


def uni_v3_pricing_gbm_version_analytic_general_solution(payoff_low, payoff_high, a, x, b, r, mu, C):
    part1 = payoff_high*np.exp(mu*(b-x))*np.sinh((x-a)*np.sqrt(2*r+mu**2))/np.sinh((b-a)*np.sqrt(2*r+mu**2))
    part2 = payoff_low*np.exp(mu*(a-x))*np.sinh((b-x)*np.sqrt(2*r+mu**2))/np.sinh((b-a)*np.sqrt(2*r+mu**2))
    part3_1_1 = np.exp(mu*(a-x))*(b-x)*np.cosh((b-x)*np.sqrt(2*r+mu**2))+np.exp(mu*(b-x))*(x-a)*np.cosh((x-a)*np.sqrt(2*r+mu**2))
    part3_1_2 = np.sqrt(2*r+mu**2)*np.sinh((b-a)*np.sqrt(2*r+mu**2))
    part3_2_1 = np.exp(mu*(a-x))*np.sinh((b-x)*np.sqrt(2*r+mu**2))+np.exp(mu*(b-x))*np.sinh((x-a)*np.sqrt(2*r+mu**2))
    part3_2_2 = np.sqrt(2*r+mu**2)*np.tanh((b-a)*np.sqrt(2*r+mu**2))*np.sinh((b-a)*np.sqrt(2*r+mu**2))
    part3_1 = part3_1_1/part3_1_2
    part3_2 = (b-a)*part3_2_1/part3_2_2
    part3 = C*(-(part3_1-part3_2))
    result = part1+part2+part3
    return result


if __name__ == '__main__':
    # H = 1.2617
    # L = 0.852365
    # C = 0.055
    # r = 0.04
    # sigma = 0.12
    # L_list = np.arange(0.90, 0.99, 0.01)
    # H_list = np.arange(1.01, 1.10, 0.01)
    # L_list, H_list = np.meshgrid(L_list, H_list)
    # L1_list = 0.90
    # L2_list = 1.10
    #
    # result = uni_v3_pricing_amerexcu_gbm_version_analytic_general_solution(1, H, L, L1_list, L2_list, r, 0, C, sigma)
    # print(result)

    # fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # ax.plot_surface(L_list, H_list, result)
    # plt.show()

    # print(uni_v3_pricing_earlyexcu_version_analytic_solution(H, L, 0.86, 1.10, 1, r, C, sigma))

    S = 1
    H = 1.1
    L = 0.9
    C = 0.005
    r = 0.04
    sigma = 0.25

    # payoff_delta = delta_cal(S, H, L, r, 0, C, sigma, option_type='payoff')
    # euro_delta = delta_cal(S, H, L, r, 0, C, sigma, option_type='euro')
    # #amer_delta = delta_cal()
    # payoff_gamma = gamma_cal(S, H, L, r, 0, C, sigma, option_type='payoff')
    # euro_gamma = gamma_cal(S, H, L, r, 0, C, sigma, option_type='euro')
    # print('payoff delta&gamma are:', payoff_delta, payoff_gamma)
    # print('euro delta&gamma are:', euro_delta, euro_gamma)
