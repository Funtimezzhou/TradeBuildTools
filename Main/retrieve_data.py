# !/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

# import system module
import pandas_datareader.data as web

import matplotlib.pyplot as plt
import pandas as pd
# import user-defined module
import sys
sys.path.append('../lib')
import datatool


"""
Part0 - Obtain ticker symbols from S&P 500
"""
# Define the instruments to download. We would like to see Apple, Microsoft and the S&P500 index.
symbols = datatool.obtain_parse_wiki_snp500()
tickers = []  #tickers = ['AAPL', 'MSFT']
for i in range( len(symbols) ):
  stock = symbols[i][0].encode("utf-8")
  tickers.append( stock )

"""
Part 1 - Get history data and save to CSV file
"""

# We would like all available data from 01/01/2000 until 12/31/2016.
start_date = '2000-01-01'
end_date = '2017-06-25'

# User pandas_reader.data.DataReader to load the desired data. As simple as that.
goog_data, status = datatool.getdata_google(tickers, start_date, end_date)

# Try yahoo API
yahoo_data, status = datatool.getdata_google(tickers,start_date, end_date)

# save data to csv
fpath = '..\Data\History Data'
ok = datatool.savedatatocsv(goog_data,fpath)

"""
Part 2 - Get weekday data and process data
"""


# Getting just the close prices. This will return a Pandas DataFrame. The index in this DataFrame is the major index of the goog_data.
price_close = goog_data.ix['Close']

# Getting all weekdays between 01/01/2000 and 12/31/2016
all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')

# How do we align the existing prices in price_close with our new set of dates?
# All we need to do is reindex price_close using all_weekdays as the new index
price_close = price_close.reindex(all_weekdays)

# Reindexing will insert missing values (NaN) for the dates that were not present
# in the original set. To cope with this, we can fill the missing by replacing them
# with the latest available price for each instrument.
price_close = price_close.fillna(method='ffill')



"""
Part 3 - Visualize data
"""

# Get the MSFT time series. This now returns a Pandas Series object indexed by date.
msft = price_close.ix[:, 'MSFT']
# Calculate the 20 and 100 days moving averages of the closing prices
short_rolling_msft = msft.rolling(window=20).mean()
long_rolling_msft = msft.rolling(window=100).mean()

# Plot everything by leveraging the very powerful matplotlib package
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(msft.index, msft, label='MSFT')
ax.plot(short_rolling_msft.index, short_rolling_msft, label='20 days rolling')
ax.plot(long_rolling_msft.index, long_rolling_msft, label='100 days rolling')
ax.set_xlabel('Date')
ax.set_ylabel('Adjusted closing price ($)')
ax.legend()
plt.show()