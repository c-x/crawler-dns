# Spider: http://www.afnic.fr/en/products-and-services/services/daily-list-of-registered-domain-names/
# .fr, .re, .yt, .tf, .wf and .pm.
# 20120331_CREA_fr.txt 

from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request

import re,sys
from time import strftime
from datetime import datetime,timedelta
from dnsmonitor.items import DNSItem


class AfnicSpider(BaseSpider):
	name            = "afnic"
	allowed_domains = ["afnic.fr"]
	start_urls      = []


	def __init__(self):
		afnic_ext       = ['fr','re','yt','tf','wf','pm']

		yesterday   = datetime.now() - timedelta(days=1)
		date        = yesterday.strftime("%Y%m%d")
		self.dbdate = yesterday.strftime("%Y-%m-%d")

		for ext in afnic_ext:
			f = 'http://www.afnic.fr/data/divers/public/publication-quotidienne/' + date + '_CREA_' + ext + '.txt'
			self.start_urls.append(f)

	def parse(self, response):
		#hxs   = HtmlXPathSelector(response)

		doms = re.split('\n', response.body)

		for d in doms:
			r = re.search('^(#|$)', d.strip())
			if( not r ):
				yield DNSItem(_id=d, registrar="afnic.fr", date=self.dbdate, ip='none')

