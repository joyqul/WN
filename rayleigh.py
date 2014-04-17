#!/usr/bin/env python
#-*- conding: utf-8-*-

import numpy as np
import matplotlib.pyplot as plt
import math

def stop_and_wait(pb, d, rb, n, k):
    return ((1 - pb)** n / (1 + d*rb / n)) * (k / n)
    
def go_back_n(pb, n, k, N):
    return ((1 - pb)**n / ((1 - pb)**n + N * (1 - (1 - pb)**n))) * (k / n)
    
def selective_repeat(pb, n, k):
    return (1 - pb) ** n * (k / n)

def probability_density_function(r, theta):
    theta = theta ** 2
    if theta == 0:
        return 0
    return (r / theta) * (math.e ** (- r**2 / (2 * theta)))
    
if __name__ == '__main__':
    """Set the control data"""
    # theta = E(r**2)
    theta = 1

    """Plot"""
    x = np.linspace(0, 10, 100000)
    y = [probability_density_function(i, theta) for i in x]
    plt.axis([0, 10, 0, 1])
    plt.plot(x, y)
    plt.show()
    
