# -*- coding: utf-8 -*-

import scrapy
import re
from EastFortune.items import EastfortuneItem
from scrapy.selector import Selector

import json
from scrapy import Request

INDEX_URL = 'http://quote.eastmoney.com/stocklist.html#sh'
SUB_URL = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=4f1862fc3b5e77c150a2b985b12db0fd&cb=jQuery18305577123502716224_1515051223806&id=1&type=r&iscr=false&_=1515051225157'
DAT_URL = 'http://emweb.securities.eastmoney.com/PC_HSF10/BusinessAnalysis/BusinessAnalysisAjax?code=sh'

class EastFortuneSpider(scrapy.Spider):
	"""docstring for EastFortuneSpider"""
	#def __init__(self, arg):
	#	super(EastFortuneSpider, self).__init__()
	#	self.arg = arg
	
	name = 'EastMoney'
	allowed_domains = ['eastmoney.com']

	#start_urls = [
					#'http://quote.eastmoney.com/center/'
	#			]

	def is_jason(self, jsonstr):
		try:
			json_object = json.loads(jsonstr)
		except ValueError, e:
			return False
		return True


	def start_requests(self):
		yield Request(INDEX_URL)

	def __init__(self):
		#self.url = INDEX_URL
		#self.url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=4f1862fc3b5e77c150a2b985b12db0fd&cb=jQuery18305577123502716224_1515051223806&id=0&type=r&iscr=false&_=1515051225157'
		self.data = EastfortuneItem()
		self.price = 0

	def priceparse(self, response):
		print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
		print '!!!!!!!!!!!!    price information is parsed here     !!!!!!!!!!!!!!!!!!!!!!!!!'
		print 'data info is ', self.data

	def infoparse(self, response):
		print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
		print 'Information crawl start. In this function, all the information will be crawled'
		#print 'response == ', response.body

		if re.match('jQuery', response.body) != None:

			string = response.body.split('(', 1)[1]
			string = string[:-1]

			#jsontmp = json.dumps(string)
			#print 'jsontmp == ', string
			try:
				data = json.loads(string)

				#print 'datas', datas
				if data:
					#for data in datas:

					#print 'data is = ', data

					#print 'data[code] = ', data['code']
					#print 'data[name] = ', data['name']
					#print 'data[price] =', data['info']['c']

					self.data['stockCode'] = data['code']
					self.data['stockName'] = data['name']
					#tmpstr = data['info']
					self.data['price'] = data['info']['c']
					self.price = (data['info']['c'])


					yield self.data
					

			except ValueError, e:
				print 'Not a json string'
#		else:
#			try:
#				data = json.loads(response.body)

#				self.income_info = data['zygcfx']

#				this_year = data['zygcfx'][0]['hy']

#				sum_up = 0
#				self.data['PSR'] = 0

#				print 'this_year is ', this_year

#				if this_year == '--' or this_year == None:
#					
#					pass
#				
#				else:
#
#					for hangye in this_year:
#						income = hangye['zysr']
#	
#						if income == '--':
#							pass
#						else:
#	
#							danwei = income[-1:]
#							number = income[:-1]
#	
#							if danwei == u'亿':
#								sum_up += float(number)*(10**8)
#							elif danwei == u'万':
#								sum_up += float(number)*(10**4)
#	
#					if self.price == 0:
#						self.data['PSR'] = 0
#					else:
#						self.data['PSR'] = sum_up/self.price
#
#				print self.data

#			yield self.data


#			except ValueError, e:
#				print 'May be not a json string'

	def parse(self, response):

		sel = Selector(response)
		conts = sel.xpath('//div[@class="qox"]/div[@class="quotebody"]/div/ul')

		for cont in conts:

			for i in re.findall(r'<li>.*?<a.*?target=.*?>(.*?)</a>', cont.extract()):

#				print 'i = ', i
				stockcode = (i.split("(")[1][:-1]).encode('utf-8')
				stockcode = '&id='+stockcode

				if stockcode.startswith('&id=002') or stockcode.startswith('&id=300'):
					next_url = re.sub(r'&id=1', stockcode+'2', SUB_URL)
				else:
					next_url = re.sub(r'&id=', stockcode, SUB_URL)
			 
				yield Request(next_url, callback=self.infoparse, dont_filter=True)




		#dont_filter to avoid debug filtered offsite request to....




