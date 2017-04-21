# This function is to import data from csv file and perform analysis
#
# Author: Junqiang Zhou, April 2017

import pandas
import csv
import matplotlib.pyplot as plot
import numpy

List = ['600009', '600012', '600017', '600018', '600020', '600027', '600029', '600033', '600035', '600050', '600098', '600101', '600106', \
		'600115', '600116', '600125', '600131', '600168', '600190', '600221', '600236', '600269', '600270', '600279', '600283', '600284', '600292', \
		'600310', '600317', '600323', '600326', '600333', '600350', '600368', '600369', '600377', '600386', '600387', '600396', '600452', '600461', \
		'600505', '600508', '600509', '600548', '600561', '600575', '600578', '600611', '600635', '600640', '600642', '600644', '600649', '600662', \
		'600692', '600717', '600719', '600726', '600741', '600744', '600751', '600768', '600769', '600795', '600798', '600820', '600834', '600863', \
		'600864', '600896', '600897', '600917', '600936', '600969', '600979', '600982', '600986', '600995', '600996', '601006', '601008', '601018', \
		'601111', '601139', '601158', '601186', '601188', '601199', '601212', '601333', '601368', '601518', '601669', '601800', '601880', '601985', \
		'601991', '601999', '603032', '603393', '603421', '603588', '603689', '603817', '603843', '900903', '900937', '900938', '900945', '900948', \
		'601228', '002108', '600481', '300409', '002154', '000718', '600759' ]

# /***************************************************************/
# /***************************************************************/
# /***************************************************************/
# import all csv data and find best stock	
avgrate = [0]*len(List)
for idxstock in range(len(List)):
	stock = List[idxstock]
	#print('Stock is ' + stock)
	
	# load stock data
	Date  = '2017-04-20'
	fname = '../Daily Data/' + Date + '/' + stock + '.csv'
	colnames = ['price', 'bid', 'ask', 'volume', 'amount']
	stockdata = pandas.read_csv(fname, encoding = "ISO-8859-1")

	# remove bad data (=0)
	vprice  = stockdata['price'].tolist()
	vbid	= stockdata['bid'].tolist()
	vask 	= stockdata['ask'].tolist()
	for idxtime in range(len(vprice)):
		if vprice[idxtime]==0:
			vprice.pop(idxtime)
			vbid.pop(idxtime)
			vask.pop(idxtime)
	

	# compute change rate
	dprice = []
	dpricefromopen = []
	for i in range(1,len(vprice)):
		dprice.append( (vprice[i] - vprice[i-1])/vprice[i-1]*100  )
		dpricefromopen.append( (vprice[i] - vprice[0])/vprice[0]*100  )	

	
	# compute average rate 
	avgrate[idxstock] = sum(dpricefromopen)/len(dpricefromopen)
	
# find stock with largest rate
sort_idx = numpy.argsort(avgrate)[::-1]
avgrate.sort(reverse = True)
# print(sort_idx)
for i in range(5):
	print("Rate Rank: Value=%f, Stock=%s" %(avgrate[i],List[sort_idx[i]]) )
# /***************************************************************/
# /***************************************************************/
# /***************************************************************/






# /***************************************************************/
# import csv data for best stock
for imaxrate in range(5):
	stock = List[sort_idx[imaxrate]]
	# load stock data
	Date  = '2017-04-20'
	fname = '../Daily Data/' + Date + '/' + stock + '.csv'
	colnames = ['price', 'bid', 'ask', 'volume', 'amount']
	stockdata = pandas.read_csv(fname, encoding = "ISO-8859-1")
	# remove bad data (=0)
	vprice  = stockdata['price'].tolist()
	vbid	= stockdata['bid'].tolist()
	vask 	= stockdata['ask'].tolist()
	for idxtime in range(len(vprice)):
			if vprice[idxtime]==0:
				vprice.pop(idxtime)
				vbid.pop(idxtime)
				vask.pop(idxtime)
	# compute change rate
	dprice = []
	dpricefromopen = []
	for i in range(1,len(vprice)):
		dprice.append( (vprice[i] - vprice[i-1])/vprice[i-1]*100  )	
		dpricefromopen.append( (vprice[i] - vprice[0])/vprice[0]*100  )	
		
	# plot data
	flagplot = True
	if flagplot:
		fig = plot.figure()
		fig.add_subplot(211)
		plot.plot(range(len(vprice)), vprice, color = 'g', label = 'Price')
		# stockdata.bid.plot(color = 'r', label = 'Bid')
		# stockdata.ask.plot(color = 'b', label = 'Ask')
		plot.legend()
		plot.xlabel('Time')
		plot.ylabel('Price')
		plot.title(stock)
		plot.draw()
		
		fig.add_subplot(212)
		plot.plot(range(1,len(vprice)), dprice, color = 'g', label = 'Rate From Last')
		plot.plot(range(1,len(vprice)), dpricefromopen, color = 'k', label = 'Rate From Open')
		plot.legend()
		plot.xlabel('Time')
		plot.ylabel('Rate')
		plot.draw()	
		
# show figure
if flagplot:	
	plot.show()
	


