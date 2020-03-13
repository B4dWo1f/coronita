#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import datetime as dt
from urllib.request import urlretrieve
from urllib.error import HTTPError
import os
here = os.path.dirname(os.path.realpath(__file__))


def get_data(fname=f'{here}/covid.xls'):
   """
   Download data if needed and read file. Original data from the EU:
   https://data.europa.eu/euodp/es/data/dataset/covid-19-coronavirus-data
   """
   for cont in range(3):
      now = dt.datetime.now() - dt.timedelta(days=cont)
      year = now.year
      month = now.month
      day = now.day

      url = 'https://www.ecdc.europa.eu/sites/default/files/documents/'
      url +=  'COVID-19-geographic-disbtribution-worldwide-'
      url += f'{year}-{month:02d}-{day:02d}.xls'

      print(f'Trying to download data from:\n{url}')
      try: 
         fname,stat = urlretrieve(url, fname)
         print('Succeeded!!')
         break
      except HTTPError:
         print('Unsuccessful. Trying one day before')
   resp = os.popen(f'file {fname}').read()
   created = None
   for l in resp.split(','):
      l = l.strip()
      if l.startswith('Create Time/Date:'):
         l = l.replace('Create Time/Date: ','')
         created = dt.datetime.strptime(l,'%a %b %d %H:%M:%S %Y')
   return created
