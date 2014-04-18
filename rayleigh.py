#!/usr/bin/env python
#-*- conding: utf-8-*-

import numpy as np
import matplotlib.pyplot as plt
import math
import random

def stop_and_wait(pb, d, rb, n, k):
    return ((1 - pb)** n / (1 + d*rb / n)) * (k / n)
    
def go_back_n(pb, n, k, N):
    return ((1 - pb)**n / ((1 - pb)**n + N * (1 - (1 - pb)**n))) * (k / n)
    
def selective_repeat(pb, n, k):
    return (1 - pb) ** n * (k / n)


def randn():
    return random.gauss(0, 1)
    
if __name__ == '__main__':
    N = 256 # Number of frequency samples
    M = 8192 # Number of time samples

    # Required parameters for INPUT: fm and row (r0)
    fm = int(raw_input("ENTER THE VALUE OF fm [20 Hz, 200Hz]:"))
    r0 = float(raw_input("ENTER THE VALUE OF r0 [1,0.1,0.01]:"))

    y = 1
    Afd_p = 0 # Average fade duration; practical value
    Nr_p = 0 # Number of Zero-crossing level per second
    Rrms_p=0 # Practically calculated R-rms value
    
    while y <= 1:
        delta_f = 2 * fm / float(N) # Frequency resolution
        delta_t = float(N) / (M-1) /2 /fm # Time resolution

        """ If N = M-1, then the time resolution delta_t = 1 / 2 * fm, which may not be small so take M >> N. 
    When M > N, we need to pad with zero values before taking IFFT.  """

        X = [complex(randn(), randn()) for m in xrange(N/2 + 1)]
        Y = [complex(randn(), randn()) for m in xrange(N/2 + 1)]

        X[0] = 0
        Y[0] = 0

        for i in xrange(N/2 + 1, M - N/2 - 1):
            X.append(0)
            Y.append(0)

        for m in xrange(M - N/2 - 1, M):
            X.append(X[M - m].conjugate())
            Y.append(Y[M - m].conjugate())


        # Sample Se(f) Spectrum
        SeF = [1.5 / (math.pi * fm * (math.sqrt(1 - ( (i - 1) * float(delta_f) / fm )**2))) for i in xrange(N/2)]

        # Calculating Edge Value by extending the slope prior to passband edge to edge
        SeF.append(SeF[N/2 -1] * 2 - SeF[(N/2 - 1) - 1])
        
        for i in xrange(N/2 + 1, M - N/2):
            SeF.append(0)

        for m in xrange(M - N/2, M):
            SeF.append(SeF[M - m])
    
        X_shaped = [ X[m] * math.sqrt(SeF[m]) for m in xrange(M) ]
        Y_shaped = [ Y[m] * math.sqrt(SeF[m]) for m in xrange(M) ]

        X_shaped = np.fft.ifft(X_shaped)
        Y_shaped = np.fft.ifft(Y_shaped)
        X_component = [ m.real for m in X_shaped ]
        Y_component = [ m.real for m in Y_shaped ]

        #************* Find R-rms value and envelope of Rayleigh Distribution ***********%

        R = [math.sqrt(X_component[m]** 2 + Y_component[m]**2) for m in xrange(M)]
        r = [20 * math.log(m, 10) if m!=0 else 0 for m in R]

        rms = math.sqrt(sum(m**2 for m in R)/len(R))
        Rrms = 20 * math.log(rms, 10)
        level = 20 * math.log(r0*rms, 10)

        R = [ m - Rrms for m in r]

        plt.axis([1, 8192, -60, 20])
        plt.plot(R)
        plt.show()

        # Calculating (Practically) Number of Zero Level Crossing and Average Fade Duration

        h = 0
        c = 0
        C1 = 0
        NUM = 0

        while h <= M-1:
            if r[h] <= level:
                i = h
                while i <= M-1:
                    if r[i] >= level:
                        NUM = NUM + 1
                        break
                    i = i + 1

                c = i - h
                C1 = C1 + c
                h = i - 1

            h = h + 1
        
        Afd_p = Afd_p + (C1/NUM) * delta_t
        Nr_p = Nr_p + NUM * delta_f
        Rrms_p = Rrms_p + Rrms

        y = y + 1

    # ************ Theoretical calculation of Number of Zero Level Crossing (Nr) and Average Fade Duration ************* %

    Nr_theoretical = math.sqrt(2 * math.pi) * fm * r0 *math.exp(-r0**2)
    
    z1 = math.exp(r0**2) - 1
    z2 = r0 * fm * math.sqrt(2 * math.pi)
    Average_fade_duration_theoretical = z1 / z2

    rowdb = 10 * math.log(r0, 10)
    Rrms_theoretical = Rrms + rowdb
    print Average_fade_duration_theoretical, Afd_p
    
    values = plt.plot(np.random.rayleigh(3, 1000))
    meanvalue = 1
    modevalue = np.sqrt(2 / np.pi) * meanvalue
    s = np.random.rayleigh(modevalue, 1000000)
    
    
