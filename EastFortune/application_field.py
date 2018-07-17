# -*- coding: utf-8 -*-


import sys
import json

def quick_get(data_list, code):
	
	res = ''
	for data in data_list:
		
		json_data = json.loads(data)

		if json_data['code'] == code or json_data['name'] == code:
			#print 'match is ', data.decode('utf-8')
			res = data
			break

	return res

def search_similar(data_list, code):
	
	res = []
	resdata = {}

	json_data = json.loads(code)
	data_filed_list = json_data['field']

	if data_filed_list is not None:
		data_field_list = data_filed_list.split(' ')

	print 'data fileds is', data_filed_list

	if len(data_filed_list) == 0:
		return res

	relatives = 0

	for data in data_list:
		json_tmp = json.loads(data)

		fields = json_tmp['field']

		#print 'fileds is ', fields

		if fields is not None:
			field_list = fields.split(' ')

		if len(field_list) > 0:
			
			for l in data_field_list:
				if l in field_list:
					relatives += 1

		if relatives > 7:
			resdata['code'] = json_tmp['code']
			resdata['price'] = json_tmp['price']
			resdata['psr'] = json_tmp['psr']
			resdata['relative'] = relatives
			resdata['name'] = json_tmp['name']
			res.append(resdata)

		resdata = {}
		relatives = 0

	return res


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


def main(filename):

	i = input('Please input your concerned stock code or name: ')

	if isinstance(i, int):
		number = str(i)
	else:
		number = i

	f = open(filename, 'rb')

	data_list = f.readlines()

	data = quick_get(data_list, number)

	f.close()

	if data is None:
		print 'Can\'t find the stock as you looked'
		exit()

	#print data.decode('utf-8')

	similar_list = search_similar(data_list, data)

	#

	similar_list = sorted(similar_list, key=lambda x: x['relative'], reverse=True)


	if len(similar_list) > 0:
		print 'similar_list is showed as below:'
		print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
		print u'股票名称  ', 'PSR            ', u'当前价格'
		print '--------------------------------'
		for similar in similar_list:
			print similar['name'], ' ', similar['psr'], ' ', similar['price']
	else:
		print 'There is no stock in the same field'

	


if __name__ == '__main__':
	
	if len(sys.argv) != 2:
		print 'Usage: python xxx.py input_name'
	
	main(sys.argv[1])