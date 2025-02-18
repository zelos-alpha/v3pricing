# MC
from code.model.inner_return_rate_cal import last_part_inf_series_value
from math import log
import numpy as np
import matplotlib.pyplot as plt


def brownian_motion(T=1, N=1000, mu=0, sigma=1):
    """
    生成布朗运动路径
    :param T: 总时间
    :param N: 时间步数
    :param mu: 漂移系数
    :param sigma: 波动率
    :return: 时间数组和布朗运动路径
    """
    dt = T / N  # 时间步长
    t = np.linspace(0, T, N)  # 时间数组
    dW = np.random.normal(0, np.sqrt(dt), N)  # 布朗运动增量
    W = np.cumsum(dW)  # 布朗运动路径
    return t, W


def stopping_time(t, W, a, b):
    """
    计算双边停时：首次触及下界 a 或上界 b 的时间
    :param t: 时间数组
    :param W: 标准布朗运动路径
    :param a: 下界
    :param b: 上界
    :return: 停时 tau, 停止时的值 W(tau), 停止类型（'a' 或 'b'）
    """
    for i in range(len(W)):
        if W[i] <= a:  # 触及下界 a
            return t[i]
        if W[i] >= b:  # 触及上界 b
            return t[i]
    return None  # 如果没有触及边界，返回 None


def average_inverse_stopping_time(a, b, num_paths=1000, T=1, N=1000):
    """
    计算多条路径的 1/tau 的平均值
    :param a: 下界
    :param b: 上界
    :param num_paths: 路径数量
    :param T: 总时间
    :param N: 时间步数
    :return: 1/tau 的平均值
    """
    inverse_tau_sum = 0  # 用于累加 1/tau
    valid_paths = 0  # 记录有效路径数量（触及边界的路径）

    for _ in range(num_paths):
        t, W = brownian_motion(T, N)  # 生成一条路径
        tau = stopping_time(t, W, a, b)  # 计算停时
        if tau is not None:  # 如果路径触及边界
            inverse_tau_sum += 1 / tau  # 累加 1/tau
            valid_paths += 1

    # 计算平均值
    if valid_paths > 0:
        average_inverse_tau = inverse_tau_sum / valid_paths
    else:
        average_inverse_tau = None  # 如果没有路径触及边界

    return average_inverse_tau


if __name__ == '__main__':
    S = 1
    H = 2
    L = 0.6
    C = 0.2
    r = 0.05
    mu = 0
    sigma = 0.7

    a = log(L)/sigma
    b = log(H)/sigma

    result1 = last_part_inf_series_value(a, b, mu)
    result2 = average_inverse_stopping_time(a, b)
    print(result1)
    print(result2)
