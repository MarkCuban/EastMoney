# -*- coding: utf-8 -*-

import sys
import csv
import re

from operator import itemgetter
from matplotlib import pyplot as plt

from matplotlib.ticker import MultipleLocator

import numpy as np

STOCK_DIR = 'stock/'

X_DAYS_AVERAGE = 10

X_AXIS_LABEL = 200

class Difference(object):
	"""docstring for Difference"""
	def __init__(self):
		
		self.maxprice = -999999
		self.max_date = ''

		self.minprice = 999999
		self.min_date = ''

		self.dlist = []
		self.datelst = []


class Stock(object):
	"""docstring for StockDifference"""
	def __init__(self, filename):

		self.code = 0
		self.price_map_date = {}

		self.file = open(filename, 'rb')
		self.lenth = len(self.file.readlines())-2

		self.file.seek(0)
		

		self.processfile()

	def __del__(self):
		
		self.file.close()


	def processfile(self):

		self.reader = csv.DictReader(self.file)

		for row in self.reader:	
			self.code = row[(u'股票代码').encode('gbk')]
			
			price_list = []
			price_list.append(row[(u'收盘价').encode('gbk')])
			price_list.append(row[(u'开盘价').encode('gbk')])

			self.price_map_date[row[(u'日期').encode('gbk')]] = price_list

		self.price_lst = sorted(self.price_map_date.iteritems(), key=lambda x:x[0])
		#print 'price_map_date is ', self.price_map_date
	
	def getPriceFromDate(self):
		pass

	def getPriceFromIndex(self, idx):
		#print 'idx is ', idx
		return self.price_lst[idx]


		

def getprice(stock, dates):
	res = []

	for x in xrange(dates):
		price = stock.getPriceFromIndex(x)[1][0]
		if price != 0:
			res.append(stock.getPriceFromIndex(x)[1][0])

	return res

def processDifferece(stock1, stock2, startyear):
	
	idx1 = 0
	idx2 = 0
	diff = Difference()

	#print 'startyear is', type(startyear)

	while stock1.getPriceFromIndex(idx1)[0] == "":
		idx1 += 1

	while stock2.getPriceFromIndex(idx2)[0] == "":
		idx2 += 1

	go_conti = False
	while True:

		if idx1 > stock1.lenth or idx2 > stock2.lenth:
			break

		date1 = stock1.getPriceFromIndex(idx1)[0]
		date2 = stock2.getPriceFromIndex(idx2)[0]

#		if startyear != 0:
		if startyear != "":
			if date1.startswith(str(startyear)) == False:
				idx1 += 1
				go_conti = True
			if date2.startswith(str(startyear)) == False:
				idx2 += 1
				go_conti = True
			if go_conti == True:
				go_conti = False
				continue

		if date1 > date2:
			idx2 += 1
		elif date1 < date2:
			idx1 += 1
		else:
			break

	dates = min(stock1.lenth, stock2.lenth)

	while True:

		if idx1 > stock1.lenth or idx2 > stock2.lenth:
			break

		price1 = float(stock1.getPriceFromIndex(idx1)[1][0])
		price2 = float(stock2.getPriceFromIndex(idx2)[1][0])

		if price1 == 0 or price2 == 0:
			idx1, idx2 = idx1 + 1, idx2 + 1
			continue

		diffprice = price1-price2

		if diff.maxprice < diffprice:
			diff.maxprice = diffprice
			diff.max_date = stock1.getPriceFromIndex(idx1)[0]

		if diff.minprice > diffprice:
			diff.minprice = diffprice
			diff.min_date = stock1.getPriceFromIndex(idx1)[0]

		diff.dlist.append(float('%.2f'%diffprice))

		string = re.sub('-', '', stock2.getPriceFromIndex(idx2)[0])

		diff.datelst.append(string)
		idx1, idx2 = idx1 + 1, idx2 + 1

	return diff

def average(dlist):
	
	return sum(dlist)/len(dlist)


def getXDayDifference(dlist, length):
	
	res = []

	for x in xrange(len(dlist)):
		five_average = average(dlist[x:x+length])
		res.append(five_average)

	return res


def main(code1, code2, startyear=0):
	
#	fcode1 = open(STOCK_DIR+code1+'.csv', 'rb')
#	fcode2 = open(STOCK_DIR+code2+'.csv', 'rb')


#	print 'file len is ', len(fcode1.readlines()), len(fcode2.readlines())

	print 'Processing... Please wait...'

	stock1 = Stock(STOCK_DIR+code1+'.csv')
	stock2 = Stock(STOCK_DIR+code2+'.csv')

	difference = processDifferece(stock1, stock2, startyear)

	print 'diff max is ', difference.maxprice, difference.max_date
	print 'diff min is ', difference.minprice, difference.min_date

	group_labels = []
	group_lst = []

	for x in xrange(len(difference.datelst)):
		if x % X_AXIS_LABEL == 0:
			group_labels.append(difference.datelst[x])

	fivedaydiff = getXDayDifference(difference.dlist, X_DAYS_AVERAGE)

	plt.plot(difference.datelst, difference.dlist, color='r', linestyle='-', linewidth=1)
	plt.plot(difference.datelst, fivedaydiff, color='b', linestyle='-', linewidth=1)
	plt.xticks(group_labels, group_labels, rotation=0)
	#plt.plot(x, fivedaydiff, color='b', linestyle='-', linewidth=1)

	plt.show()



if __name__ == '__main__':
	
	if len(sys.argv) == 3:
		#print 'Usage: python stockdifference.py code1 code2'
		main(sys.argv[1], sys.argv[2])
	elif len(sys.argv) == 4:
		main(sys.argv[1], sys.argv[2], sys.argv[3])
	else:
		print 'Usage: python stockdifference.py code1 code2 (startyear) '

