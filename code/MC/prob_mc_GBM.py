import numpy as np


def geometric_brownian_motion(S0, mu, sigma, T, N, M):
    """
    生成几何布朗运动路径

    参数:
    S0 (float): 初始价格
    mu (float): 漂移率
    sigma (float): 波动率
    T (float): 总时间
    N (int): 时间步数
    M (int): 路径数

    返回:
    numpy.ndarray: 价格路径
    """
    dt = T / N
    dW = np.sqrt(dt) * np.random.randn(M, N)

    # 初始化价格矩阵
    W = np.zeros((M, N + 1))
    W[:, 0] = np.log(S0)

    # 生成几何布朗运动路径（对数空间）
    for t in range(1, N + 1):
        W[:, t] = W[:, t - 1] + (mu - 0.5 * sigma ** 2) * dt + sigma * dW[:, t - 1]

    # 转换回价格空间
    return np.exp(W)


def first_hitting_time(W, a, b):
    """
    计算首次触及边界的时间

    参数:
    W (numpy.ndarray): 价格路径
    a (float): 下边界
    b (float): 上边界

    返回:
    numpy.ndarray: 首次触及边界的时间
    """
    hit_index = np.argmax((W < a) | (W > b), axis=1)
    N = W.shape[1]
    hit_index[hit_index == 0] = N
    first_hitting_times = hit_index / N
    return first_hitting_times


def hit_index(W, a, b):
    """
    分析路径首次触及边界的情况

    参数:
    W (numpy.ndarray): 价格路径
    a (float): 下边界
    b (float): 上边界

    返回:
    tuple: 首次触及a、b的路径索引和未触及的路径索引
    """
    hit_a = W < a
    hit_b = W > b

    first_hit_a = np.argmax(hit_a, axis=1)
    first_hit_b = np.argmax(hit_b, axis=1)

    # 如果未触及，设置索引为N
    first_hit_a[first_hit_a == 0] = W.shape[1]
    first_hit_b[first_hit_b == 0] = W.shape[1]

    hits_a_first = (first_hit_a < first_hit_b)
    hits_b_first = (first_hit_b < first_hit_a)
    does_not_hit = ~hits_a_first & ~hits_b_first

    first_hits_a_indices = np.where(hits_a_first)[0].tolist()
    first_hits_b_indices = np.where(hits_b_first)[0].tolist()
    does_not_hit_indices = np.where(does_not_hit)[0].tolist()

    return first_hits_a_indices, first_hits_b_indices, does_not_hit_indices


def compare_prob_hit_a(T, N, M, a, b, S0=100, mu=0.05, sigma=0.2):
    """
    比较不同时间段触及边界的概率

    参数:
    T (float): 总时间
    N (int): 时间步数
    M (int): 路径数
    a (float): 下边界
    b (float): 上边界
    S0 (float): 初始价格
    mu (float): 漂移率
    sigma (float): 波动率
    """
    # 使用GBM替代原始的标准布朗运动
    W = geometric_brownian_motion(S0, mu, sigma, T, N, M)

    first_hits_a_indices, first_hits_b_indices, does_not_hit_indices = hit_index(W, a, b)
    hitting_times = first_hitting_time(W, a, b)

    bins = 10
    time_group = np.linspace(0, T, bins + 1)
    # 路径索引按时间分组
    path_index = np.digitize(hitting_times, time_group)

    # 计算不同时间组的触及概率
    for i in range(bins):
        path_index_i = np.where(path_index == i)[0]
        # 获取触及下边界的路径索引
        hit_a_index = np.intersect1d(path_index_i, first_hits_a_indices)
        hit_b_index = np.intersect1d(path_index_i, first_hits_b_indices)

        try:
            prob = len(hit_a_index) / len(path_index_i)
            print(f"group {i}  prob hitting a is {prob}, with {len(path_index_i)} paths")
            print("hit_a_index num is ", len(hit_a_index), "hit_b_index num is ", len(hit_b_index))
        except ZeroDivisionError:
            print(f"time from {time_group[i]} to {time_group[i + 1]} is 0")


# 保留原有的辅助函数
def lambda_liq(h, l):
    return 1 / (2 - np.sqrt(l) - (1 / np.sqrt(h)))


def v3_h_value(h, l, l2):
    return lambda_liq(h, l) * (2 * np.sqrt(l2) - np.sqrt(l) - (l2 / np.sqrt(h)))


def v3_l_value(h, l, l1):
    return lambda_liq(h, l) * (2 * np.sqrt(l1) - np.sqrt(l) - (l1 / np.sqrt(h)))


def get_one_path_is_hit_a_and_time(S0, mu, sigma, a, b, dt):
    """
    模拟单条GBM路径，直到触及边界

    参数:
    S0 (float): 初始价格
    mu (float): 漂移率
    sigma (float): 波动率
    a (float): 下边界
    b (float): 上边界
    dt (float): 时间步长

    返回:
    tuple: (是否触及下边界, 触及边界的时间)
    """
    current = S0
    t = 0

    while True:
        t += 1
        # GBM路径更新
        current *= np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * np.random.randn())

        # 检查是否触及边界
        if current < a:
            return True, t * dt
        if current > b:
            return False, t * dt


# 使用示例
if __name__ == "__main__":
    # 示例参数
    T = 1.0  # 总时间
    N = 252  # 时间步数
    M = 1000  # 路径数
    a = 90  # 下边界
    b = 110  # 上边界

    compare_prob_hit_a(T, N, M, a, b)
