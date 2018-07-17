
import sys

import json



def preprocess(datalist):
	
	reslist = []

	for data in datalist:
		
		json_str = json.loads(data)

		field_str = json_str['field']

		if field_str == None:
			continue

		field_list = field_str.split(' ')

		for field in field_list:
			
			if field not in reslist:
				reslist.append(field)

	print 'field is showed as below:'
	
	string = ''
	for res in reslist:
		string += res + ' '

	print string






def main(filename):
	
	f = open(filename, 'rb')

	datalist = f.readlines()

	preprocess(datalist)

		
	f.close()





if __name__ == '__main__':
	
	if len(sys.argv) != 2:
		print 'Usage: python input_name'
	main(sys.argv[1])