# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EastfortuneItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
   	stockCode = scrapy.Field()
   	stockName = scrapy.Field()
   	price = scrapy.Field()
#   	income_info = scrapy.Field()
#   	PSR = scrapy.Field()


class IncomeINFOItem(scrapy.Item):
	"""docstring for IncomeINFOItem"""
	#def __init__(self, arg):
	#	super(IncomeINFOItem, self).__init__()
	#	self.arg = arg
	
	stockCode = scrapy.Field()
	IncomeInfo = scrapy.Field()
	#IncomeThisYear = scrapy.Field()


class PSRInfoItem(scrapy.Item):
	"""docstring for PSRInfoItem"""
	stockCode = scrapy.Field()
	field = scrapy.Field()
	zongguben = scrapy.Field()
	zongshouru = scrapy.Field()

		


		
