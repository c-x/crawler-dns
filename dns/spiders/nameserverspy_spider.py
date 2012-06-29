# Spider: nameserverspy.org
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request

import re,sys
from time import gmtime, strftime
from dnsmonitor.items import DNSItem


class NameserverspySpider(CrawlSpider):
	name            = "nameserverspy"
	allowed_domains = ["nameserverspy.org"]
	start_urls      = ["http://www.nameserverspy.org"]

	rules = ( 
		Rule( SgmlLinkExtractor(restrict_xpaths='//table[@id="domain"]/tbody/tr/td/a[contains(@href,"date")]'), callback='parse_lastday', follow=True ), 
	)

	def parse_lastday(self, response):
		hxs   = HtmlXPathSelector(response)

		# http://nameserverspy.org/domain.php?date=2012-04-4&ns=vpweb.com
		# http://nameserverspy.org/domain.php?date=2012-04-4&ns=dns.com.cn
		# Extract date and nameserer from URI
		date      = strftime("%Y-%m-%d", gmtime())
		registrar = "unknown"

		r = re.search('date=(\d+-\d+-\d+)', response.url)
		if( r ):
			date = r.group(1)
		
		r = re.search('ns=([^ &]+)', response.url)
		if( r ):
			registrar = r.group(1)

		# Extract DNS Hosts from table
		domains = hxs.select('//table[@id="domain"]/tbody/tr/td/text()').extract()
		for domain in domains:
    			d = domain.strip()
			if( d ):
				yield DNSItem(_id=d, registrar=registrar, date=date, ip='none')

		# Extract next pages links (if any and if first page only)
		if( not re.search('&page=\d+', response.url) ):
			
			links = hxs.select('//table[@id="domain"]/tfoot/tr/td/a/@href').extract()
			for link in links:
				u = self.start_urls[0] + link
				yield Request(u, callback=self.parse_lastday)

