# Scrapy settings for dnsmonitor project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

####################
# Collection Mongo #
####################
DB_HOST       = '127.0.0.1'
DB_PORT       = 27017
DB_DATABASE   = 'dns'
DB_COLLECTION = 'dns'

#################
# Config Scrapy #
#################
BOT_NAME    = 'dns'
BOT_VERSION = '1.0'

SPIDER_MODULES   = ['dns.spiders']
NEWSPIDER_MODULE = 'dns.spiders'

#USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
USER_AGENT = 'Mozilla/5.0 (X11; U; Linux i686; de-AT; rv:1.8.0.2) Gecko/20060309 SeaMonkey/1.0'

ITEM_PIPELINES = [
	'dns.pipelines.dbInsertPipeline',
]

