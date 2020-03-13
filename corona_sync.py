#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
here = os.path.dirname(os.path.realpath(__file__))
# My libraries
import web
import models
import utils
# Standard
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib.dates as mdates
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


fname = f'{here}/covid.xls'
Ncountries = 10
Nforecast = 30
N0 = 10  # number of cases for common origin
download = False
start = dt.datetime(2020,1,1,0,0,0)
end = None
now = dt.datetime.now()
fmt = '%b %d'   # date format for plot


# Get data
if download:
   if web.get_data(fname) != None:
      df = pd.read_excel(fname)
   else:
      print('Error getting data')
      exit()
else:
   df = pd.read_excel(fname)


# Select countries
countries,cases = [],[]
for c in df['CountryExp'].unique():
   if c.startswith('Cases'): continue
   num = df[df['CountryExp'] == c]['NewConfCases'].sum()
   countries.append(c)
   cases.append(num)
inds = np.argsort(cases)
countries = np.array(countries)[inds[-Ncountries:]]
countries = list(reversed(countries))
countries = ['Spain','France','Germany','Italy','China']


fig, ax = plt.subplots()
start_dates = []
for i,country in enumerate(countries):
   # Grab data for country
   aux = df[df['CountryExp']==country].sort_values(by='DateRep')
   dates = aux['DateRep']
   Y = np.cumsum(aux['NewConfCases'])
   T0 = np.min(np.where(Y>=N0)[0])
   start_dates.append(T0)
   X = np.array([(x-dates.iloc[T0]).total_seconds()/60/60/24 for x in dates])
   # ax.plot(X,Y, 'o-', label=f'{country}')
   print(f'{country} day: {T0} ({Y.iloc[T0]})')
   utils.fit_and_plot(X,Y,Nforecast,None,country,f'C{i}',fig,ax)

ax.legend()
ax.set_xlim(xmin=-1)
ax.set_ylim([0,8.5e4])
ax.set_xlabel(f'Days since country reached {N0} cases')
ax.set_ylabel('Cumulative cases')
fig.tight_layout()
plt.show()
