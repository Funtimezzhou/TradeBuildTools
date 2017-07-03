# !/usr/bin/python
# -*- coding: utf-8 -*-

import pandas_datareader.data as web
import fix_yahoo_finance
import matplotlib.pyplot as plt
import pandas as pd
import os
import bs4
import requests
import datetime

# obtain stock symbols from S&P 500
def obtain_parse_wiki_snp500():
    
    # Download and parse the Wikipedia list of S&P500 
    # constituents using requests and BeautifulSoup.

    # Returns a list of tuples for to add to MySQL.
    
    # Stores the current time, for the created_at record
    now = datetime.datetime.utcnow()

    # Use requests and BeautifulSoup to download the 
    # list of S&P500 companies and obtain the symbol table
    response = requests.get(
        "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    )
    soup = bs4.BeautifulSoup(response.text)

    # This selects the first table, using CSS Selector syntax
    # and then ignores the header row ([1:])
    symbolslist = soup.select('table')[0].select('tr')[1:]

    # Obtain the symbol information for each 
    # row in the S&P500 constituent table
    symbols = []
    for i, symbol in enumerate(symbolslist):
        tds = symbol.select('td')
        symbols.append(
            (
                tds[0].select('a')[0].text,  # Ticker
                'stock', 
                tds[1].select('a')[0].text,  # Name
                tds[3].text,  # Sector
                'USD', now, now
            ) 
        )
    return symbols

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
  

