# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json

from EastFortune.items import EastfortuneItem, IncomeINFOItem, PSRInfoItem

from EastFortune.spiders.eastfortune import EastFortuneSpider
from EastFortune.spiders.incomespider import IncomeSpider
from EastFortune.spiders.PSR import PSRSpider

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

class EastfortunePipeline(object):

    def __init__(self):
    	pass
    	
    def open_spider(self, spider):
    	if isinstance(spider, EastFortuneSpider):
    		self.stockfile = open('EastMoney.json', 'wb')
    	elif isinstance(spider, IncomeSpider):
    		self.incomefile = open('CompanyIncome.json', 'wb')
    	elif isinstance(spider, PSRSpider):
    		self.psrfile = open('psr.json', 'wb')
    	#exit()

    def close_spider(self, spider):
    	if isinstance(spider, EastFortuneSpider):
    		self.stockfile.close()
    	elif isinstance(spider, IncomeSpider):
    		self.incomefile.close()
    	elif isinstance(spider, PSRSpider):
    		self.psrfile.close()
    	


    def process_item(self, item, spider):

		itemdict = {}

		if isinstance(item, EastfortuneItem):

			itemdict['name'] = item['stockName']
			itemdict['code'] = item['stockCode']
			itemdict['price'] = item['price']
			#print 'item is', itemdict, type(itemdict)

			itemdict['name'] = itemdict['name'].encode('utf-8')

			json.dump(itemdict, self.stockfile, ensure_ascii=False)
			self.stockfile.write('\n')

		elif isinstance(item, IncomeINFOItem):

			itemdict['code'] = item['stockCode']
			itemdict['IncomeInfo'] = item['IncomeInfo']

			#print 'itemdict is ', itemdict['IncomeInfo']

			itemdict = map_to(itemdict)

			json.dump(itemdict, self.incomefile, ensure_ascii=False)

			self.incomefile.write('\n')

		elif isinstance(item, PSRInfoItem):

			itemdict['code'] = item['stockCode']
			itemdict['field'] = item['field']
			itemdict['zongguben'] = item['zongguben']
			itemdict['zongshouru'] = item['zongshouru']

			itemdict = map_to(itemdict)

			json.dump(itemdict, self.psrfile, ensure_ascii=False)

			self.psrfile.write('\n')
#    	self.file.write('name: ' + item['stockName'] + ' ')
#    	self.file.write('code: ' + item['stockCode'] + ' ')
#    	self.file.write('price: ' + item['price'] + '\n')
#    	self.file.write('PSR: ' + str(item['PSR']) + '\n')

        #line = json.dumps(dict(item))+","
        #self.file.write(line.decode("unicode_escape"))

		return item
