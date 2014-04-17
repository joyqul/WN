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

def urban_path_loss(dis, alpha = 0.8, fc = 1000, hb = 30, hm = 1):
    # fc: carrier frequency (150 MHz to 1500 MHz) 
    # hb: effective BS antenna height(30m ~ 200m)
    # hm: effective MS antenna height(1m ~ 10m)
    # dis: distance (1m ~ 20km)
    # alpha: correction factor for the mobile antenna height
    return 69.55 + 26.16 * math.log(fc, 10) - 13.82 * math.log(hb, 10) - \
        alpha + (44.9 - 6.55 * math.log(hb, 10)) * math.log(dis, 10)

def large_cities_loss(dis, fc = 1000, hb = 30, hm = 1):
    alpha = (1.1 * math.log(fc, 10) - 0.7) * hm - (1.56 * math.log(fc, 10) - 0.8)
    return urban_path_loss(dis, alpha)

def medium_small_loss(dis, fc = 1000, hb = 30, hm = 1):
    if fc > 300:
        alpha = 8.29 * (math.log(1.54 * hm, 10))**2 - 1.1
    else:
        alpha = 3.2 * (math.log(11.75 * hm, 10))**2 - 4.97
    return urban_path_loss(dis, alpha)
def suburban_loss(dis, alpha = 0.8, fc = 1000, hb = 30, hm = 1):
    return urban_path_loss(dis) - 2 * (math.log(fc / 28, 10))**2 - 5.4

def open_loss(dis, alpha = 0.8, fc = 1000, hb = 30, hm = 1):
    return urban_path_loss(dis) - 4.78 * math.log(fc, 10)**2 - 18.33 * math.log(fc, 10) - 40.94
    
if __name__ == '__main__':
    """Set the control data"""
    # theta = E(r**2)
    theta = 1
    # Gt, transmitting antenna gain
    Gt = 1
    # Gr, receiving antenna gain
    Gr = 1
    # Pt, transmitting signal power
    # Pr, receiving signal power
    # Lp, path loss 
    # Ls, slow fading
    # Lf, fast fading
    # L, propagation loss
    # L = Lp * Ls * Lf
    # Pr = (Gt * Gr * Pt) / L

    """Plot"""
    x = np.linspace(0.001, 10, 100000)
    # y = [probability_density_function(i, theta) for i in x]
    y = [open_loss(i) for i in x]
    plt.axis([0, 10, 0, 200])
    plt.plot(x, y)
    plt.show()
    
