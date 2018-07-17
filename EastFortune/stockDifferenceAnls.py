# -*- coding: utf-8 -*-
import sys
from stockdifference import Stock, processDifferece


STOCK_DIR = 'stock/'
DENGFEN_TIME = 10

class StockDiffAnalysis(object):
	"""docstring for StockDiffAnalysis"""
	def __init__(self, max, min, difflst, datelst):
		
		self.max = max
		self.min = min
		self.step = 0
		self.dlst = difflst
		self.datelst = datelst
		self.reslist = []

		self.process()

	def __del__(self):
		pass

	def process(self):
		
		diff = round(self.max-self.min, 0)
		self.step = diff/DENGFEN_TIME

		for x in xrange(DENGFEN_TIME):
			self.reslist.append(0)

		for x in self.dlst:
			if int((x - self.min)//self.step) >= DENGFEN_TIME:
				self.reslist[DENGFEN_TIME-1] += 1
			elif int((x - self.min)//self.step) <= 0:
				self.reslist[0] += 1
			else:
				self.reslist[int((x - self.min)//self.step)] += 1



def processAnalyse():
	pass


def showResult(StockDiffAnalysis_ob):

	print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
	print 'Analyse result:'
	print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
	print 'max: ', StockDiffAnalysis_ob.max
	print 'min: ', StockDiffAnalysis_ob.min
	print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
	
	for x in xrange(DENGFEN_TIME):
		print 'Section %d:     %.2f - %.2f:      %.2f%%' % (x, round(StockDiffAnalysis_ob.min+x*StockDiffAnalysis_ob.step, 2), round(StockDiffAnalysis_ob.min+(x+1)*StockDiffAnalysis_ob.step, 2), float((StockDiffAnalysis_ob.reslist[x])*100)/len(StockDiffAnalysis_ob.dlst))



def Analyse(code1, code2, startyear, show=True):
	
	stock1 = Stock(STOCK_DIR+code1+'.csv')
	stock2 = Stock(STOCK_DIR+code2+'.csv')

	difference = processDifferece(stock1, stock2, startyear)

	#print 'difference is ', difference.maxprice, difference.max_date

	diffanl = StockDiffAnalysis(difference.maxprice, difference.minprice, difference.dlist, difference.datelst)

	if show == True:
		showResult(diffanl)

	return diffanl


if __name__ == '__main__':
	if len(sys.argv) == 4:
		Analyse(sys.argv[1], sys.argv[2], sys.argv[3])
	elif len(sys.argv) == 5:
		Analyse(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
	else:
		print 'input: python stockDifferenceAnls.py code1 code2'