# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class DNSItem(Item):
	registrar  = Field()
	_id        = Field() # nameserver : default key for mongodb
	ip         = Field()
	date       = Field()
