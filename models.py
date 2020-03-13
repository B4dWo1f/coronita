#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import numpy as np

def sigmoid(x,a,b,c):   
   return a/(1+np.exp(-x*b+c))
