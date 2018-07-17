# -*- coding:  utf-8 -*-

from scrapy import Spider, Request

class FieldSpider(Spider):
	"""docstring for FieldSpider"""

	name = 'StockFieldInfo'
	allowed_domains = ['eastmoney.com']

	def start_Requests(self):
		yield Request()