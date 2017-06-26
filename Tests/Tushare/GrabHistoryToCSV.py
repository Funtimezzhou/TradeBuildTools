#This function is to grab history data and save the data into csv file
#
#@author: Junqiang Zhou, April 2017
#

#python -m pdb .py



import tushare
import numpy 
import matplotlib.pyplot as plot


def movingaverage(interval, window_size):
    window = numpy.ones(int(window_size))/float(window_size)
    return numpy.convolve(interval, window, 'same')
	
	
List = ['600008', '600009', '600012', '600017', '600018', '600020', '600027', '600029', '600033', '600035', '600050', '600098', '600101', '600106', \
		'600115', '600116', '600125', '600131', '600168', '600190', '600221', '600236', '600269', '600270', '600279', '600283', '600284', '600292', \
		'600310', '600317', '600323', '600326', '600333', '600350', '600368', '600369', '600377', '600386', '600387', '600396', '600452', '600461', \
		'600505', '600508', '600509', '600548', '600561', '600575', '600578', '600611', '600635', '600640', '600642', '600644', '600649', '600662', \
		'600692', '600717', '600719', '600726', '600741', '600744', '600751', '600768', '600769', '600795', '600798', '600820', '600834', '600863', \
		'600864', '600896', '600897', '600917', '600936', '600969', '600979', '600982', '600986', '600995', '600996', '601006', '601008', '601018', \
		'601111', '601139', '601158', '601186', '601188', '601199', '601212', '601333', '601368', '601518', '601669', '601800', '601880', '601985', \
		'601991', '601999', '603032', '603393', '603421', '603588', '603689', '603817', '603843', '900903', '900937', '900938', '900945', '900948', \
		'601228', '002108', '600481', '300409', '002154', '000718', '600759' ]

idxstock = 29
stock = List[idxstock]
print('Stock is ' + stock)

hist2016 = tushare.get_k_data(stock, ktype = '60',start='2016-01-23',end='2016-12-16')
# # plot raw data
# fig = plot.figure()
# ax = hist2016[['open','close','high','low']].plot(color=['g','r','b','k'],title = stock)
# ax.set_xlabel("Date")
# ax.set_ylabel('Price')
# plot.show()

# compute moving average
# get open and close price
window = 5
fig = plot.figure()
dopen  = hist2016['open'].tolist()
dclose = hist2016['close'].tolist()
dopen_av = movingaverage(dopen,window)
dclose_av = movingaverage(dclose,window)
plot.plot(dopen[window//2:len(dopen_av)-window//2], color = 'g')
plot.plot(dopen_av[window//2:len(dopen_av)-window//2],color = 'r')
plot.show()


# save to csv
fname = '../History Data/' + stock + '.csv'
with open(fname,'a') as fd:
	hist2016.to_csv(fd,header = True)