# -*- coding: utf-8 -*-
import csv
import sys

STOCK_DIR = 'stock/'


class Stock(object):
	"""docstring for StockDifference"""
	def __init__(self, filename):

		self.code = 0
		self.price_map_date = {}
		self.junzhi = {}

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

	def getJunZhi(self, time):
		
		for x in self.price_lst:
			print x, type(x)


def main(code):

	stock = Stock(STOCK_DIR+code+'.csv')

	stock.getJunZhi(20)






if __name__ == '__main__':
	main(sys.argv[1])