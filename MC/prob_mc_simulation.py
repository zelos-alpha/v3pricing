#standard brownian motion pathes
import numpy as np
def standard_brownian_motion(T, N, M):
    """
    Generates standard Brownian motion paths.
    Parameters:
    T (float): Total time.
    N (int): Number of time steps.
    M (int): Number of paths.
    Returns:
    numpy.ndarray: A 2D array of shape (M, N) representing the Brownian motion paths.
    """

    dt = T / N  # Time increment
    dW = np.sqrt(dt) * np.random.randn(M, N)  # Increments of Brownian motion
    W = np.cumsum(dW, axis=1)  # Cumulative sum to get the Brownian paths
    return W

# get first hitting time of a or b
def first_hitting_time(W, a, b):
    hit_index = np.argmax((W < a) | (W > b), axis=1)
    N = W.shape[1]
    hit_index[hit_index == 0] = N
    first_hitting_times = hit_index / N
    return first_hitting_times


import numpy as np


def hit_index(W, a, b):
    hit_a = W < a
    hit_b = W > b

    first_hit_a = np.argmax(hit_a, axis=1)
    first_hit_b = np.argmax(hit_b, axis=1)
    # if never hit, set the index to N
    first_hit_a[first_hit_a == 0] = W.shape[1]
    first_hit_b[first_hit_b == 0] = W.shape[1]
    hits_a_first = (first_hit_a < first_hit_b)
    hits_b_first = (first_hit_b < first_hit_a)
    does_not_hit = ~hits_a_first & ~hits_b_first

    first_hits_a_indices = np.where(hits_a_first)[0].tolist()
    first_hits_b_indices = np.where(hits_b_first)[0].tolist()
    does_not_hit_indices = np.where(does_not_hit)[0].tolist()

    return first_hits_a_indices, first_hits_b_indices, does_not_hit_indices

def compare_prob_hit_a(T, N, M, a, b):
    W=standard_brownian_motion(T, N, M)
    first_hits_a_indices, first_hits_b_indices, does_not_hit_indices = hit_index(W, a, b)
    hitting_times = first_hitting_time(W, a, b)

    bins = 10
    time_group = np.linspace(0, T, bins+1)
    # path index for its hitting time in different group
    path_index = np.digitize(hitting_times, time_group)

    # calculate the probability of hitting a for different group
    for i in range(bins):
        path_index_i = np.where(path_index == i)[0]
        # we got first_hits_a_indices already,we use it to get path_index that hit a first
        hit_a_index = np.intersect1d(path_index_i, first_hits_a_indices)
        hit_b_index = np.intersect1d(path_index_i, first_hits_b_indices)
        try:
            prob = len(hit_a_index) / len(path_index_i)
            print(f"group {i}  prob hitting a is {prob}, with {len(path_index_i)} paths")
            print("hit_a_index num is ", len(hit_a_index), "hit_b_index num is ", len(hit_b_index))
        except ZeroDivisionError:
            print(f"time from {time_group[i]} to {time_group[i+1]} is 0")




def lambda_liq(h,l):
    return 1/(2-np.sqrt(l)-(1/np.sqrt(h)))
def v3_h_value(h,l,l2):
    return lambda_liq(h,l)*(2*np.sqrt(l2)-np.sqrt(l)-(l2/np.sqrt(h)))
def v3_l_value(h,l,l1):
    return lambda_liq(h,l)*(2*np.sqrt(l1)-np.sqrt(l)-(l1/np.sqrt(h)))


def get_one_path_is_hit_a_and_time(a,b,dt):
    #generate one path step by step get it hits a or b
    current = 0
    t =0
    while True:
        t=t+1
        # current + random
        current += np.random.randn()*np.sqrt(dt)
        if current < a:
            return True, t*dt
        if current > b:
            return False,t*dt





def plot_path(path):
    import matplotlib.pyplot as plt
    plt.plot(path)
    plt.show()

if __name__ == "__main__":
    T = 1
    N = 1000
    M = 10000
    a = -0.2
    b = 0.8
    compare_prob_hit_a(T, N, M, a, b)
    print("done")