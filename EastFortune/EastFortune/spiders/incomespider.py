import scrapy
from scrapy.selector import Selector
from scrapy import Request

import re
import json

from EastFortune.items import IncomeINFOItem

INDEX_URL = 'http://quote.eastmoney.com/stocklist.html#sh'
INCOME_URL = 'http://emweb.securities.eastmoney.com/PC_HSF10/BusinessAnalysis/BusinessAnalysisAjax?code=sh'
INCOME_URL = 'http://emweb.securities.eastmoney.com/PC_HSF10/OperationsRequired/OperationsRequiredAjax?times=1&code=sz002603'

class IncomeSpider(scrapy.Spider):
	"""docstring for incomeSpider"""
	#def __init__(self, arg):
	#	super(incomeSpider, self).__init__()
	#	self.arg = arg
	
	name = 'CompanyIncome'

	allowed_domains = ['eastmoney.com']

	def start_requests(self):
		yield Request(INDEX_URL)

	def infoparse(self, response):
		
		print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
		print '!!!!!!!!!!!!    price information is parsed here     !!!!!!!!!!!!!!!!!!!!!!!!!'
		
		item = IncomeINFOItem()

		stockcode = response.url.split('sh')[1]

		print 'data info is ', stockcode

		try:
			json_ob = json.loads(response.body)
			item['stockCode'] = stockcode
			item['IncomeInfo'] = json_ob['zygcfx']

			yield item

		except ValueError, e:
			print 'This is not a json string, the url is ', response.url



	def parse(self, response):
		
		sel = Selector(response)
		cont = sel.xpath('//div[@class="qox"]/div[@class="quotebody"]/div/ul')[0].extract()

		for i in re.findall(r'<li>.*?<a.*?target=.*?>(.*?)</a>', cont):

			stockcode = (i.split("(")[1][:-1]).encode('utf-8')
			data_url = INCOME_URL + stockcode
			#stockcode = '&id='+stockcode
			#next_url = re.sub(r'&id=', stockcode, INCOME_URL)
			 
			yield Request(data_url, callback=self.infoparse, dont_filter=True)		
