# -*- coding: utf-8 -*-


import sys
import json
import re

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



def getSameField(data_list, field):
	
	res = []
	res_data = {}

	field_list = field.split(' ')
	relative = 0

	for data in data_list:
		
		json_str = json.loads(data)

		if json_str['field'] is not None:
			fields = json_str['field'].split(' ')

			for fl in fields:
				#if re.search(field, fl) is not None:
				if fl in field_list:
					relative += 1

			if relative >= len(field_list):
				res_data['code'] = json_str['code']
				res_data['price'] = json_str['price']
				res_data['psr'] = json_str['psr']
				res_data['name'] = json_str['name']
				res.append(res_data)
				
			relative = 0
			res_data = {}

	return res



def main_loop(data_list):
	
	#print 'Input concerned field!'
	print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

	while True:

		field = raw_input('Please input the concerned field: ')

		if field == 'code':
			break

		field = unicode(field, 'gbk')
		#field = field.decode('utf-8')

		concerned_list = getSameField(data_list, field)

		concerned_list = sorted(concerned_list, key=lambda x:x['psr'])

		print 'field list is showed as below:'
		print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
		print u'股票名称  ', 'PSR            ', u'当前价格'
		print '--------------------------------'
		for similar in concerned_list:
			print similar['name'], ' ', similar['psr'], ' ', similar['price']		

	return 0

def main_similar(data_list):

	i = input('Please input your concerned stock code or name: ')

	if isinstance(i, int):
		number = str(i)
	else:
		number = i	

	data = quick_get(data_list, number)

	if data is None:
		print 'Can\'t find the stock as you looked'
		exit()

	similar_list = search_similar(data_list, data)

	similar_list = sorted(similar_list, key=lambda x: x['relative'], reverse=True)

	return similar_list


def main(filename):


	f = open(filename, 'rb')

	data_list = f.readlines()

	f.close()

	similar_list = main_similar(data_list)

	while True:

		if len(similar_list) > 0:
			print 'similar list is showed as below:'
			print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
			print u'股票名称  ', 'PSR            ', u'当前价格'
			print '--------------------------------'
			for similar in similar_list:
				print similar['name'], ' ', similar['psr'], ' ', similar['price']	
		else:
			print 'There is no stock in the same field'

		res = main_loop(data_list)
		if res == 0:
			similar_list = main_similar(data_list)

if __name__ == '__main__':
	
	if len(sys.argv) != 2:
		print 'Usage: python xxx.py input_name'
	
	main(sys.argv[1])