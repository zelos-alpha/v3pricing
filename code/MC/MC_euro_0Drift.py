import numpy as np

from MC.prob_mc_simulation import get_one_path_is_hit_a_and_time, v3_l_value, v3_h_value
from UniV3StoppingTimePricingEuro_with_optimization import uni_v3_pricing_euroexcu_version_analytic_solution_optimize, \
    uni_v3_pricing_euroexcu_version_analytic_solution
import matplotlib.pyplot as plt
# fix matplotlib on mac
import matplotlib
matplotlib.use('TkAgg')
from numpy import exp, sqrt, log as ln


def one_path_value(h, l, c, r, sigma,dt=0.0001):
    hit_a,t= get_one_path_is_hit_a_and_time(ln(l)/sigma,ln(h)/sigma,dt)
    if hit_a:
        return v3_l_value(h,l)*exp(-r*t)+t*c*exp(-r*t)
    else:
        return v3_h_value(h,l)*exp(-r*t)+t*c*exp(-r*t)


def one_path_lp_value(h, l, r, sigma,dt=0.0001):
    hit_a, t = get_one_path_is_hit_a_and_time(ln(l) / sigma, ln(h) / sigma, dt)
    if hit_a:
        return v3_l_value(h, l) * exp(-r * t)
    else:
        return v3_h_value(h, l) * exp(-r * t)

def one_path_stop_time_value(h, l, sigma,dt=0.0001):
    hit_a, t = get_one_path_is_hit_a_and_time(ln(l) / sigma, ln(h) / sigma, dt)
    return t



def one_path_mc_demo():
    r = 0.04
    C = 0.03
    sigma = 0.4
    result = uni_v3_pricing_euroexcu_version_analytic_solution_optimize(r, C, sigma)
    h,l = result[0]
    v= result[1]
    print(f"the pricing input is C = {C}, r = {r}, sigma = {sigma}")
    print(f"the optimal h,l,v is {h},{l},{v}")

    # test one path simulation
    print(one_path_value(h, l, C, r, sigma))


def verify_v_by_mc(r, C, sigma, h, l, N,dt):
    values = np.array([one_path_value( h, l, C, r, sigma,dt) for _ in range(N)])
    return np.mean(values)



def plot_hist():
    r = 0.04
    C = 0.03
    sigma = 0.4
    N = 100
    h,l = 1.2,0.8
    v =  uni_v3_pricing_euroexcu_version_analytic_solution(h, l, r, C, sigma)

    dt =1/3000
    v_values = [one_path_value( h, l, r, sigma,dt) for _ in range(N)]
    #print(v_values)
    plt.hist(v_values,bins=100)
    # plot the optimal v with label
    plt.axvline(v, color='r', linestyle='dashed', linewidth=1)
    # plot the mean value with label
    plt.axvline(np.mean(v_values), color='g', linestyle='dashed', linewidth=1)

    plt.legend(["optimal v","mean v"])
    #print the optimal v and mean v
    print(f"the optimal v is {v}")
    print(f"the mean v is {np.mean(v_values)}")

    # with r,c,sigma,h,l  on tilte
    plt.title(f"r={r},C={C},sigma={sigma},h={h},l={l}")
    plt.show()


def compare_dt():
    r = 0.04
    C = 0.03
    sigma = 0.4
    N = 100
    h,l = 1.1,0.9
    v =  uni_v3_pricing_euroexcu_version_lp(h, l, r, C, sigma)
    #print v
    print(f"the optimal v is {v}")

    dt =1/300
    v_values = [one_path_value( h, l, r,C, sigma,dt) for _ in range(N)]
    print(f"the dt is {dt}, the mean v is {np.mean(v_values)}")

    dt =1/3000
    v_values = [one_path_value( h, l, r,C, sigma,dt) for _ in range(N)]
    print(f"the dt is {dt}, the mean v is {np.mean(v_values)}")

    dt =1/300000
    v_values = [one_path_value( h, l, r,C, sigma,dt) for _ in range(N)]
    print(f"the dt is {dt}, the mean v is {np.mean(v_values)}")

    dt =1/3000000
    v_values = [one_path_value( h, l, r,C, sigma,dt) for _ in range(N)]
    print(f"the dt is {dt}, the mean v is {np.mean(v_values)}")


    #

def verify_stop_Time_for_different_dt():
    r = 0.04
    C = 0.03
    sigma = 0.4
    N = 1000
    h,l = 1.2,0.8

    a = ln(l)/sigma
    b = ln(h)/sigma
    expect_exit_time = -a*b
    print(f"the expect exit time is {expect_exit_time}")

    dt =1/300
    stop_time = [one_path_stop_time_value( h, l, sigma,dt) for _ in range(N)]
    print(f"the dt is {dt}, the mean stop time is {np.mean(stop_time)}")

    dt =1/3000
    stop_time = [one_path_stop_time_value( h, l, sigma,dt) for _ in range(N)]
    print(f"the dt is {dt}, the mean stop time is {np.mean(stop_time)}")

    dt =1/10000
    stop_time = [one_path_stop_time_value( h, l, sigma,dt) for _ in range(N)]
    print(f"the dt is {dt}, the mean stop time is {np.mean(stop_time)}")

    dt =1/300000
    stop_time = [one_path_stop_time_value( h, l, sigma,dt) for _ in range(N)]
    print(f"the dt is {dt}, the mean stop time is {np.mean(stop_time)}")






if __name__ == "__main__":
    #plot_hist()
    # compare_dt()
    #verify_stop_Time()
    #one_path_mc_demo()
    r = 0.04
    C = 0.03
    sigma = 0.4
    N = 1000
    h, l = 1.2, 0.8

    v = uni_v3_pricing_euroexcu_version_analytic_solution(h, l, r, C, sigma)
    print(f"the pricing input is C = {C}, r = {r}, sigma = {sigma}")


    result = verify_v_by_mc(r, C, sigma, h, l, N,1/1000)
    print(f"the MC value is {result}")
    print(f"the optimal v is {v}")