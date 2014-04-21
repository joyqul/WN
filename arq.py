#!/usr/bin/env python
#-*- conding: utf-8-*-

import numpy as np
import matplotlib.pyplot as plt
import math
import random

def t_go_back_n(n, pb, N):
    pack = (1 - pb) ** n
    return 1 + N * (1 - pack) / pack
    
def go_back_n(pb, n, k, N, rb, packet, d, D_nack):
    frame_time = t_go_back_n(n, pb, N)
    total_time = frame_time + (d / D_nack) / N
#print (d / D_nack) / N, (1 - ( 1 - pb) ** n ) * packet * D_nack / N
    return k / total_time

def t_selective_repeat(n, pb):
    pack = (1 - pb) ** n
    return 1 / pack

def selective_repeat(pb, n, k, d, D_nack):
    frame_time = t_selective_repeat(n, pb)
    total_time = frame_time #+ (1 - ( 1 - pb) ** n ) * packet * D_nack * 8
    return k / total_time

if __name__ == '__main__':
    """Control data"""
    n = float(1500) * 8 # code rate = 1/3
    k = n / 3
    d = 0.00001
    rb = 10**7
    packet = rb / n
    pb = 0.0000001
    D_nack = n / rb
    
    """
    # first part figure
    x = [ i for i in xrange(1, 11) ]
    y = [ go_back_n(pb, n, k, i, rb, packet, d, D_nack) for i in xrange(1, 11) ]
    plt.xlabel('Value of N')
    plt.ylabel('Throughput (bits per second)')
    plt.plot(x, y)
    plt.grid()
    plt.show()


    """
    # second part figure
    st_ber = 0.0000001
    ed_ber = 0.001
    point_num = 10000
    x = np.linspace(st_ber, ed_ber, point_num)
    
    y1 = [ selective_repeat(i, n, k, d, D_nack) for i in x ]
    y2 = [ go_back_n(i, n, k, 3, rb, packet, d, D_nack) for i in x]
    
    plt.plot(x, y1, 'r', label = 'Selective Repeat')
    plt.plot(x, y2, 'g', label = 'Go back N, N = 3')
    plt.grid()
    plt.legend()
    plt.show()
