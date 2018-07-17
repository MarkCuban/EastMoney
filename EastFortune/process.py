
import sys
import json

def getOverAllIncome(incomeinfo):
	
	if incomeinfo == None:		
		return 0





def getIncomePriceRatio(price, income):
	pass


def main(stockfile, incomefile):

	fs = open(stockfile)
	fi = open(incomefile)

	stocklist = fs.readlines()
	incomelist = fi.readlines()

	i = 0
	match = False

	for stock in stocklist:

		stockdict = json.loads(stock)

		while True:

			incomedict = json.loads(incomelist[i])

			if stockdict['code'] == incomedict['code']:
				match = True
				break

			if i >= len(incomedict):
				print 'income over'
				break


		if match == True:

			income = getOverAllIncome(incomedict['IncomeInfo'])

			PIR = getIncomePriceRatio(float(stockdict['price']), income)
			


		







if __name__ == '__main__':

	if len(sys.argv) != 3:
		print 'Usage: python input_name output_name'
		exit()

	main(sys.argv[1], sys.argv[2])