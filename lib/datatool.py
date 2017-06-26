# !/usr/bin/python
# -*- coding: utf-8 -*-

import pandas_datareader.data as web
import fix_yahoo_finance
import matplotlib.pyplot as plt
import pandas as pd
import os

# get EOD data from google
def getdata_google(tickers,  start_date, end_date):
  # use pandas_reader.data.DataReader to load the history data
  try:
    goog_data = web.get_data_google(tickers,start_date,end_date)
    if 'Adj Close' not in goog_data.items:
      goog_data.loc['Adj Close',:,:] = goog_data['Close']
    status = True
  except:
    status = False
  return goog_data, status

# get EOD data from yahoo
def getdata_yahoo(tickers, start_date, end_date):
  try:
    yahoo_data = web.get_data_yahoo(tickers,start_date,end_date)
    if 'Adj Close' not in yahoo_data.items:
      yahoo_data.loc['Adj Close',:,:] = yahoo_data['Close']
    status = True
  except:
    status = False
  return yahoo_data, status
  
def savedatatocsv(panel_data,fpath):
  for ticker in panel_data.minor_axis:
    # save data to csv according to ticker name
    panel_data.minor_xs(ticker).to_csv(os.path.join(fpath, ticker + '.csv'))
  status = True
  return status
  

