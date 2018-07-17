# -*- coding: utf-8 -*-
import os

from stockDifferenceAnls import Analyse, showResult



STOCK_DIR = 'stock/'

START_YEARS = 2014

def JudgeStocks(difference):

	tars = []
	maxratio = 0
	minratio = 10

	for x in xrange(len(difference.reslist)):
		tars.append(round(float((difference.reslist[x])*100)/len(difference.dlst), 2))

	max()

def main():
	
	files = os.listdir(STOCK_DIR)

	for file1 in files:
		if not os.path.isdir(file1):
			anal = False
			for file2 in files:
				if not os.path.isdir(file2):
					if file1 == file2:
						anal = True
						continue

				if anal == True:
					diff = Analyse(file1.split('.csv')[0], file2.split('.csv')[0], START_YEARS, False)

					JudgeStocks(diff)



if __name__ == '__main__':
	main()