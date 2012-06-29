# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

#class DnsmonitorPipeline(object):
from time import mktime, localtime, strftime
from socket import gethostbyname

import pymongo
from dnsmonitor.items import DNSItem
from scrapy.conf import settings
from scrapy import log


class dbInsertPipeline(object):

	def __init__(self):
		cnx      = pymongo.Connection(settings['DB_HOST'], settings['DB_PORT'])
		self.db  = cnx[ settings['DB_DATABASE'] ]
		self.col = self.db[settings['DB_COLLECTION']]

	def process_item(self, item, spider):

		if( isinstance(item, DNSItem) ):

			t = item['date'].split('-')
			tt= mktime( (int(t[0]), int(t[1]), int(t[2]), 0,0,0,0,0,0) )

			item['date'] = strftime("%Y-%m-%d", localtime(tt) )

			self.col.insert( dict(item) )
			log.msg("Wrote item to DB (%s/%s)" % (settings['DB_DATABASE'], settings['DB_COLLECTION']), level=log.DEBUG, spider=spider) 

		return item
