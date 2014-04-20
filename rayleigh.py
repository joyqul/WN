#!/usr/bin/env python
#-*- conding: utf-8-*-

import numpy as np
import matplotlib.pyplot as plt
import math
import random


def randn():
    return random.gauss(0, 1)
    
if __name__ == '__main__':
    N = 15 # Number of frequency samples
    M = 100000 # Number of time samples

    # Required parameters for INPUT: fm and row (r0)
    fm = 100
    r0 = 0.1

    y = 1
    Afd_p = 0 # Average fade duration; practical value
    Nr_p = 0 # Number of Zero-crossing level per second
    Rrms_p = 0 # Practically calculated R-rms value
    
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
        x = [ i / 10000.0 for i in xrange(len(R)) ]

        plt.axis([1, 10, -60, 20])
        plt.title('Rayleigh fading signal')
        plt.xlabel('Time Samples, s')
        plt.ylabel('Instantaneous Power dB')
        plt.plot(x, R)
        plt.show()

        y = y + 1

