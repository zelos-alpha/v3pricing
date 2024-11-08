import numpy as np

from code.model.greek_cal import delta_cal, gamma_cal, vega_cal, rho_cal, dCCal, get_all_greeks
from code.model.UniV3StoppingTimePricingGen import (uni_v3_pricing_euroexcu_gbm_version_analytic_general_solution,
                                                    uni_v3_pricing_amerexcu_gbm_version_analytic_general_solution)
from matplotlib import pyplot as plt

from code.model.optimization import AmericanOptimize_fix

func_dict = {
    'euro': uni_v3_pricing_euroexcu_gbm_version_analytic_general_solution,
    'amer': uni_v3_pricing_amerexcu_gbm_version_analytic_general_solution
}

euro_params = {
    'H': 1.5,
    'L': 0.8,
    'r': 0.04,
    'mu': 0.0,
    'C': 0.2,
    'sigma': 1.2,
}


def get_l1_l2():
    H=euro_params['H']
    L=euro_params['L']
    r=euro_params['r']
    mu=euro_params['mu']
    C=euro_params['C']
    sigma = euro_params['sigma']
    # def AmericanOptimize_fix(r,C,sigma,H,L,bounds=(0.02,80)):
    res = AmericanOptimize_fix(r,C,sigma,H,L)
    L1,L2 = res[0]
    print(f"L1:{L1}, L2:{L2}")
    return L1,L2

def plot_diff_ame_and_euro():

    L1,L2 = get_l1_l2()
    H=euro_params['H']
    L=euro_params['L']
    r=euro_params['r']
    mu=euro_params['mu']
    C=euro_params['C']
    sigma = euro_params['sigma']
    s_list = np.linspace(L, H, 20)
    print(f"H:{H}, L:{L}, L1:{L1}, L2:{L2}, r:{r}, mu:{mu}, C:{C}, sigma:{sigma}")
    # uni_v3_pricing_euroexcu_gbm_version_analytic_general_solution(S, H, L, r, mu, C, sigma):
    euro_value_list = [uni_v3_pricing_euroexcu_gbm_version_analytic_general_solution(s, H,L,r,mu,C,sigma) for s in s_list]
    #uni_v3_pricing_amerexcu_gbm_version_analytic_general_solution(S, H, L, L1, L2, r, mu, C, sigma):
    amer_value_list = [uni_v3_pricing_amerexcu_gbm_version_analytic_general_solution(s,H,L,L1,L2,r,mu,C,sigma) for s in s_list]
    plt.plot(s_list, euro_value_list, label='euro')
    plt.plot(s_list, amer_value_list, label='amer')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    plot_diff_ame_and_euro()

