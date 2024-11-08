import numpy as np
from matplotlib import pyplot as plt

from code.model.optimization import EuroOptimize


def plot_different_range_for_different_sigma():
    r = 0.05
    C = 0.2
    sigma_list = np.linspace(0.2,1,100)
    result = [EuroOptimize(r,C,sigma,bounds=(0.05,300)) for sigma in sigma_list]
    h_list = [i[0][0] for i in result]
    l_list = [i[0][1] for i in result]
    v_list = [i[1] for i in result]
    # print table about sigma,H,L
    for i,sigma in enumerate(sigma_list):
        print(f"sigma:{sigma}, H:{h_list[i]}, L:{l_list[i]}, V:{v_list[i]}")

    # two colum figure
    fig, ax = plt.subplots(2,1)
    ax[0].plot(sigma_list,h_list)
    ax[0].plot(sigma_list,l_list)
    #set as log scale,title,legend
    ax[0].set_yscale('log')
    ax[0].set_title('H and L vs sigma')
    ax[0].legend(['H','L'])

    ax[1].plot(sigma_list,v_list)

    #title at the bottom
    ax[1].set_title('V vs sigma')



    #show
    plt.show()


def print_for_AME():
    r = 0.1
    C = 0.2
    sigma_list = np.linspace(0.2,1,40)




if __name__ == '__main__':
    plot_different_range_for_different_sigma()