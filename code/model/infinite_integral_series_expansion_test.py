# 这个脚本的目的是为了将inner_return_rate_cal脚本中
# 涉及到的无穷积分，及其级数展开进行检验
# 无穷积分本身使用quad进行计算，但是会遇到浮点数溢出故障
# 级数展开为手动推导后得到的解析公式
# 现在将比较两种算法之间的数值差异
# 如果数值极为接近，则改用级数展开算法进行计算
# 2025年2月6日更新
# 此测试脚本对于irr整体解析式中的上下限积分部分进行了quad积分与级数展开解析式的数值比较
# 测试成功，级数展开解析式可以代替quad积分
# 对于1/tau的期望的级数展开解析式的测试检验，在其他文件进行
import numpy as np
from scipy.integrate import quad
from math import log, sqrt, sinh, cosh, exp, pi


def lower_bound_inf_int_function(x,a,b,z,mu):
    part1=(b-x)*sqrt(2*z+mu**2)
    part2=(b-a)*sqrt(2*z+mu**2)
    return sinh(part1)/sinh(part2)


def lower_bound_inf_int_value(x, a, b, r, mu):
    value, error = quad(lambda z:lower_bound_inf_int_function(x, a, b, z, mu), r, np.inf)
    return value


def upper_bound_inf_int_value(x,a,b,r,mu):
    try:
        value, error = quad(lambda z:upper_bound_int_int_function(x,a,b,z,mu), r, np.inf)
    except:
        value=0
    return value


def upper_bound_int_int_function(x,a,b,z,mu):
    part1=(x-a)*sqrt(2*z+mu**2)
    part2=(b-a)*sqrt(2*z+mu**2)
    # print(part1, part2)
    return sinh(part1)/sinh(part2)


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


# 定义绝对误差
def absolute_error(result1, result2):
    return np.abs(result1-result2)


# 定义相对误差
def relative_error(result1, result2):
    return np.abs((result1-result2)/result1)


# 通用测试函数
def compare_algorithms(algorithm_pair, test_inputs_1, test_inputs_2, fixed_params):
    algo1, algo2 = algorithm_pair
    x, r, mu = fixed_params
    for a in test_inputs_1:
        for b in test_inputs_2:
            # 调用两种算法
            result1 = algo1(x, a, b, r, mu)
            result2 = algo2(x, a, b, r, mu)

            # 计算误差
            abs_err = absolute_error(result1, result2)
            rel_err = relative_error(result1, result2)

            # 输出结果
            print(f"Input: a = {a}, b = {b}")
            print(f"{algo1.__name__} Result: {result1}")
            print(f"{algo2.__name__} Result: {result2}")
            print(f"Absolute Error: {abs_err}")
            print(f"Relative Error: {rel_err}")
            print("-" * 40)


if __name__ == '__main__':
    # S=1
    # sigma=0.4
    # C=0.2
    # r=0.04
    # mu=0
    # # 生成测试数据
    # test_inputs_a = np.linspace(log(0.01)/sigma, log(0.93)/sigma, 50)
    # test_inputs_b = np.linspace(log(1.05)/sigma, log(5)/sigma, 50)
    #
    # # 定义固定参数
    # fixed_params = (0, r, mu)  # a=1, b=2, c=3
    #
    # # 定义需要比较的算法对
    # algorithm_pairs = [
    #     (lower_bound_inf_int_value, lower_bound_inf_series_value),  # 比较算法 1 和算法 2
    # ]
    #
    # for pair in algorithm_pairs:
    #     print(f"Comparing {pair[0].__name__} and {pair[1].__name__}:")
    #     compare_algorithms(pair, test_inputs_a, test_inputs_b, fixed_params)
    #     print("\n" + "=" * 60 + "\n")
    # =================================================
    # 以上实验证明了下限积分的级数展开的有效性，虽然跑到一定程度，test中断了，原因是无穷积分算法的效果不足，但是级数展开算法性能依旧强劲
    S=1
    sigma=0.4
    C=0.2
    r=0.04
    mu=0
    # 生成测试数据
    test_inputs_a = np.linspace(log(0.01)/sigma, log(0.93)/sigma, 50)
    test_inputs_b = np.linspace(log(1.01)/sigma, log(5)/sigma, 50)

    # 定义固定参数
    fixed_params = (0, r, mu)  # a=1, b=2, c=3

    # 定义需要比较的算法对
    algorithm_pairs = [
        (upper_bound_inf_int_value, upper_bound_inf_series_value),
        (lower_bound_inf_int_value, lower_bound_inf_series_value)# 比较算法 1 和算法 2
    ]

    for pair in algorithm_pairs:
        print(f"Comparing {pair[0].__name__} and {pair[1].__name__}:")
        compare_algorithms(pair, test_inputs_a, test_inputs_b, fixed_params)
        print("\n" + "=" * 60 + "\n")
