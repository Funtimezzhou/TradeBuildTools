# !/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

# import system module
import pandas_datareader.data as web

import matplotlib.pyplot as plt
import pandas as pd
import bs4
import requests

# import user-defined module
import sys
sys.path.append('../lib')
import datatool



# """
# Part0 - Obtain ticker symbols from S&P 500
# """
# # Define the instruments to download. We would like to see Apple, Microsoft and the S&P500 index.
# symbols = datatool.obtain_parse_wiki_snp500()
# tickers = []  
# for i in range( len(symbols) ):
  # stock = symbols[i][0].encode("utf-8")
  # tickers.append( stock )
  

"""
Load data from webpage
"""
# Use requests and BeautifulSoup to download the 
    # list of S&P500 companies and obtain the symbol table
response = requests.get("https://www.marketbeat.com/ratings/USA/latest/")
soup = bs4.BeautifulSoup(response.text)

# This selects the first table, using CSS Selector syntax
    # and then ignores the header row ([1:])
symbolslist = soup.select('table')[0].select('tr')[1:]