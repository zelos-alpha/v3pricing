import numpy as np

from code.model.greek_cal import delta_cal, gamma_cal, vega_cal, rho_cal, dCCal, get_all_greeks
from code.model.UniV3StoppingTimePricingGen import (uni_v3_pricing_euroexcu_gbm_version_analytic_general_solution,
                                                    uni_v3_pricing_amerexcu_gbm_version_analytic_general_solution)
from matplotlib import pyplot as plt

func_dict = {
    'euro': uni_v3_pricing_euroexcu_gbm_version_analytic_general_solution,
    'amer': uni_v3_pricing_amerexcu_gbm_version_analytic_general_solution
}

euro_params = {
    'H': 1.2,
    'L': 0.5,
    'r': 0.08,
    'mu': 0.2,
    'C': 0.02,
    'sigma': 0.2,
    'S':1
}

amer_params = {
    'H': 2,
    'L': 0.5,
    'r': 0.05,
    'mu': 0.3,
    'C': 0.03,
    'sigma': 0.2,
    'S': 1

}


def plot_different_sigma_euro():
    func = func_dict["euro"]
    H = euro_params['H']
    L = euro_params['L']
    r = euro_params['r']
    mu = euro_params['mu']
    C = euro_params['C']
    S = euro_params['S']
    sigma_list = np.linspace(0.01, 0.4, 200)
    #value for different sigma
    value_list = [func(sigma=sigma, H=H,S=S,r=r,L=L,mu=mu,C=C) for sigma in sigma_list]
    #plot
    plt.plot(sigma_list, value_list)
    plt.xlabel('sigma')
    plt.ylabel('value')
    plt.title('value vs sigma')
    plt.show()


if __name__ == '__main__':
    plot_different_sigma_euro()