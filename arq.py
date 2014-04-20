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

