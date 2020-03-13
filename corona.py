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
download = True
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



# Plot results
fig, ax = plt.subplots()

if end == None: end = now

for cont,country in enumerate(countries):
   # Grab data for country
   aux = df[df['CountryExp']==country].sort_values(by='DateRep')
   # Select dates
   aux = aux.loc[aux['DateRep']>=start]
   aux = aux.loc[aux['DateRep']<=end]
   # Numerical dates (days since origin)
   dates = aux['DateRep']
   X = np.array([(x-start).total_seconds()/60/60/24 for x in aux['DateRep']])
   Y = np.cumsum(aux['NewConfCases'])
   label = f'{country}'
   label = label.replace('United States of America','USA') # lol
   utils.fit_and_plot(X,Y,Nforecast,start,label,f'C{cont%10}',fig,ax)


# Ax settings
ax.legend()
ax.xaxis.set_major_formatter(mdates.DateFormatter(fmt))
ax.set_ylim([0,8.5e4])
ax.set_xlabel('Date')
ax.set_ylabel('Total cases')
ax.set_title(f'Forecast done: {dt.datetime.now().date()}')

fig.tight_layout()
f_out = f"{here}/{dt.datetime.now().date().strftime('%Y_%m_%d')}.png"
print(f_out)
fig.savefig(f_out)
# plt.show()
