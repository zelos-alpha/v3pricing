import numpy as np
from scipy.integrate import quad
from math import log, sqrt, sinh, cosh, exp, pi
from code.model.UniV3StoppingTimePricingGen import uni_v3_pricing_euroexcu_gbm_version_analytic_general_solution
# irr的cal计算成功，指没出bug，但是数值是负值，带之后review


# 用无穷级数展开代替quad，实验结果
def irr_cal(S, L, H, sigma, C, r, mu):
    para_a=log(L)/sigma
    para_b=log(H)/sigma
    para_x=log(S)/sigma
    # print(L, H, para_a, para_b)
    lambda_para = 1 / (2 - sqrt(L) - (1 / sqrt(H)))
    lower_bound_lp_part=lambda_para*L*(1/sqrt(L)-1/sqrt(H))*exp(mu*(para_a-para_x))*lower_bound_inf_series_value(para_x, para_a, para_b, r, mu)
    upper_bound_lp_part=lambda_para*(sqrt(H)-sqrt(L)*exp(mu*(para_b-para_x))*upper_bound_inf_series_value(para_x, para_a, para_b, r, mu))
    fee_part=C*cosh((para_b+para_a)*sqrt(2*r+mu**2)/2)/cosh((para_b-para_x)*sqrt(2*r+mu**2)/2)
    last_part=last_part_inf_series_value(para_a, para_b, mu)
    return lower_bound_lp_part+upper_bound_lp_part+fee_part-last_part


# 由于quad函数会遇到浮点数溢出故障，即math range error，所以现在试验一下是否能够用级数展开，来近似计算结果
def lower_bound_inf_series_value(x, a, b, r, mu, count_num=1000):
    n=np.arange(0, count_num)
    terms1=np.exp((a-x-2*n*(b-a))*sqrt(2*r+mu**2))*((a-x-2*n*(b-a))*sqrt(2*r+mu**2)-1)/((a-x-2*n*(b-a))**2)
    terms2=np.exp(-(2*b-a-x+2*n*(b-a))*sqrt(2*r+mu**2))*((2*b-a-x+2*n*(b-a))*sqrt(2*r+mu**2)+1)/((2*b-a-x+2*n*(b-a))**2)
    terms=-(terms1+terms2)
    series_sum=np.sum(terms)
    return series_sum

# 对上限无穷积分进行展开的函数
def upper_bound_inf_series_value(x, a, b, r, mu, count_num=1000):
    n=np.arange(0, count_num)
    terms1=np.exp((x-b-2*n*(b-a))*sqrt(2*r+mu**2))*((x-b-2*n*(b-a))*sqrt(2*r+mu**2)-1)/((x-b-2*n*(b-a))**2)
    terms2=np.exp(-(b-2*a+x+2*n*(b-a))*sqrt(2*r+mu**2))*((b-2*a+x+2*n*(b-a))*sqrt(2*r+mu**2)+1)/((b-2*a+x+2*n*(b-a))**2)
    terms=-(terms1+terms2)
    series_sum=np.sum(terms)
    return series_sum


# 对1/tau的期望的解析式的展开形式
def last_part_inf_series_value(a, b, mu, count_num=1000):
    n=np.arange(0, count_num)
    terms1=((-1)**(n+1))*(np.exp((a-n*(b-a))*mu)*((a-n*(b-a))*mu-1))/((a-n*(b-a))**2)
    terms2=((-1)**(n+1))*(np.exp(-(b+n*(b-a))*mu)*((b+n*(b-a))*mu+1))/((b+n*(b-a))**2)
    terms=terms1-terms2
    series_sum=np.sum(terms)
    return series_sum


if __name__ == '__main__':
    # S=1
    # L=0.8
    # H=1.2
    # sigma=0.7
    # C=0.2
    # r=0.04
    # mu=0
    #
    # x=0
    # a=log(L)/sigma
    # b=log(H)/sigma
    # result=upper_bound_inf_int_value(x,a,b,r,mu)
    # result2=upper_bound_inf_series_value(x, a, b, r, mu)

    # pv_result = uni_v3_pricing_euroexcu_gbm_version_analytic_general_solution(S, H, L, r, mu, C, sigma)
    # result=irr_cal(S, L, H, sigma, C, r, mu)
    # print(pv_result)
    # print(result)
    # S = 1
    # H = 1.05
    # L = 0.01
    # C = 0.2
    # r = 0.05
    # mu = 0
    # sigma = 0.7
    #
    # x=0
    # a=log(L)/sigma
    # b=log(H)/sigma
    # # result=lower_bound_inf_int_value(x,a,b,r,mu)
    # # result2=lower_bound_inf_series_value(x, a, b, r, mu)
    # # result=irr_cal(S, L, H, sigma, C, r, mu)
    # result2=upper_bound_inf_series_value(x, a, b, r, mu)
    # # print(result)
    # print(result2)

    S = 1
    H = 2
    L = 0.6
    C = 0.2
    r = 0.05
    mu = 0
    sigma = 0.7
    result = irr_cal(S, L, H, sigma, C, r, mu)
    pv_result = uni_v3_pricing_euroexcu_gbm_version_analytic_general_solution(S, H, L, r, mu, C, sigma)
    print(result)
    print(pv_result)
