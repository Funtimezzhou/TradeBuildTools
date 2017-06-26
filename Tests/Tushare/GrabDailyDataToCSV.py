#This function is to grab real time data and save the data into csv file
#
#@author: Junqiang Zhou, April 2017
#

#python -m pdb .py



import tushare
import numpy 
import matplotlib.pyplot as plot
import time
import datetime
import os
import sys

# # get historical data
List = numpy.array(['600008', '600009', '600012', '600017', '600018', '600020', '600027', '600029', '600033', '600035', '600050', '600098', '600101', '600106', \
					'600115', '600116', '600125', '600131', '600168', '600190', '600221', '600236', '600269', '600270', '600279', '600283', '600284', '600292', \
					'600310', '600317', '600323', '600326', '600333', '600350', '600368', '600369', '600377', '600386', '600387', '600396', '600452', '600461', \
					'600505', '600508', '600509', '600548', '600561', '600575', '600578', '600611', '600635', '600640', '600642', '600644', '600649', '600662', \
					'600692', '600717', '600719', '600726', '600741', '600744', '600751', '600768', '600769', '600795', '600798', '600820', '600834', '600863', \
					'600864', '600896', '600897', '600917', '600936', '600969', '600979', '600982', '600986', '600995', '600996', '601006', '601008', '601018', \
					'601111', '601139', '601158', '601186', '601188', '601199', '601212', '601333', '601368', '601518', '601669', '601800', '601880', '601985', \
					'601991', '601999', '603032', '603393', '603421', '603588', '603689', '603817', '603843', '900903', '900937', '900938', '900945', '900948', \
					'601228', '002108', '600481', '300409', '002154', '000718', '600759' ], \
					dtype='object')
# hist2015 = tushare.get_hist_data(stock,start='2016-01-01',end='2017-04-07',ktype = 'D')
# hist2015 = hist2015.sort_index(ascending=True, axis=0)
# # print column names
# print(list(hist2015))
# # plot figure of open and close price
# # plot method - 1
# # fig = plot.gcf()
# # hist2015.open.plot(color='g')
# # hist2015.close.plot(color='r')
# # plot.xlabel('Time')
# # plot.ylabel('Price')
# # plot.legend('Open','Close')
# # plot.show()

# # plot method - 2
# ax = hist2015[['open','close']].plot(color=['g','r'],title = stock)
# ax.set_xlabel("Date")
# ax.set_ylabel('Price')
# plot.show()

# # get open and close price
# dopen  = hist2015['open'].tolist()
# dclose = hist2015['close'].tolist()


# time in range
def time_in_range(start, end, x):
	# return true if x is in the range [start,end]
	return start <= x <= end
	
# save data periodically to csv file
def SaveRealTimeQuotes():

	tstart = time.time()
	# get date time in CN
	datetimeCN = datetime.datetime.now()
	#datetimeCN = datetimeUS + datetime.timedelta(hours=12)
	# define working hours in morning and afternoon
	mstart = datetime.time(9,30)
	mend   = datetime.time(11,30)
	astart = datetime.time(13,0)
	aend   = datetime.time(15,0)
	
	# save data if working hour
	if time_in_range(mstart,mend,datetimeCN.time()) | time_in_range(astart,aend,datetimeCN.time()):
		try:
			for i in range(1,len(List)):
				stock = List[i]
				# extract real time quotes
				real_quote = tushare.get_realtime_quotes(stock)
				# #print(list(real_quote))
				# #print(real_quote['price'].values)
				
				file_path = '../Daily Data/' + str(datetimeCN.date())
				#print(file_path)
				if not os.path.exists(file_path):
				   os.makedirs(file_path)
				   
				# save to csv
				fname = '../Daily Data/' + str(datetimeCN.date()) + '/' + stock + '.csv'
				if os.path.exists(fname):
					with open(fname,'a') as fd:
						real_quote.to_csv(fd,header = False)
				else:
					with open(fname,'a') as fd:
						real_quote.to_csv(fd,header = True)
					
				
		except:
			logname = '../Daily Data/' + str(datetimeCN.date()) + '/' + 'LOG' + stock + '.log'
			with open(logname,'a') as fd:
				fd.write('No data available at ' + str(datetimeCN.time()) + '\n')
	else:
		print(str(datetimeCN.time()) + ' is not within working hour!')
		if (datetimeCN.time() > aend):
			sys.exit()
		
	# skip time
	tend = time.time()
	time.sleep(120 - (tend-tstart) )

while True:		
	SaveRealTimeQuotes()

# get today data
# today_ticks = tushare.get_today_ticks(stock)
# print(list(today_ticks))


# plot data
#plot.figure()
#plot.plot(df.Index.to_pydatetime(),df.open,'r')
#plot.plot(dt.Index.to_pydatetime(),df.close,'g')
#plot.xlabel('Time')
#plot.ylabel('Price')
#plot.legend('Open','Close')
#plot.show()






# save data to path
#df.to_csv('H:/Repository/trade/Data/000875.csv',columns=['open','high','low','close'])

# get real-time data
#df = tushare.get_realtime_quotes('000875') #Single stock symbol
#print(df[['code','name','price','bid','ask','volume','amount','time']])

#df = tushare.get_tick_data('600848',date='2017-04-10')
#print(df.head(10))