# 此脚本用于进行开仓，平仓时的ETH交易金额计算
import numpy as np


def Euro_Pricing_Penalty_Term_Value_0drift_Version(L, H, r, k, sigma):
    para_a=np.log(L)/sigma
    para_b=np.log(H)/sigma
    lambda_para=1/(2-np.sqrt(L)-1/np.sqrt(H))
    part1=1-1/np.sqrt(H)
    part2_1=L*(1/np.sqrt(L)-1/np.sqrt(H))
    part2_2=np.sinh(para_b*np.sqrt(2*r))/np.sinh((para_b-para_a)*np.sqrt(2*r))
    result=k*lambda_para*(part1+part2_1*part2_2)
    return result


def Euro_Pricing_Penalty_Term_Value_GBM_Version(L, H, r, k, mu, sigma):
    para_a=np.log(L)/sigma
    para_b=np.log(H)/sigma
    lambda_para=1/(2-np.sqrt(L)-1/np.sqrt(H))
    part1=1-1/np.sqrt(H)
    part2_1=L*(1/np.sqrt(L)-1/np.sqrt(H))
    part2_2=np.sinh(para_b*np.sqrt(2*r+mu**2))/np.sinh((para_b-para_a)*np.sqrt(2*r+mu**2))
    result=k*lambda_para*(part1+part2_1*part2_2)
    return result


def Amer_Pricing_Penalty_Term_Value_0drift_Version(L, H, L1, L2, r, k, sigma):
    para_a=np.log(L1)/sigma
    para_b=np.log(L2)/sigma
    lambda_para=1/(2-np.sqrt(L)-1/np.sqrt(H))
    part1=1-1/np.sqrt(H)
    part2_1=L1*(1/np.sqrt(L1)-1/np.sqrt(H))
    part2_2=np.sinh(para_b*np.sqrt(2*r))/np.sinh((para_b-para_a)*np.sqrt(2*r))
    part3_1=L2*(1/np.sqrt(L2)-1/np.sqrt(H))
    part3_2=np.sinh(-para_a*np.sqrt(2*r))/np.sinh((para_b-para_a)*np.sqrt(2*r))
    result=k*lambda_para*(part1+part2_1*part2_2+part3_1*part3_2)
    return result


def Amer_Pricing_Penalty_Term_Value_GBM_Version(L, H, L1, L2, r, k, mu, sigma):
    para_a=np.log(L1)/sigma
    para_b=np.log(L2)/sigma
    lambda_para=1/(2-np.sqrt(L)-1/np.sqrt(H))
    part1=1-1/np.sqrt(H)
    part2_1=L1*(1/np.sqrt(L1)-1/np.sqrt(H))
    part2_2=np.sinh(para_b*np.sqrt(2*r+mu**2))/np.sinh((para_b-para_a)*np.sqrt(2*r+mu**2))
    part3_1=L2*(1/np.sqrt(L2)-1/np.sqrt(H))
    part3_2=np.sinh(-para_a*np.sqrt(2*r+mu**2))/np.sinh((para_b-para_a)*np.sqrt(2*r+mu**2))
    result=k*lambda_para*(part1+part2_1*part2_2+part3_1*part3_2)
    return result
