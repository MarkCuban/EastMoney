# -*- coding:  utf-8 -*-

import scrapy
from EastFortune.items import PSRInfoItem
from scrapy import Request
from scrapy.selector import Selector

import re

import json


INDEX_URL = 'http://quote.eastmoney.com/stocklist.html#sh'

#SUB_URL = 'http://emweb.securities.eastmoney.com/f10_v2/OperationsRequired.aspx?type=web&code=sh'
SUB_URL = 'http://emweb.securities.eastmoney.com/PC_HSF10/OperationsRequired/OperationsRequiredAjax?times=1&code='

class PSRSpider(scrapy.Spider):
	"""docstring for PSRSpider"""

	name = 'PSR'
	allowed_domains = ['eastmoney.com']

	def start_requests(self):
		yield Request(INDEX_URL)


	def infoparse(self, response):
		print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
		print '!!!!!!!!!!!!    stock information is parsed here     !!!!!!!!!!!!!!!!!!!!!!!!!'
		
		item = PSRInfoItem()

		stockstring = response.url.split('&code=sh')

		if len(stockstring) <= 1:
			stockstring = response.url.split('&code=sz')

		#print 'stockstring is', stockstring

		try:
			json_ob = json.loads(response.body)
			item['stockCode'] = stockstring[1]

			if len(json_ob['hxtc']) >= 1:
				item['field'] = json_ob['hxtc'][0]['ydnr']
			else:
				item['field'] = None

			if json_ob['zxzb1'] is not None:
				stringtmp = json_ob['zxzb1'].split(u'总股本')[1]
				stringtmp = stringtmp.split('<span>')[1]
				stringtmp = stringtmp.split('</span>')[0]
			else:
				stringtmp = None

			item['zongguben'] = stringtmp

			if json_ob['zxzb2'] is not None:
				stringtmp = json_ob['zxzb2'].split(u'营业总收入')[1]
				stringtmp = stringtmp.split('<span>')[1]
				stringtmp = stringtmp.split('</span>')[0]
			else:
				stringtmp = None

			item['zongshouru'] = stringtmp

			yield item

		except ValueError, e:
			print 'This is not a json string, the url is ', response.url

	def parse(self, response):
		sel = Selector(response)
		conts = sel.xpath('//div[@class="qox"]/div[@class="quotebody"]/div/ul')
		
		idx = 0

		for cont in conts:

			idx = conts.index(cont)

			for i in re.findall(r'<li>.*?<a.*?target=.*?>(.*?)</a>', cont.extract()):

				stockcode = (i.split("(")[1][:-1]).encode('utf-8')

				if idx >= 1:		#shen zhen 
					data_url = SUB_URL + 'sz' + stockcode
				else:
					data_url = SUB_URL + 'sh' + stockcode
			#stockcode = '&id='+stockcode
			#next_url = re.sub(r'&id=', stockcode, INCOME_URL)
			 
				yield Request(data_url, callback=self.infoparse, dont_filter=True)		