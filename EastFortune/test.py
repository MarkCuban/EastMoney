# -*- coding: utf-8 -*-

import json
import re


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




string = '(万股)</span></th><td class="tips-data-Left"><span>7,426,272.66</span></td></tr><tr><th class="tips-fieldname-Left"><span>稀释每股收益(元)</span></th><td class="tips-data-Left"><span>0.7000</span></td><th class="tips-fieldname-Left"><span>每股未分配利润(元)</span></th><td class="tips-data-Left"><span>1.5619</span></td><th class="tips-fieldname-Left"><span>流通股本(万股)</span></th><td class="tips-data-Left"><span>3,925,086.40</span></td></tr></table><div class="tfoot">数据来源:2017三季报;其中每股收益字段均以最新总股本计算得出，精确到小数点后四位，其余指标若发生股本变动等情况则将重新计算</div>'

tmp = string.split('<span>')[1]
tmp = tmp.split('</span>')[0]


print 'End is ', tmp


