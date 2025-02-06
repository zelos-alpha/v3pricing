# 此脚本将要对E(1/tau)进行进行数值检验，检测级数展开解析式的有效性
# 一方面，E(1/tau)是对两个cosh的除法进行从0到正无穷的积分
# 另一方面，经过手动推导得到了他的几何级数展开式
# 现检验，2者在数值上是否有差异
import numpy as np
from scipy.integrate import quad
from math import log, sqrt, sinh, cosh, exp, pi


# 此函数为quad形式积分的被积函数形式
def target_function(a, b, r, mu):
    part1=cosh((b+a)*sqrt(2*r+mu**2)/2)
    part2=cosh((b-a)*sqrt(2*r+mu**2)/2)
    return part1/part2


# 对于target_function进行quad积分
def function1(a, b, mu):
    try:
        value, error = quad(lambda z:target_function(a, b, z, mu), 0, np.inf)
    except:
        value=0
    return value


# 这个是对于E(1/tau)的形式进行级数展开得到的解析式
def function2(a, b, mu, count_num=1000):
    n=np.arange(0, count_num)
    terms1=((-1)**(n+1))*(np.exp((a-n*(b-a))*mu)*((a-n*(b-a))*mu-1))/((a-n*(b-a))**2)
    terms2=((-1)**(n+1))*(np.exp(-(b+n*(b-a))*mu)*((b+n*(b-a))*mu+1))/((b+n*(b-a))**2)
    terms=terms1-terms2
    series_sum=np.sum(terms)
    return series_sum


# 定义绝对误差
def absolute_error(result1, result2):
    return np.abs(result1-result2)


# 定义相对误差
def relative_error(result1, result2):
    return np.abs((result1-result2)/result1)


# 测试函数
def compare_algo(algorithm_pair, test_inputs_1, test_inputs_2, fixed_params):
    algo1, algo2 = algorithm_pair
    mu = fixed_params
    for a in test_inputs_1:
        for b in test_inputs_2:
            # 调用两种算法
            result1 = algo1(a, b, mu)
            result2 = algo2(a, b, mu)

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
    sigma=0.4
    mu=0
    # 生成测试数据
    test_inputs_a = np.linspace(log(0.01)/sigma, log(0.93)/sigma, 50)
    test_inputs_b = np.linspace(log(1.01)/sigma, log(5)/sigma, 50)

    algorithm_pairs = [
        (function1, function2),  # 比较算法 1 和算法 2
    ]

    print(f"Comparing {function1.__name__} and {function2.__name__}:")
    compare_algo(algorithm_pairs[0], test_inputs_a, test_inputs_b, mu)
    print("\n" + "=" * 60 + "\n")
    # 测试成功，在quad，即function1能成功抛出结果的情况下，二者误差小于1e-8
