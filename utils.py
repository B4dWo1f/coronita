#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import models
import numpy as np
import datetime as dt
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib.dates as mdates

def plot_top(df,fig=None,ax=None,threshold=500):
   """
   Plot date for every country with more than threshold cases
   """
   if fig==None or ax == None: fig, ax = plt.subplots()
   for c in df['CountryExp'].unique():
      aux = df[df['CountryExp']==c].sort_values(by='DateRep')
      Y = np.cumsum(aux['NewConfCases'])
      if np.max(Y) > threshold and not c.startswith('Cases'):
         ax.plot(aux['DateRep'], np.cumsum(aux['NewConfCases']), lw=3,label=c)
   ax.legend()
   ax.set_ylim(ymin=-1)


def fit_and_plot(X,Y,N,start=None,label='',C='',fig=None,ax=None):
   """
   X: numerical days from start date
   Y: number of cumulative cases
   N: total number of days to forecast (from min(X) to max(X)+N)
   start: if provided, it will be considered as the starting date
   C: Color for the plot
   """
   if fig==None or ax == None: fig, ax = plt.subplots()
   # Fit sigmoid
   popt, pcov = curve_fit(models.sigmoid, X,Y,maxfev = 8000)
   # future dates
   Xn = np.array(range(int(max(X)+N)))
   y = models.sigmoid(Xn,*popt)
   # Prepare plots
   if start != None:
      x = np.array([start + dt.timedelta(days=int(i)) for i in X])
      x_forecast = np.array([start + dt.timedelta(days=int(i)) for i in Xn])
   else:
      x = X
      x_forecast = Xn
   if len(label) > 0: label += f':  {int(np.max(y))}'
   ax.plot(x, Y, f'{C}', lw=3,label=label)
   ax.plot(x_forecast, y, f'{C}--', alpha=0.8)
