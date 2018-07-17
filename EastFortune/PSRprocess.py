# -*- coding:  utf-8 -*-

import json
import sys
import re
import csv

def map_to(d):

	if isinstance(d, dict):

		res = {}

		for k, v in d.items():
			if isinstance(v, dict) or isinstance(v, list):
				v = map_to(v)
			elif isinstance(v, unicode):
				v = v.encode('utf-8')
			#c = type(v)
			res[k] = v

	elif isinstance(d, list):

		res = []

		for k in d:
			if isinstance(k, dict) or isinstance(k, list):
				res.append(map_to(k))
			elif isinstance(k, unicode):
				res.append(k.encode('utf-8'))

	return res

def map_to_csv(d):

	if isinstance(d, dict):

		res = {}

		for k, v in d.items():
			if isinstance(v, dict) or isinstance(v, list):
				v = map_to(v)
			elif isinstance(v, unicode):
				v = v.encode('gbk')
			#c = type(v)
			res[k] = v

	elif isinstance(d, list):

		res = []

		for k in d:
			if isinstance(k, dict) or isinstance(k, list):
				res.append(map_to(k))
			elif isinstance(k, unicode):
				res.append(k.encode('gbk'))

	return res

def main(stockfile, psrfile, outputfile):

	fs = open(stockfile, 'rb')
	fp = open(psrfile, 'rb')
	fout = open(outputfile, 'wb')

	psrs = fp.readlines()
	stocklist = fs.readlines()

	psrdict = {}

	idx = 0
	match = False
	conti = False

	rows = []

	for psr in psrs:

		json_psr = json.loads(psr)

		while True:
			json_stock = json.loads(stocklist[idx])

			psr_code = int(json_stock['code'])
			stock_code = int(json_psr['code'])

			if psr_code > stock_code:
				conti = True
				break
			elif psr_code < stock_code:
				idx += 1
			else:
				match = True
				break

			if idx >= len(stocklist):
				print 'stock end'
				break

		if conti:
			conti = False
			continue
					
		if match:

			if json_stock['price'] == '-':
				price = 0
			else:
				price = float(json_stock['price'])

			code = json_psr['code']
			capitalization_str = json_psr['zongguben']

			if capitalization_str is not None:
				capitalization = float(re.sub(',', '', capitalization_str))*10000
			else:
				capitalization = 0

			sales_str = json_psr['zongshouru']

			if sales_str is not None:
				sales_str = re.sub(',', '', sales_str)
			else:
				sales_str = u'--'

			if sales_str != u'--':
				number_str = re.search(r'\d+\.\d+', sales_str).group()
				number = float(number_str)
				base = re.sub(number_str, '', sales_str)

				for cha in base:
				
					if cha == u'万':
						number *= 10000
					elif cha == u'亿':
						number = number*100000000

				psr = price*capitalization / number
			else:
				psr = 0

			psrdict['code'] = code
			psrdict['psr'] = psr
			psrdict['price'] = price
			psrdict['field'] = json_psr['field']
			psrdict['name'] = json_stock['name']

			#print 'psrdict is ', psrdict

			resdict = map_to(psrdict)

			psrdict = map_to_csv(psrdict)

			#print 'psrdict after mapped is ', psrdict

			rows.append(psrdict)
			

			json.dump(resdict, fout, ensure_ascii=False)
			fout.write('\n')
			match = False
			psrdict = {}


	fout.close()
	fs.close()
	fp.close()

	#write in csv in order to analyse the data in convenience 

	headers = ['code', 'name', 'price', 'psr', 'field']

	#print 'rows is ', rows

	with open('result.csv', 'wb') as fcsv:
		f_csv = csv.DictWriter(fcsv, headers)
		f_csv.writeheader()
		f_csv.writerows(rows)




		


if __name__ == '__main__':
	
	if len(sys.argv) != 4:
		print 'Usage: python input_name output_name'
		exit()

	main(sys.argv[1], sys.argv[2], sys.argv[3])
