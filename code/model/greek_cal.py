import numpy as np
import matplotlib.pyplot as plt
from code.model.UniV3StoppingTimePricingGen import (uni_v3_pricing_payoff_version_analytic_solution,
                                                    uni_v3_pricing_euroexcu_gbm_version_analytic_general_solution,
                                                    uni_v3_pricing_amerexcu_gbm_version_analytic_general_solution)

func_dict = {
    'payoff': uni_v3_pricing_payoff_version_analytic_solution,
    'euro': uni_v3_pricing_euroexcu_gbm_version_analytic_general_solution,
    'amer': uni_v3_pricing_amerexcu_gbm_version_analytic_general_solution
}



def delta_cal(S, H, L, option_type='euro', ds=0.0001, **kwargs):
    pricing_func = func_dict[option_type]
    pv_left = pricing_func(S-ds, H, L, **kwargs)
    pv_right = pricing_func(S+ds, H, L, **kwargs)
    return (pv_right - pv_left) / (2*ds)




def gamma_cal(S, H, L, option_type='euro', ds=0.0001, **kwargs):
    delta_left = delta_cal(S-ds, H, L, option_type=option_type, ds=ds, **kwargs)
    delta_right = delta_cal(S+ds, H, L, option_type=option_type, ds=ds, **kwargs)
    result = (delta_right - delta_left) / ds
    return result


def vega_cal(S, H, L, sigma, option_type='euro', dsigma=0.0001, **kwargs):
    if option_type == 'payoff':
        return None
    func = func_dict[option_type]
    pv_left = func(S, H, L, sigma=sigma-dsigma,**kwargs)
    pv_right = func(S, H, L, sigma = sigma+dsigma,**kwargs)
    return (pv_right-pv_left)/(2*dsigma)

def rho_cal(S, H, L, r, option_type='euro', dr=0.0001, **kwargs):
    if option_type == 'payoff':
        return None
    func = func_dict[option_type]
    pv_left = func(S, H, L, r=r-dr, **kwargs)
    pv_right = func(S, H, L, r=r+dr, **kwargs)
    return (pv_right-pv_left)/(2*dr)

def dCCal(S, H, L, C, option_type='euro', dC=0.0001, **kwargs):
    if option_type == 'payoff':
        return None
    func = func_dict[option_type]
    pv_left = func(S, H, L, C=C-dC, **kwargs)
    pv_right = func(S, H, L, C=C+dC, **kwargs)
    return (pv_right-pv_left)/(2*dC)



def get_all_greeks(S, H, L, r,C,sigma,option_type , **kwargs):
    delta = delta_cal(S, H, L,r=r,C=C,sigma=sigma, option_type=option_type, **kwargs)
    gamma = gamma_cal(S, H, L,r=r,C=C,sigma=sigma, option_type=option_type, **kwargs)
    vega = vega_cal(S, H, L, sigma, r=r, C=C, option_type=option_type, **kwargs)
    rho = rho_cal(S, H, L, r, C=C, sigma=sigma, option_type=option_type, **kwargs)
    dC = dCCal(S, H, L, C, r=r, sigma=sigma, option_type=option_type, **kwargs)
    return delta, gamma, vega, rho, dC
def test_greeks():
    S = 1
    H = 1.1
    L = 0.9
    C = 0.08
    r = 0.03
    sigma = 0.25
    mu = 0
    L1 =0.95
    L2 = 1.05

    # Test for European option
    params = {'S': S, 'H': H, 'L': L, 'r': r, 'C': C, 'sigma': sigma, 'mu': mu, 'option_type': 'euro'}
    euro_greeks = get_all_greeks(**params)


    # Test for American option
    params = {'S': S, 'H': H, 'L': L, 'r': r, 'C': C, 'sigma': sigma, 'mu': mu,'L1':L1, 'L2':L2, 'option_type': 'amer'}
    ame_greeks = get_all_greeks(**params)

    # Test for Payoff option
    payoff_delta = delta_cal(S=S, H=H, L=L, option_type='payoff')
    payoff_gamma = gamma_cal(S=S, H=H, L=L, option_type='payoff')

    # Print all Delta values first
    print("=====================delta==============================")
    euro_delta, amer_delta, payoff_delta = euro_greeks[0], ame_greeks[0], payoff_delta
    print(f"European Option Delta: {euro_delta}")
    print(f"American Option Delta: {amer_delta}")
    print(f"Payoff Option Delta: {payoff_delta}")
    # Print all Gamma values
    print("=====================gamma==============================")
    euro_gamma, amer_gamma = euro_greeks[1], ame_greeks[1]
    print(f"European Option Gamma: {euro_gamma}")
    print(f"American Option Gamma: {amer_gamma}")
    print(f"Payoff Option Gamma: {payoff_gamma}")

    # Print all Vega values
    print("=====================vega==============================")
    euro_vega, amer_vega = euro_greeks[2], ame_greeks[2]
    print(f"European Option Vega: {euro_vega}")
    print(f"American Option Vega: {amer_vega}")

    # Print all Rho values
    print("=====================rho==============================")
    euro_rho, amer_rho = euro_greeks[3], ame_greeks[3]
    print(f"European Option Rho: {euro_rho}")
    print(f"American Option Rho: {amer_rho}")

    # Print all dC values
    print("=====================dC==============================")
    euro_dC, amer_dC = euro_greeks[4], ame_greeks[4]
    print(f"European Option dC: {euro_dC}")
    print(f"American Option dC: {amer_dC}")


if __name__ == '__main__':
    test_greeks()
