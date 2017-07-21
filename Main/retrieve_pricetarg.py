# !/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

# import system module
import pandas_datareader.data as web
import fix_yahoo_finance
import matplotlib.pyplot as plt
import pandas as pd
import bs4
import requests
from finsymbols import symbols

# import user-defined module
import sys
sys.path.append('../lib')
import datatool

targetdate = '2017-07-20'
marketdate = '2017-07-20'

"""
Obtain ticker symbols from S&P 500
"""
# Define the instruments to download. We would like to see Apple, Microsoft and the S&P500 index.
sp500  = symbols.get_sp500_symbols()
tickers = []  
for i in range( len(sp500) ):
  stock = sp500[i]['symbol'].encode("utf-8")
  tickers.append( stock )
  
usenasdaq = True
if usenasdaq: 
  nasdaq = symbols.get_nasdaq_symbols()
  for i in range( len(nasdaq) ):
    stock = nasdaq[i]['symbol'].encode("utf-8")
    tickers.append( stock )
  tickers = list( set(tickers) )
  
usenyse = True
if usenyse:
  nyse = symbols.get_nyse_symbols()
  for i in range(len(nyse)):
    stock = nyse[i]['symbol'].encode("utf-8")
    tickers.append(stock)
  tickers = list( set(tickers) )

"""
Load Analyst ratings from webpage
"""
print('****************Download Analyst Ratings******************')
# Use requests and BeautifulSoup to download the 
    # list of S&P500 companies and obtain the symbol table
response = requests.get('https://www.marketbeat.com/ratings/USA/' + targetdate + '/')
soup = bs4.BeautifulSoup(response.text,'lxml')

# This selects the first table, using CSS Selector syntax
    # and then ignores the header row ([1:])
head  = soup.select('table')[0].select('tr')[0]
table = soup.select('table')[0].select('tr')[1:]

AnalystRes = {}
for i, tab in enumerate(table):
   # Get row data for each brokerage
   Brokerage = tab.select('td')[0].text.encode('utf-8')
   # Get action where target is raised or dropped
   Action    = tab.select('td')[2].text.encode('utf-8')
   # Get company name and stock code
   Company   = tab.select('td')[3].text.encode('utf-8')
   CompanyName   = Company.split('(')[0]
   StockName     = Company.split('(')[1].split(')')[0]
   # Get ratings: buy, sell, hold 
   Rating    = tab.select('td')[4].text.encode('utf-8')
   if Rating.find('->') >= 0:
     Rating_from = Rating.split('->')[0]
     Rating_to   = Rating.split('->')[1]
   else:
     Rating_from = ''
     Rating_to   = Rating
   # Get Target Price
   PriceTarg = tab.select('td')[5].text.encode('utf-8')
   if PriceTarg.find('->') >= 0:
     PriceTarg_from = PriceTarg.split('->')[0]
     PriceTarg_to   = PriceTarg.split('->')[1]
   else:
     PriceTarg_from = ''
     PriceTarg_to   = PriceTarg
   # Get impact on share price: low, medium
   Impact    = tab.select('td')[6].text.encode('utf-8')
   
   # Store data in dictionary
   if StockName not in AnalystRes.keys():
     AnalystRes[StockName]={}
   val = [(Action, Rating_from, Rating_to, PriceTarg_from, PriceTarg_to, Impact)]
   label = ['Action','Rating_from','Rating_to','PriceTarg_from','PriceTarg_to','Impact']
   index = [(targetdate)]
   AnalystRes[StockName][Brokerage] = pd.DataFrame(data = val, columns = label, index = index)
print('Analyst Rating Sucessfully Loaded!\n')



"""
Load Daily Data from Google and Yahoo
"""
print('****************Retrieve Stock Data******************')
stocklist = []
for stock in tickers:
  if stock in AnalystRes.keys():
    stocklist.append(stock)

# Initialize complete data set
DataSet = {k: AnalystRes[k] for k in stocklist} 

# User pandas_reader.data.DataReader to load the desired data. As simple as that.
google_data = web.get_data_google(stocklist,marketdate)
for stock in stocklist:
  DataSet[stock]['Google_data'] = google_data.minor_xs(stock)
  
# # Try yahoo API
# yahoo_data = web.get_data_yahoo(stocklist,marketdate)
# for stock in stocklist:
  # DataSet[stock]['Yahoo_data'] = google_data.minor_xs(stock)
# print('\nDaily Data Successfully Downloaded, and DataSet is ready!\n')


"""
Run Data Analysis: based on comparison between price target from and price target to 
"""
cont_mat = 0
cont_dis = 0
goodstock = []
for stock in DataSet.keys():

  stock_googledata  = DataSet[stock]['Google_data']
  # stock_yahoodata   = DataSet[stock]['Yahoo_data']
  
  stockkeys = DataSet[stock].keys()
  analystlist = [x for x in stockkeys if x not in ['Google_data','Yahoo_data']]
  
  for analyst in analystlist:
    stock_analystdata = DataSet[stock][analyst]
    pricetargfrom = stock_analystdata.get_value(targetdate,'PriceTarg_from')
    pricetargto   = stock_analystdata.get_value(targetdate,'PriceTarg_to')
    ratingto      = stock_analystdata.get_value(targetdate,'Rating_to')

    pricetargdelta = 0
    pricemarkdelta = 0
    if pricetargfrom and pricetargto:
      for str in ["$",","]:
        pricetargfrom = pricetargfrom.replace(str,"")
        pricetargto   = pricetargto.replace(str,"")
      pricetargfrom = float( pricetargfrom.strip() )
      pricetargto   = float( pricetargto.strip() )
      pricetargdelta = pricetargto - pricetargfrom
    
      priceopen  = stock_googledata['Open'].get_value(marketdate)
      priceclose = stock_googledata['Close'].get_value(marketdate)
      pricemarkdelta = priceclose - priceopen

      if (ratingto.strip() in ['Buy','Outperform']) and (pricetargdelta/pricetargfrom >=0.2):
        goodstock.append(stock)
 
      if (pricetargdelta > 0) and (pricemarkdelta > 0):
         print('*****Stock %s: target price increase, market price increase*****' %(stock)) 
         print ('Target Price From: %.3g, Target Price To: %.3g \
                Market Price Open: %.3g, Market Price Close: %.3g \n' \
                %(pricetargfrom, pricetargto, priceopen, priceclose))
         cont_mat += 1
 
      elif (pricetargdelta > 0) and (pricemarkdelta < 0): 
         print('*****Stock %s: target price increase, market price decrease*****' %(stock)) 
         print ('Target Price From: %.3g, Target Price To: %.3g \
                Market Price Open: %.3g, Market Price Close: %.3g \n' \
                %(pricetargfrom, pricetargto, priceopen, priceclose))
         cont_dis += 1
      
      # elif (pricetargdelta < 0) and (pricemarkdelta < 0):
         # print('*****Stock %s: target price decrease, market price decrease*****' %(stock)) 
         # print ('Target Price From: %.3g, Target Price To: %.3g \
                # Market Price Open: %.3g, Market Price Close: %.3g \n' \
                # %(pricetargfrom, pricetargto, priceopen, priceclose))
         # cont_mat += 1
 
      # elif (pricetargdelta < 0) and (pricemarkdelta > 0): 
         # print('*****Stock %s: target price decrease, market price increase*****' %(stock)) 
         # print ('Target Price From: %.3g, Target Price To: %.3g \
                # Market Price Open: %.3g, Market Price Close: %.3g \n' \
                # %(pricetargfrom, pricetargto, priceopen, priceclose))
         # cont_dis += 1
GoodStockSet = { k: DataSet[k] for k in goodstock }
print(GoodStockSet.keys())
print('Target price and market price trends match: %d, dismatch: %d' %(cont_mat, cont_dis))
print('Done')
