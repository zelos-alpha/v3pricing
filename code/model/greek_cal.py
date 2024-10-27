import numpy as np
import matplotlib.pyplot as plt
from code.model.UniV3StoppingTimePricingGen import (uni_v3_pricing_payoff_version_analytic_solution,
                                                    uni_v3_pricing_euroexcu_gbm_version_analytic_general_solution,
                                                    uni_v3_pricing_amerexcu_gbm_version_analytic_general_solution)


def delta_cal(S, H, L, r, mu, C, sigma, L1=0.5, L2=1.5, option_type='euro'):
    if option_type == 'euro':
        pv_left = uni_v3_pricing_euroexcu_gbm_version_analytic_general_solution(S-0.0001, H, L, r, mu, C, sigma)
        pv_right = uni_v3_pricing_euroexcu_gbm_version_analytic_general_solution(S+0.0001, H, L, r, mu, C, sigma)
        result = (pv_right-pv_left)/0.0002
    elif option_type == 'amer':
        pv_left = uni_v3_pricing_amerexcu_gbm_version_analytic_general_solution(S-0.0001, H, L, L1, L2, r, mu, C, sigma)
        pv_right = uni_v3_pricing_amerexcu_gbm_version_analytic_general_solution(S+0.0001, H, L, L1, L2, r, mu, C, sigma)
        result = (pv_right-pv_left)/0.0002
    elif option_type == 'payoff':
        pv_left = uni_v3_pricing_payoff_version_analytic_solution(S-0.0001, H, L)
        pv_right = uni_v3_pricing_payoff_version_analytic_solution(S+0.0001, H, L)
        result = (pv_right-pv_left)/0.0002
    else:
        raise Exception('Wrong option type input!')
    return result


def gamma_cal(S, H, L, r, mu, C, sigma, L1=0.5, L2=1.5, option_type='euro'):
    delta_left = delta_cal(S-0.0001, H, L, r, mu, C,sigma, L1, L2, option_type)
    delta_right = delta_cal(S+0.0001, H, L, r, mu, C,sigma, L1, L2, option_type)
    result = (delta_right-delta_left)/0.0002
    return result


if __name__ == '__main__':
    S = 1
    H = 1.1
    L = 0.9
    C = 0.005
    r = 0.04
    sigma = 0.25

    S_list = np.linspace(0.85, 1.15, 200)
    payoff_delta = [delta_cal(S, H, L, r, 0, C, sigma, option_type='payoff') for S in S_list]
    payoff_gamma = [gamma_cal(S, H, L, r, 0, C, sigma, option_type='payoff') for S in S_list]
    euro_delta = [delta_cal(S, H, L, r, 0, C, sigma, option_type='euro') for S in S_list]
    euro_gamma = [gamma_cal(S, H, L, r, 0, C, sigma, option_type='euro') for S in S_list]
    payoff_pv = [uni_v3_pricing_payoff_version_analytic_solution(S, H, L) for S in S_list]
    euro_pv = [uni_v3_pricing_euroexcu_gbm_version_analytic_general_solution(S, H, L, r, 0, C, sigma) for S in S_list]
    plt.plot(S_list, euro_pv)
    plt.savefig('C=0005.png')
    plt.show()
