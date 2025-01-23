import numpy as np
from scipy.integrate import quad
from math import log, sqrt, sinh, cosh, exp, pi
# irr的cal计算成功，指没出bug，但是数值是负值，带之后review


def irr_cal(S, L, H, sigma, r, mu):
    para_a=log(L)/sigma
    para_b=log(H)/sigma
    para_x=log(S)/sigma
    # print(L, H, para_a, para_b)
    lambda_para = 1 / (2 - sqrt(L) - (1 / sqrt(H)))
    lower_bound_lp_part=-lambda_para*L*(1/sqrt(L)-1/sqrt(H))*exp(mu*(para_a-para_x))*lower_bound_inf_int_value(para_x, para_a, para_b, r, mu)
    upper_bound_lp_part=-lambda_para*(sqrt(H)-sqrt(L)*exp(mu*(para_b-para_x))*upper_bound_inf_int_value(para_x, para_a, para_b, r, mu))
    fee_part=cosh((para_b+para_a)*sqrt(2*r+mu**2)/2)/cosh((para_b-para_x)*sqrt(2*r+mu**2)/2)
    # 1/tau目前的解析式待定，还未成功推导他和那个两个cosh的除法积分的关系
    last_part=(pi**2)/(8*((para_b-para_a)**2))
    return lower_bound_lp_part+upper_bound_lp_part+fee_part-last_part


def lower_bound_inf_int_function(x,a,b,z,mu):
    part1=(b-x)*sqrt(2*z+mu**2)
    part2=(b-a)*sqrt(2*z+mu**2)
    return sinh(part1)/sinh(part2)


def lower_bound_inf_int_value(x, a, b, r, mu):
    value, error = quad(lambda z:lower_bound_inf_int_function(x, a, b, z, mu), r, np.inf)
    return value


def upper_bound_inf_int_value(x,a,b,r,mu):
    value, error = quad(lambda z:upper_bound_int_int_function(x,a,b,z,mu), r, np.inf)
    return value


def upper_bound_int_int_function(x,a,b,z,mu):
    part1=(x-a)*sqrt(2*z+mu**2)
    part2=(b-a)*sqrt(2*z+mu**2)
    # print(part1, part2)
    return sinh(part1)/sinh(part2)


if __name__ == '__main__':
    S=1
    L=1.2
    H=0.8
    sigma=0.4
    r=0.04
    mu=0

    result=irr_cal(S, L, H, sigma, r, mu)
    print(result)
