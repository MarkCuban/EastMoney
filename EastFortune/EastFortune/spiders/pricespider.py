# -*- coding:  utf-8 -*-

import scrapy
import re
from scrapy import Request
from scrapy.selector import Selector
import csv
import time

from tools import map_to, map_to_csv


INDEX_URL = 'http://quote.eastmoney.com/stocklist.html#sh'

SUB_URL = 'http://quotes.money.163.com/service/chddata.html?code=0&end=0&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'

class StockPriceEachDaySpider(scrapy.Spider):
	"""docstring for StockPriceEachDaySpider"""

	name = 'StockPriceSpider'
	allowed_domains = ['eastmoney.com']

	def start_requests(self):
		yield Request(INDEX_URL)

	def infoparse(self, response):
		
		print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
		print '------------infomation is parsed here--------------'

		codes = response.url.split('code=0')
		if len(codes) > 1:
			code = codes[1]
			code = code.split('&end=')[0]
		else:
			code = response.url.split('code=1')[1]
			code = code.split('&end=')[0]			

		with open('stock/'+code+'.csv', 'wb') as f:
			f_csv = csv.writer(f)
			strings = response.body.split('\n')

			for string in strings:
				#print 'type of string is ', type(string)
				datas = string.split(',')

				f_csv.writerow(datas)


	def parse(self, response):
		print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
		print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
		sel = Selector(response)
		conts = sel.xpath('//div[@class="qox"]/div[@class="quotebody"]/div/ul')


		#this section is used for debug

#		urlstrings = SUB_URL.split('0')
#		stockcode = '601333'
#		nexturl = urlstrings[0]+'0'+stockcode+urlstrings[1]+'20070129'+urlstrings[2]
#		yield Request(nexturl, callback=self.infoparse, dont_filter=True)

		#end

		idx = 0

		for cont in conts:
			idx = conts.index(cont)

			for i in re.findall(r'<li>.*?<a.*?target=.*?>(.*?)</a>', cont.extract()):

				stockcode = (i.split("(")[1][:-1]).encode('utf-8')
				urlstrings = SUB_URL.split('0')

				if idx >= 1:
					nexturl = urlstrings[0]+'1'+stockcode+urlstrings[1]+time.strftime('%Y%m%d')+urlstrings[2]
				else:
					nexturl = urlstrings[0]+'0'+stockcode+urlstrings[1]+time.strftime('%Y%m%d')+urlstrings[2]

				#print 'nexturl is ', nexturl
				yield Request(nexturl, callback=self.infoparse, dont_filter=True)
